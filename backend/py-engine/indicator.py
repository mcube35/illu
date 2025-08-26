import pandas as pd

def bb_bands(df: pd.DataFrame):
    n = 20
    k = 2
    mb = df['c'].rolling(n).mean()
    std = df['c'].rolling(n).std(ddof=0)

    ub = mb + k * std
    lb = mb - k * std
    return ub, mb, lb