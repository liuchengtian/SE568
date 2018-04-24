# init
from flask import Flask, render_template, request, redirect, url_for
#from StockTracking.backendserver.rss import rss
from flask import request, render_template, jsonify
# from StockTracking.backendserver.data import read_file
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
import feedparser
import csv
import os


app = Flask(__name__, template_folder='templates', static_folder='static')

Bootstrap(app)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=4, max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index1.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            #if user.password == form.password.data:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('user', ticker_id=user.id))

        return '<h1>Invalid username or password!</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been created!</h1>'

    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('start'))


@app.route('/?ticker=<ticker_id>', methods=['GET', 'POST'])
def user(ticker_id):
    print(ticker_id)
    return render_template('mainPage.html', name='Welcome, ' + current_user.username)


@app.route('/user', methods=['GET', 'POST'])
def index():
    return render_template('userPage.html')


@app.route('/backend/get_news', methods=['GET', 'POST'])
def get_news():
    ticker = request.form.get('ticker')
    print('get news about ' + ticker)
    return jsonify(feed(ticker))


@app.route('/backend/get_price', methods=['GET', 'POST'])
def get_price():
    ticker = request.form.get('ticker')
    print('get price about ' + ticker)
    return jsonify(getData(ticker))


@app.route('/backend/query_info', methods=['GET', 'POST'])
def query_info():
    pass


def feed(ticker: str):
    rss_url = 'http://finance.yahoo.com/rss/headline?s=' + ticker
    # get rss
    feeds = feedparser.parse(rss_url)
    rss = dict()
    # get version of rss
    # print(feeds.version)

    # get http head
    # print(feeds.headers)
    # print(feeds.headers.get('Content-Type'))

    # rss title
    rss['title'] = feeds['feed']['title']
    # rss link
    rss['link'] = feeds['feed']['link']
    # rss subtitle
    rss['sub title'] = feeds['feed']['subtitle']
    # number of articles
    print(feeds)
    n = len(feeds['entries'])
    rss['number'] = n
    rss['article'] = [dict() for i in range(n)]

    for i in range(n):
        rss['article'][i]['index'] = i
        rss['article'][i]['title'] = feeds['entries'][i]['title']
        rss['article'][i]['link'] = feeds['entries'][i]['link']
        rss['article'][i]['date'] = feeds['entries'][i]['published_parsed']
        rss['article'][i]['summary'] = feeds['entries'][i]['summary']

    return rss


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


# if __name__ == '__main__':
#     print(getData("AMZN_historical"))
#
#
# if __name__ == '__main__':
#     print(feed('AMZN'))