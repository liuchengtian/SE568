import numpy as np
import data_manager as DM
import os


def calculate_rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter
        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi


def read_historical(stockSymbol):
    dirname = os.path.dirname(__file__)
    path = '/csv/' + stockSymbol + '_historical.csv'
    dm = DM.DataManager(dirname + path)
    column_name = dm.column_names
    historical_prices = [dm.data[column_name[i]].tolist() for i in range(1,6)]
    # print(historical_prices)
    return historical_prices


def get_RSI(stockname):
    data = read_historical(stockname)
    return calculate_rsi(data).tolist()

