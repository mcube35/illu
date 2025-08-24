import os
import okx.MarketData as MarketData
import time
from datetime import datetime
import pandas as pd

def okx_get_candlesticks(limit):
    try:
        flag = "0" # live trading: 0, demo trading: 1
        columns = ['ts','o','h','l','c','vol','volCcy','volCcyQuote','confirm']
        api = MarketData.MarketAPI(flag=flag)

        after = ""
        candles = []

        while len(candles) < limit:
            batch_size = min(300, limit - len(candles))

            res = api.get_history_candlesticks(
                instId="BTC-USDT-SWAP",
                bar="15m",
                limit=str(batch_size),
                after=after
            )

            data = res['data']
            if not data: break

            candles.extend(data)
            after = data[-1][0]
            time.sleep(0.2)
            print(f'Fetch Candles {len(candles)} / {limit}')

        df = pd.DataFrame(data=candles, columns=columns)
        df['ts'] = pd.to_datetime(df['ts'].astype(int), unit='ms')
        df.drop(columns=['confirm'], inplace=True)
        df.to_csv("okx-btc-usdt-swap-15m.csv", index=False)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    okx_get_candlesticks(limit=100000)
    # while True:
    #     now = datetime.now()
    #     # 15분 단위 + 0~4초 구간만 실행 (스킵 방지)
    #     if (now.minute % 15 == 0) and (now.second < 5):
    #         okx_get_candlesticks()
    #         time.sleep(10)     # 같은 구간 중복 실행 방지용
    #     else:
    #         time.sleep(1)
