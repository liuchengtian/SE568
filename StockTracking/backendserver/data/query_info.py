from .analyzer import analyzeSymbol, SVMpredict
from .bayesian import BayesianCurveFitting
from .rsi import get_RSI
from .macd import get_MACD
from .data_manager import DataManager


import time
# import sys
# sys.path.append('..')
from ..config import *
import mysql.connector
import sqlite3
import datetime

# connect database
print('connect sqlite db')
conn = sqlite3.connect('StockTracking/backendserver/data/database.db')
cursor = conn.cursor()


def query_info_date(stockname, time_type, from_time, to_time):
    query_date = """
        SELECT date
        FROM {__stockname__}_{__time_type__}
        WHERE date >= '{__from_time__}' and date <= '{__to_time__}'
        order by date ASC;
        """
    date = []
    q_results = cursor.execute(query_date.format(__stockname__=stockname, __time_type__=time_type,
                                            __from_time__=from_time, __to_time__=to_time))
    for res in q_results:
        date.append(res[0])
    return date


def query_info_close(stockname, time_type, from_time, to_time):
    close = []
    query_close = """
        SELECT `4. close`
        FROM {__stockname__}_{__time_type__}
        WHERE date >= '{__from_time__}' and date <= '{__to_time__}'
        order by date ASC;
        """
    q_results = cursor.execute(query_close.format(__stockname__=stockname, __time_type__=time_type,
                                            __from_time__=from_time, __to_time__=to_time))
    for res in q_results:
        close.append(res[0])
    return close


def query_info_rsi(stockname, time_type, from_time, to_time):
    # get RSI results
    print('get RSI result:')
    rsi = get_RSI(stockname, time_type, from_time, to_time)
    # returns a list of rsi
    return rsi


def query_info_svm(stockname, time_type=None, from_time=None, to_time=None):
    # get SVM prediction
    print('get SVM prediction:')
    svm = SVMpredict(filename='StockTracking/backendserver/data/csv/'+stockname+'_historical.csv')
    return svm


def query_info_bayesian(stockname, time_type=None, from_time=None, to_time=None):
    # get Bayesian prediction
    print('get Bayesian prediction:')
    model = BayesianCurveFitting()
    data = model.read_csv(filename='StockTracking/backendserver/data/csv/'+stockname+'_historical.csv', y_in_column=4)
    tmp = model.predict(y_vec=data)
    bayesian = tmp[0]
    variance = tmp[1]
    return bayesian


def query_info_neural_network(stockname, time_type, from_time, to_time):
    # moving average result
    print('get moving average result:')
    pred_price = round(analyzeSymbol(stockname, 5),2)
    pred_price1 = round(analyzeSymbol(stockname, 50),2)

    query_current_price = """
        SELECT "4. close"
        FROM {__stockname__}_{__time_type__}
        WHERE Date <= '{__to_time__}'
        """

    q_results = cursor.execute(query_current_price.format(__stockname__=stockname, __time_type__=time_type, __to_time__=to_time))
    for res in q_results:
        chart_data = res[0]
    current_price = chart_data
    rec_BS_A = ['BUY', 'SELL', 'HOLD']
    if float(current_price)*(0.99) > pred_price:
        rec_BS = rec_BS_A[1]
    elif float(current_price)*(1.01) < pred_price:
        rec_BS = rec_BS_A[0]
    else:
        rec_BS = rec_BS_A[2]

    if float(current_price)*(0.99) > pred_price1:
        rec_BS1 = rec_BS_A[1]
    elif float(current_price)*(1.01) < pred_price1:
        rec_BS1 = rec_BS_A[0]
    else:
        rec_BS1 = rec_BS_A[2]
    return pred_price, rec_BS, pred_price1, rec_BS1


def query_info_moving_avg(stockname, time_type, from_time, to_time):
    move_avg_query = """
        SELECT {__stockname__}_{__time_type__}.date, {__stockname__}_{__time_type__}.`{__value_name__}`, 
        avg({__time_type__}data_past.`{__value_name__}`) as `{__value_name__}_window`
        FROM {__stockname__}_{__time_type__}
        JOIN (
            SELECT
            {__stockname__}_{__time_type__}.date, {__stockname__}_{__time_type__}.`{__value_name__}`
            FROM {__stockname__}_{__time_type__}
        ) AS {__time_type__}data_past 
          ON {__stockname__}_{__time_type__}.date BETWEEN {__time_type__}data_past.date and date({__time_type__}data_past.date, '+{__window__} days')
        GROUP BY 1, 2
        order by {__stockname__}_{__time_type__}.date ASC;
        """

    q_results = cursor.execute(move_avg_query.format(__stockname__=stockname, __time_type__=time_type, __value_name__='4. close', __window__=30))
    date1 = []
    moving_avg1 = []
    for result in q_results:
        unixtime = result[0]
        if from_time <= unixtime <= to_time:
            date1.append(unixtime)
            moving_avg1.append(result[2])

    q_results = cursor.execute(move_avg_query.format(__stockname__=stockname, __time_type__=time_type, __value_name__='4. close', __window__=100))
    date2 = []
    moving_avg2 = []
    for result in q_results:
        unixtime = result[0]
        if from_time <= unixtime <= to_time:
            date2.append(unixtime)
            moving_avg2.append(result[2])
    data = {'SMA1': moving_avg1,
            'date1': date1,
            'SMA2': moving_avg2,
            'date2': date2}
    return data


def query_info_macd(stockname, time_type, from_time, to_time):
    # get MACD results
    print('get MACD result:')
    MACD = get_MACD(stockname, time_type, from_time, to_time)
    # pandas
    return MACD.loc[from_time:to_time]


def query_info_highest(stockname):
    query_highest = """
    SELECT max(t.`4. close`)
    FROM (SELECT `4. close`
            FROM {__stockname__}_historical
            ORDER BY date DESC
            LIMIT 10) AS t
    """
    q_results = cursor.execute(query_highest.format(__stockname__=stockname))
    for res in q_results:
        highest = res[0]
    return highest


def query_info_average(stockname):
    query_average = """
    SELECT avg(t.`4. close`)
    FROM (SELECT `4. close`
            FROM {__stockname__}_historical
            ORDER BY date DESC
            LIMIT 365) AS t
    """
    q_results = cursor.execute(query_average.format(__stockname__=stockname))
    for res in q_results:
        average = res[0]
    return average


def query_info_lowest(stockname):
    query_lowest = """
    SELECT min(t.`4. close`)
    FROM (SELECT `4. close`
            FROM {__stockname__}_historical
            ORDER BY date DESC
            LIMIT 365) AS t
    """
    q_results = cursor.execute(query_lowest.format(__stockname__=stockname))
    for res in q_results:
        lowest = res[0]
    return lowest


# if __name__ == '__main__':
# function('AAPL', 'daily')
# print(query_info_macd('AAPL', 'historical', '2003-01-01', '2004-01-01'))
print(query_info_lowest('AAPL'))
