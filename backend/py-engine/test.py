import pandas as pd

data  = pd.read_csv('binance-btc-usdt-spot-15m.csv')

print(round(data['quote_asset_vol'].mean() * 3.5, 2))