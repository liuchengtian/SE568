from .analyzer import analyzeSymbol, SVMpredict
from .bayesian import BayesianCurveFitting
from .rsi import get_RSI
import time
# import sys
# sys.path.append('..')
from config import *
import mysql.connector
import sqlite3
import datetime


def function(stockname):
    # moving average
    print('get moving average result:')
    # pred_price = round(analyzeSymbol(stockname, 5),2)

    # # get Bayesian Prediction
    # print('get Bayesian result:')
    # model = BayesianCurveFitting()
    # data = model.read_csv(filename='StockTracking/backendserver/data/csv/'+stockname+'_historical.csv', y_in_column=4)
    # # get Bayesian Prediction
    # tmp = model.predict(y_vec=data)
    # returnBayesian = tmp[0]
    # variance = tmp[1]
    # print(returnBayesian)
    #
    # # get SVM prediction
    # print('get SVM result:')
    # returnSVM = SVMpredict(filename='StockTracking/backendserver/data/csv/'+stockname+'_historical.csv')
    # print(returnSVM)
    #
    # get RSI prediction
    print('get RSI result:')
    RSI = get_RSI(stockname)

    # connect database
    print('connect sqlite db')
    conn = sqlite3.connect('StockTracking/backendserver/data/database.db')
    cursor = conn.cursor()

    rt_price = """
        SELECT "4. close"
        FROM AAPL_realtime
        """
    cursor.execute('SELECT "4. close" FROM %s_realtime' % stockname)


    q_results = cursor.execute(rt_price)
    for i in q_results:
        rt_current = i[0]

    # rec_BS_A = ['BUY','SELL','HOLD']
    # if float(rt_current)*(0.99) > pred_price:
    #     rec_BS = rec_BS_A[1]
    # elif float(rt_current)*(1.01) < pred_price:
    #     rec_BS = rec_BS_A[0]
    # else:
    #     rec_BS = rec_BS_A[2]


    recent_trend_query = """
    SELECT date, `{__value_name__}`
    FROM {__stockname__}_historical
    order by date ASC;
    """
    move_avg_query = """
    SELECT {__stockname__}_historical.Date, {__stockname__}_historical.`{__value_name__}`, avg(historicaldata_past.`{__value_name__}`) as `{__value_name__}_window`
    FROM {__stockname__}_historical
    JOIN (
        SELECT
        {__stockname__}_historical.Date, {__stockname__}_historical.`{__value_name__}`
        FROM {__stockname__}_historical
    ) AS historicaldata_past 
      ON {__stockname__}_historical.Date BETWEEN  historicaldata_past.Date and date(historicaldata_past.Date, '+{__window__} days')
    GROUP BY 1, 2
    order by {__stockname__}_historical.Date ASC;
    """

    data_types = [
        '1. Open',
        '2. High',
        '3. Low',
        '4. Close',
        '5. Volume',
    ]

    date_and_moving_avg1_all = {}
    date_and_moving_avg2_all = {}
    date_and_trend_all = {}
    date_and_rsi_all = {}

    # print(move_avg_query.format(__stockname__=stockname, __value_name__='1. Open', __window__=3))
    i = 0
    for data_type in data_types:
        q_results = cursor.execute(recent_trend_query.format(__stockname__=stockname, __value_name__=data_type))
        recent_trend = []
        for result in q_results:
            unixtime = result[0]
            recent_trend.append([unixtime, result[1]])
        date_and_trend_all[data_type] = recent_trend

        q_results = cursor.execute(move_avg_query.format(__stockname__=stockname, __value_name__=data_type, __window__=50))
        date_and_moving_avg = []
        for result in q_results:
            unixtime = result[0]
            date_and_moving_avg.append([unixtime, result[2]])
        date_and_moving_avg1_all[data_type] = date_and_moving_avg

        q_results = cursor.execute(move_avg_query.format(__stockname__=stockname, __value_name__=data_type, __window__=150))
        date_and_moving_avg = []
        date_and_rsi = []
        j = 0
        for result in q_results:
            unixtime = result[0]
            date_and_moving_avg.append([unixtime, result[2]])
            date_and_rsi.append([unixtime, RSI[i][j]])
            j += 1
        date_and_moving_avg2_all[data_type] = date_and_moving_avg
        date_and_rsi_all[data_type] = date_and_rsi
        i += 1

        # print(chart_data_all_th)
        # print(chart_data_all_fth)

    print(date_and_moving_avg1_all)
    print(date_and_moving_avg2_all)
    print(date_and_trend_all)
    print(date_and_rsi_all)



# if __name__ == '__main__':
function('AAPL')