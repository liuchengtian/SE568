import csv
import os

def getData(sys):
    dirname = os.path.dirname(__file__)
    path = '/CSV/'+sys+'.csv'
    # print(dirname)
    f = open(dirname+path, 'r')
    csv_f = csv.reader(f)
    date = []
    Open = []
    High = []
    Low = []
    Close = []
    for row in csv_f:
        dateItem = row[0]
        openItem = float(row[1])
        highItewm = float(row[2])
        lowItem = float(row[3])
        closeItem = float(row[4])
        date.append(dateItem)
        Open.append(openItem)
        High.append(highItewm)
        Low.append(lowItem)
        Close.append(closeItem)
    # print data
    f.close()

    # define the json format
    data = dict()
    data['date'] = date
    data['open'] = Open
    data['high'] = High
    data['low'] = Low
    data['close'] = Close
    return data

# print(getData("AMZN"))
