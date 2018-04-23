# init
from flask import Flask, render_template, request
#from flask_bootstrap import Bootstrap
from StockTracking.backendserver.rss import rss
from StockTracking.backendserver import app
from flask import request, render_template, jsonify
from StockTracking.backendserver.temple import readFile
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

app = Flask
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')




@app.route('/')
def start():
    return render_template('mainPage.html')


@app.route('/login')
def login():
    form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/ticker=<ticker_id>', methods=['GET', 'POST'])
def index(ticker_id):
    print(ticker_id)
    return render_template('mainPage.html')


@app.route('/backend/get_news', methods=['GET', 'POST'])
def get_news():
    ticker = request.form.get('ticker')
    print('get news about ' + ticker)
    return jsonify(rss.feed(ticker))


@app.route('/backend/get_price', methods=['GET', 'POST'])
def get_price():
    ticker = request.form.get('ticker')
    print('get price about ' + ticker)
    return jsonify(readFile.getData(ticker))


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

