#init
from flask import Flask, render_template, request
# from flask_bootstrap import Bootstrap
from StockTracking.backendserver.rss import rss
from StockTracking.backendserver import app
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g

@app.route('/', methods=['GET', 'POST'])
def start():
    print(123)
    return render_template('mainPage.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    print(456)
    return render_template('mainPage.html')


@app.route('/backend/get_news', methods=['GET', 'POST'])
def get_news():
    a = request.form.get('ticker')
    return rss.feed()



