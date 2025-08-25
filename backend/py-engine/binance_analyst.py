import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import indicator

# CSV 불러오기
df = pd.read_csv("binance-btc-usdt-spot-15m.csv")
df.drop(columns=['vol'], inplace=True)

# z-score 계산
df['qvol_zscore'] = abs(stats.zscore(df['quote_asset_vol']))
df.drop(columns=['quote_asset_vol'], inplace=True)

# 볼밴 돌파여부
ma, upper, lower = indicator.bollinger(df['c'])
df['bbu_break'] = (df['c'] > upper).astype(int)
df['bbl_break'] = (df['c'] < lower).astype(int)

# 이전봉 대비 %
df['pct_change'] = ((1 - df['c'].shift(1) / df['c']) * 100).round(2)


# 정답데이터 샘플 만들기
df['label'] = (df['qvol_zscore'] > 3) & (df['bbu_break'] | df['bbl_break'])
df.to_csv('data.csv')
print(df[df['qvol_zscore'] > 3])

# 보고 작업하라고 만드는 txt파일
indices = df[df['qvol_zscore'] > 3].index
with open("indices.txt", "w") as f:
    for idx in indices:
        f.write(str(idx) + "\n")