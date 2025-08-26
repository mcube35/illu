import json
import pandas as pd
from binance.client import Client
import indicator

class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.client = Client(api_key, api_secret)
        
    def get_candles(self) -> pd.DataFrame:
        columns = ['ts','o','h','l','c','vol','close_time','quote_asset_vol','trades','taker_base_vol','taker_quote_vol','ignore']
        res = self.client.get_klines(symbol='BTCUSDT', interval='15m', limit=50)
        candle = pd.DataFrame(res, columns=columns).sort_values('ts')
        
        obj_cols = candle.select_dtypes(include=['object']).columns
        candle[obj_cols] = candle[obj_cols].astype(float)

        return candle
    
    def signal(self):
        candle = self.get_candles()
        
        candle['ts'] = pd.to_datetime(candle['ts'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
        candle['close_time'] = pd.to_datetime(candle['close_time'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        ub, mb, lb = indicator.bb_bands(candle)
        candle['ub_break'] = (candle['c'] > ub).astype(int)
        candle['lb_break'] = (candle['c'] < lb).astype(int)
        
        candle['prev_ub_break'] = candle['ub_break'].shift(1)
        candle['prev_lb_break'] = candle['lb_break'].shift(1)

        # 82246592.79은 데이터 56000개 기준 quote_asset_vol 평균값 * 3.5
        candle['high_vol'] = (candle['quote_asset_vol'] > 82246592.79).astype('Int64')
        
        # 롱 조건
        long_cond = (
            (candle['high_vol'].shift(2) == 1) &
            (candle['lb_break'].shift(2) == 1) &
            (candle['lb_break'].shift(1) == 1) &
            (candle['lb_break'] == 1)
        )
        
        # 숏 조건
        short_cond = (
            (candle['high_vol'].shift(2) == 1) &
            (candle['ub_break'].shift(2) == 1) &
            (candle['ub_break'].shift(1) == 1) &
            (candle['ub_break'] == 1)
        )

        # 시그널 컬럼 추가 (1=롱, -1=숏, 0=없음)
        candle['signal'] = 0
        candle.loc[long_cond, 'signal'] = 1
        candle.loc[short_cond, 'signal'] = -1
        return candle[['ts', 'close_time', 'high_vol', 'ub_break', 'lb_break', 'signal']]