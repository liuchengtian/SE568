from ..config import *


def get_MACD(stockname, interval):
    data = ti.get_macd(symbol=stockname, interval=interval)
    return data


if __name__ == '__main__':
    print(get_MACD('AAPL', 'daily'))