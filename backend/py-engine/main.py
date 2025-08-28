import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from decimal import Decimal
import json
from fastapi import FastAPI
import binance_client
from okx_trade import OkxTrade
from okx.Trade import TradeAPI
from okx.Account import AccountAPI
import pymysql

# 조회 반영이 잘 안되어서 autocommit = True

def get_conn():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='1234',
        db='illu',
        autocommit=True
    )

TRADE_CONFIGS = {}
OKX_FLAG = '1' # live trading: 0, demo trading: 1
INST_ID = "BTC-USDT-SWAP"

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(okx_auto_loop())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/trade/signal")
def binance_candles():
    client = binance_client.BinanceClient(api_key="", api_secret="")
    signal = client.signal()
    return json.loads(signal.to_json(orient="records"))

def open_position(trade_api: TradeAPI, side: str, size: float):
    """
    포지션 열기 (롱/숏)
    side: "long" or "short"
    """
    result = trade_api.place_order(
        instId=INST_ID,
        tdMode="isolated",
        side="buy" if side == "long" else "sell",
        posSide=side,
        ordType="market",
        sz=str(size),
    )
    print(f'open_position: {result}')
    return result


def close_position(acc_api: AccountAPI, trade_api: TradeAPI, side: str):
    """
    포지션 청산 (롱/숏)
    side: "long" or "short"
    """
    # 1. 현재 포지션 조회
    res = acc_api.get_positions(instId=INST_ID)
    positions = res.get("data", []) if isinstance(res, dict) else []

    # 2. 해당 방향 포지션 찾기
    pos = next((p for p in positions if p.get("posSide") == side), None)
    if not pos or float(pos.get("pos", 0)) == 0:
        print(f"{side.upper()} 포지션 없음")
        return False

    # 3. 청산 수량
    sz = max(float(pos["pos"]), float(pos.get("minSz", 0.0001)))

    # 4. 시장가 청산 주문
    result = trade_api.place_order(
        instId=INST_ID,
        tdMode="isolated",
        side="sell" if side == "long" else "buy",
        posSide=side,
        ordType="market",
        sz=str(sz)
    )
    print(f'close_position: {result}')
    return result

def to_config(row) -> OkxTrade:
    config_id = row['id']
    config = TRADE_CONFIGS.get(config_id, OkxTrade())
    
    config.config_id = config_id
    config.user_id = row['user_id']
    
    config.long_input_pct = row['long_input_pct']
    config.short_input_pct = row['short_input_pct']
    
    api_key = row['api_key']
    api_secret = row['api_secret']
    passphrase = row['passphrase']
    
    if not config.account_api:
        config.account_api = AccountAPI(
            api_key=api_key,
            api_secret_key=api_secret,
            passphrase=passphrase,
            use_server_time=True,
            flag=OKX_FLAG
        )

    if not config.trade_api:
        config.trade_api = TradeAPI(
            api_key=api_key,
            api_secret_key=api_secret,
            passphrase=passphrase,
            use_server_time=True,
            flag=OKX_FLAG
        )
        
    TRADE_CONFIGS[config_id] = config
    return config

def get_running_rows():
    conn = get_conn()
    
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        sql = "SELECT * FROM trade_config WHERE is_running = 1"
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

async def okx_auto_loop():
    client = binance_client.BinanceClient(api_key="", api_secret="")
    
    while True:
        now = datetime.now()
        # 15분 단위 정각 (예: 10:00:00, 10:15:00 ...)
        if now.second % 10 == 0:
        # if now.minute % 15 == 0 and now.second == 0:
            # 시그널 가져오기
            data = client.signal()
            signal = data['signal'].iloc[-1]
            signal = 1

            rows = get_running_rows()
            for row in rows:
                config = to_config(row)
                
                res = config.account_api.get_positions(instId=INST_ID)
                positions = res.get("data", []) if isinstance(res, dict) else []
                has_position = any(float(p.get('pos', 0)) > 0 for p in positions)
                leverage = float(config.account_api.get_leverage(instId=INST_ID, mgnMode="isolated")['data'][0]['lever'])
                
                if has_position:
                    for p in positions:
                        pnl = float(p['uplRatioLastPx']) * 100 # last price기준으로 pnl계산
                        profit_threshold = 0.5 * leverage
                        lose_threshold = -0.5 * leverage
                        
                        if pnl > profit_threshold or pnl < lose_threshold or True:
                            result = close_position(acc_api=config.account_api, trade_api=config.trade_api, side=p['posSide'])
                            if result['code'] == '0':
                                await asyncio.sleep(1)
                                
                                p_history = config.account_api.get_positions_history(instId=INST_ID)
                                p_data = p_history['data'][0]
                                c_time = p_data['cTime']
                                u_time = p_data['uTime']
                                pnl = Decimal(p_data['realizedPnl'])
                                pnl_ratio = Decimal(p_data['pnlRatio']) * 100
                                
                                with get_conn().cursor() as cur:
                                    cur.execute("""
                                        INSERT INTO trade_history (c_time, u_time, pnl, pnl_ratio, user_id)
                                        VALUES (%s, %s, %s, %s, %s)
                                    """, (c_time, u_time, pnl, pnl_ratio, config.user_id))
                else:
                    max_size = config.account_api.get_max_order_size(instId=INST_ID, tdMode='isolated')

                    max_buy = int(float(max_size['data'][0]['maxBuy']) * 0.9)
                    max_sell = int(float(max_size['data'][0]['maxSell']) * 0.9)

                    if signal == 1:
                        open_position(trade_api=config.trade_api, side="long", size=max_buy)
                    elif signal == -1:
                        open_position(trade_api=config.trade_api, side="short", size=max_sell)

            # 이미 실행했으니 같은 초에서 여러 번 실행되지 않게 대기
            await asyncio.sleep(3)
        else:
            await asyncio.sleep(0.3)