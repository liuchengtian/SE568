import pip
import os
try:
    import mysql.connector  # using mysql connector should install it first(python 2.7/3.3/3.4)
except ImportError:
    pip.main(['install', 'mysql-connector-python'])
    print('You may need to run the script again.')
    import mysql.connector
try:
    from sqlalchemy import create_engine
    from sqlalchemy.types import VARCHAR
except ImportError:
    pip.main(['install', 'sqlalchemy'])
    from sqlalchemy import create_engine
    from sqlalchemy.types import VARCHAR
try:
    import pandas as pd
    from pandas import DataFrame
except ImportError:
    pip.main(['install', 'pandas'])
    import pandas as pd
try:
    import pandas_datareader as pdr
    from pandas_datareader import data, wb
except ImportError:
    pip.main(['install', 'pandas_datareader'])
    import pandas_datareader as pdr
    from pandas_datareader import data, wb
# try:
#     from datetime import *
# except ImportError:
#     pip.main(['install', 'datetime'])
#     from datetime import *
try:
    from alpha_vantage.timeseries import TimeSeries
except ImportError:
    pip.main(['install', 'alpha_vantage'])
    pip.main(['install', 'simplejson'])
    from alpha_vantage.timeseries import TimeSeries
try:
    import numpy as np
except ImportError:
    pip.main(['intall', 'numpy'])
    import numpy as np
try:
    import matplotlib.pyplot as plt
except ImportError:
    pip.main(['install', 'matplotlib'])
    import matplotlib.pyplot as plt
from time import sleep

User = 'root'
PassWord = 'password'
Host = '127.0.0.1'
Port = '3306'
Database = 'SEProject'
api_key = 'EQ6GGWD5D4ME4283'
# get TimeSeries object of Alpha Vintage API
ts = TimeSeries(key=api_key, output_format='pandas', retries=20)

# using alpha vantage finance api to save data into a pandas dataframe
stocks = ['AAPL', 'GOOGL', 'NVDA', 'AABA', 'AMZN', 'MSFT', 'BAC', 'NKE', 'NFLX', 'FB']
stocks = ['GOOGL']
####################################################

def init_db():
    # initialize database and create schema
    try:
        cnx = mysql.connector.connect(user=User, password=PassWord, host=Host)  # using configuration of sever
    except mysql.connector.Error:
        print('Can Not Connect With Database Sever.')
        raise SystemExit()
    cursor = cnx.cursor()

    # using mysql to create real time data
    create_RealtimeData = '''CREATE TABLE IF NOT EXISTS realtimedata               
                           (`date` DATETIME,
                            `open` REAL,
                            `high` REAL,
                            `low` REAL,
                            `close` REAL,
                            `volume` INTEGER,
                            `sym` CHAR(20),
                            PRIMARY KEY(sym,date)
                            );'''

    # using mysql to creat historical data
    create_HistoricalData = '''CREATE TABLE IF NOT EXISTS historicaldata
                           (`date` DATE,
                            `open` REAL,
                            `high` REAL,
                            `low` REAL,
                            `close` REAL,
                            `volume` INTEGER,
                            `sym` CHAR(20),
                            PRIMARY KEY(sym,date)
                            );'''
    cursor.execute('CREATE DATABASE IF NOT EXISTS ' + Database)  # creat database if not exists
    cursor.execute('USE ' + Database)  # select the database
    cursor.execute(create_RealtimeData)  # create table
    cursor.execute(create_HistoricalData)  # create table


def get_realtime_data(stock):
    realtime = []
    for ticker in stock:
        print("loading " + ticker)
        df, meta = ts.get_intraday(symbol=ticker, interval='1min', outputsize='compact')
        df['sym'] = meta['2. Symbol']
        realtime.append(df)
    return realtime


def get_hist_data(stock):
    historical = []
    for ticker in stock:
        print("loading " + ticker)
        df, meta = ts.get_daily(symbol=ticker, outputsize='full')
        df['sym'] = meta['2. Symbol']
        historical.append(df)
    return historical

def test_plot(df):
    plt.figure()
    plt.plot(df['4. close'].iloc[-260:], range(10))
    # plt.xticks(np.arange(10))
    plt.title('Times Series for the ' + df['sym'][0] + ' stock')
    plt.show()
    plt.close()

def main():
    init_db()
    print('Reading Data and Putting them in Database. Exit with Ctrl+C.')
    try:
        # returns current price and volume quotes for a given symbol in a dataframe
        engine = create_engine(
            'mysql+mysqlconnector://' + User + ':' + PassWord + '@' + Host + ':' + Port + '/' + Database,
            echo=False)

        # stocks = ['AAPL']
        df_historical = get_hist_data(stocks)
        print('Creating historical database.')
        for i in range(0, len(stocks)):
            df = df_historical[i]
            if not os.path.exists('data'):
                os.makedirs('data')
            df.to_csv('data/' + stocks[i] + '_historical.csv')
            df.to_sql(name=stocks[i].lower()+'_historical', con=engine, if_exists='replace',
                      dtype={'date': VARCHAR(df.index.get_level_values('date').str.len().max())})

        # ============= code for real-time quotes ==============
        print('Loading real-time data.')
        df_realtime = get_realtime_data(stocks)
        last_ones = []
        for i in range(0, len(stocks)):
            df = df_realtime[i]
            df.to_csv('data/' + stocks[i] + '_rtdata.csv')
            df.to_sql(name=stocks[i].lower()+'realtime', con=engine, if_exists='replace',
                      dtype={'date': VARCHAR(df.index.get_level_values('date').str.len().max())})
            last_ones.append(df_realtime[i].iloc[-1:])

        while True:
            print('Continue loading.')
            df_realtime = get_realtime_data(stocks)
            for i in range(len(stocks)):
                df_newest = pd.DataFrame(df_realtime[i].iloc[-1:])
                if df_newest.values.tolist()[0] == last_ones[i].values.tolist()[0]:
                    continue
                else:
                    last_ones[i] = df_newest
                with open('data/' + stocks[i] + '_rtdata.csv', 'a') as file:
                    df_newest.to_csv(file, header=False, index=True)
                df_newest.to_sql(name='realtimedata', con=engine, if_exists='append')
            sleep(20)


    except KeyboardInterrupt:
        print('User Asked to Exit')
        raise SystemExit()
    except ValueError:
        print('Retry if Invalid API calls are raised. It might be caused by faulty connection'
              ' or unresponsive server. Or change retries in TimeSeries to a greater number.')
        raise SystemExit()

if __name__ == '__main__':
    main()