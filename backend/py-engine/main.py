from datetime import datetime
import json
import time
from fastapi import FastAPI, Request
from threading import Thread
import binance_client

app = FastAPI()

trading_flags = {}
trading_threads = {}

@app.get("/")
def root():
    return {"message": "Hello World"}

# @app.get("/trade/signal")
# def binance_candles():
#     client = binance_client.BinanceClient(api_key="", api_secret="")
#     signal = client.signal()
#     return json.loads(signal.to_json(orient="records"))


def okx_auto_loop(user_id: str):
    client = binance_client.BinanceClient(api_key="", api_secret="")

    while trading_flags.get(user_id, False):
        now = datetime.now()
        # 15분 단위 정각 (예: 10:00:00, 10:15:00 ...)
        if now.minute % 15 == 0 and now.second == 0:
            data = client.signal()
            signal = data['signal']

            if signal == 1:
                execute_buy(user_id)
            elif signal == -1:
                execute_sell(user_id)

            # 이미 실행했으니 같은 초에서 여러 번 실행되지 않게 대기
            time.sleep(3)

        time.sleep(0.3)  # 계속 시간 체크

@app.get("/trade/okx_auto")
async def okx_auto(req: Request):
    try :
        data = await req.json()
        user_id = data.get("user_id")
        action = data.get("action")
        
        if not user_id or action not in ["start", "stop"]:
            return {"status": "error", "msg": "invalid request"}
        
        if action == "start":
            if trading_flags.get(user_id, False):
                return {"status": "running", "msg": f"{user_id} already trading"}
            trading_flags[user_id] = True
            t = Thread(target=okx_auto_loop, args=(user_id,), daemon=True)
            trading_threads[user_id] = t
            t.start()
            return {"status": "started", "user_id": user_id}

        elif action == "stop":
            trading_flags[user_id] = False
            trading_threads.pop(user_id, None)
            return {"status": "stopped", "user_id": user_id}
    except:
        return {"status": "error"}