def bollinger(c, n=20):
    ma = c.rolling(n).mean()
    sd = c.rolling(n).std(ddof=0)
    return ma, ma+2*sd, ma-2*sd