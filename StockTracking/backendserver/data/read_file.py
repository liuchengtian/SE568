import csv
import os
from StockTracking.backendserver.data import data_manager as DM

stockNameSet = ['AABA', 'AAPL', 'AMZN', 'BAC', 'FB', 'GOOGL', 'MSFT', 'NFLX', 'NKE', 'NVDA']


def getStock(sys):
    dirname = os.path.dirname(__file__)
    path = '/csv/'+sys+'_historical.csv'
    print(dirname)
    dm = DM.DataManager(dirname+path)
    typeSet = dm.column_names
    dataSet = dict()
    dateSet = []
    echartDataSet = []
    for item in typeSet:
        dataSet[item] = []
    lenSize, itemSize = dm.data.shape
    for i in range(100):
        dataItem = dm.data.iloc[i, :]
        dateSet.append(dataItem[0])
        for j in range(itemSize):
            dataSet[typeSet[j]].append(dataItem[j])
    print(dataSet)
    resultSet = dict()
    resultSet['typeName'] = typeSet
    print(resultSet['typeName'])
    resultSet['tableData'] = dataSet
    resultSet['date'] = dateSet
    for i in range(1,itemSize-2):
        echartItem = dict()
        echartItem['name'] = typeSet[i]
        echartItem['type'] = 'line'
        echartItem['smooth'] = True
        echartItem['data'] = dataSet[typeSet[i]]
        echartDataSet.append(echartItem)
    resultSet['echartData'] = echartDataSet
    return resultSet


def getStocks():
    dirname = os.path.dirname(__file__)
    resultSet = []
    typeSet = None
    result = dict()
    for item in stockNameSet:
        path = '/csv/'+item+'_realtime.csv'
        dm = DM.DataManager(dirname+path)
        dataItem = dict()
        typeSet = dm.column_names
        lenSize,itemSize = dm.data.shape
        tempItem = dm.data.iloc[0, :]
        for j in range(itemSize):
            dataItem[typeSet[j]]=tempItem[j]
        resultSet.append(dataItem)
    result['data'] = resultSet
    result['colName'] = typeSet
    return result


if __name__ == '__main__':
    print(getStock("AMZN"))
