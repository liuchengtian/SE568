# init
from flask import Flask, render_template, request
# from flask_bootstrap import Bootstrap
from StockTracking.backendserver.rss import rss
from StockTracking.backendserver import app
from flask import request, render_template, jsonify
from StockTracking.backendserver.data import read_file


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('mainPage.html')


@app.route('/?ticker=<ticker_id>', methods=['GET', 'POST'])
def user(ticker_id):
    print(ticker_id)
    return render_template('mainPage.html')


@app.route('/user', methods=['GET', 'POST'])
def index():
    return render_template('userPage.html')

@app.route('/backend/get_news', methods=['GET', 'POST'])
def get_news():
    ticker = request.form.get('ticker')
    print('get news about ' + ticker)
    return jsonify(rss.feed(ticker))


@app.route('/backend/get_price', methods=['GET', 'POST'])
def get_price():
    ticker = request.form.get('ticker')
    print('get price about ' + ticker)
    return jsonify(read_file.getData(ticker))


@app.route('/backend/query_info', methods=['GET', 'POST'])
def query_info():
    pass
