import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def bb_bands(df: pd.DataFrame):
    n = 20
    k = 2
    mb = df['c'].rolling(n).mean()
    std = df['c'].rolling(n).std(ddof=0)

    ub = mb + k * std
    lb = mb - k * std
    return ub, mb, lb

# def bb_signal(df, ub, lb):
#     sig = pd.Series(0, index=df.index)
#     sig[df['c'] > ub] = 1
#     sig[df['c'] < lb] = 2
#     return sig

data = pd.read_csv('binance-btc-usdt-spot-15m.csv')
data['high_vol'] = (data['quote_asset_vol'] > data['quote_asset_vol'].mean() * 3.5).astype(int)

ub, mb, lb = bb_bands(data)
# data['bb_break'] = bb_signal(data, ub, lb)
data['ub_break'] = (data['c'] > ub).astype(int)
data['lb_break'] = (data['c'] < lb).astype(int)

data['c_pct'] = ((data['c'] / data['o'] - 1) * 100).round(2)
data['h_pct'] = ((data['h'] / data['o'] - 1) * 100).round(2)
data['l_pct']  = ((data['l'] / data['o'] - 1) * 100).round(2)

data['label'] = np.sign(data['c_pct'].shift(-1)).map({-1: 0, 0: 1, 1: 2})

# data = data[(data['bb_break'] != 0) & data['high_vol']]

data.drop(columns=['o', 'h', 'l', 'c', 'vol', 'quote_asset_vol'], inplace=True)
data.to_csv('preprocess.csv', index=False)
print(data.head())
print(data.value_counts(subset='label'))