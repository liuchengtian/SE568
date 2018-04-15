#init
from flask import Flask, render_template, request
# from flask_bootstrap import Bootstrap
from StockTracking.backendserver.rss import rss
from StockTracking.backendserver import app
from flask import request,render_template,jsonify

@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('mainPage.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('mainPage.html')


@app.route('/backend/get_news', methods=['GET', 'POST'])
def get_news():
    ticker = request.form.get('ticker')
    print(type(ticker))
    a =  rss.feed(ticker)
    return jsonify(a=a)



