import os
import time
import pandas as pd
from binance.client import Client
from datetime import datetime

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(api_key, api_secret)

def binance_get_spot_candles(limit):
    try:
        symbol = "BTCUSDT"
        interval = "15m"
        candles = []

        batch_limit = 1000  # 한 번에 최대 1000개
        start_ts = None  # 시작 timestamp (ms)

        while len(candles) < limit:
            fetch_limit = min(batch_limit, limit - len(candles))

            # 시작시간 지정
            if start_ts:
                start_str = int(start_ts)
            else:
                start_str = "12 Jan 2024"

            # get_historical_klines 호출 (포지셔널 인자 사용)
            data = client.get_historical_klines(symbol, interval, start_str, limit=fetch_limit)

            if not data:
                break

            candles.extend(data)
            start_ts = data[-1][0] + 1  # 마지막 timestamp + 1ms

            print(f'Fetch Candles {len(candles)} / {limit}')
            time.sleep(0.2)

        # DataFrame 생성
        columns = ['ts','o','h','l','c','vol','close_time','quote_asset_vol','trades','taker_base_vol','taker_quote_vol','ignore']
        df = pd.DataFrame(candles, columns=columns)
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df.sort_values('ts', inplace=True)
        df.drop(columns=['close_time','trades','taker_base_vol','taker_quote_vol','ignore'], inplace=True)

        df.to_csv("binance-btc-usdt-spot-15m.csv", index=False)
        print("Saved CSV successfully")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    binance_get_spot_candles(limit=70000)