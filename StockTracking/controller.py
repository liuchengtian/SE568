# init
from flask import Flask, render_template, request, redirect, url_for
from flask import request, render_template, jsonify
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import AnonymousUserMixin
import feedparser
import csv
import os


from StockTracking.backendserver.rss import rss
from StockTracking.backendserver.data import read_file,query_info

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
    #authenticated = db.Column(db.Boolean, default=False)

    def is_authenticated(self):
        """Check the user whether logged in."""

        # Check the User's instance whether Class AnonymousUserMixin's instance.
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True


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

@app.route('/backend/get_userId', methods=['GET', 'POST'])
def get_userId():
    if current_user.is_authenticated:
        userInfo = dict()
        userInfo['id'] = current_user.id
        userInfo['name'] = current_user.username
        print(userInfo)
        return jsonify(userInfo)
    else:
        print("in none")
        return None


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index1.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('start'))
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


def is_logined():
    if current_user.is_authenticated:
        return True
    return False


def user_info():
    return current_user


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('start'))


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    # print('in stock')
    return render_template('mainPage.html')


@app.route('/stock?ticker=<ticker_id>', methods=['GET', 'POST'])
def stock_with_id(ticker_id):
    print("have ticker name:", ticker_id)
    return render_template('mainPage.html')


@app.route('/user?ticker_id=<ticker_id>', methods=['GET', 'POST'])
def user(ticker_id):
    print("have ticker name")
    print(ticker_id)
    return redirect(url_for('start'))


# @app.route('/user', methods=['GET', 'POST'])
# def mainPage():
#     return render_template('userPage.html')


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    return render_template('result.html')


@app.route('/backend/get_stocks', methods=['GET', 'POST'])
def get_stocks():
    return jsonify(read_file.getStocks())


@app.route('/backend/get_news', methods=['GET', 'POST'])
def get_news():
    ticker = request.form.get('ticker')
    print('get news about ' + ticker)
    return jsonify(rss.feed(ticker))


@app.route('/backend/get_price', methods=['GET', 'POST'])
def get_price():
    ticker = request.form.get('ticker')
    print('get price about ' + ticker)
    return jsonify(read_file.getStock(ticker))


@app.route('/backend/get_rsi', methods=['GET', "POST"])
def get_rsi():
    ticker = request.form.get('ticker')
    time_type = request.form.get('time_type')
    from_time = request.form.get('from_time')
    to_time = request.form.get('to_time')
    data = query_info.query_info_rsi(ticker, time_type, from_time, to_time)
    date = query_info.query_info_date(from_time, to_time)
    assert(len(data) == len(date))
    result = {
        'rsi': data,
        'date': date
    }
    return jsonify(result)


@app.route('/backend/get_macd', methods=['GET', "POST"])
def get_macd():
    ticker = request.form.get('ticker')
    time_type = request.form.get('time_type')
    from_time = request.form.get('from_time')
    to_time = request.form.get('to_time')
    data = query_info.query_info_macd(ticker, time_type, from_time, to_time)
    MACD_Hist = data['MACD_Hist']
    MACD = data['MACD']
    MACD_Signal = data['MACD_Signal']
    date = query_info.query_info_date(from_time, to_time)
    assert(len(data) == len(date))
    result = {
        'MACD': MACD,
        'MACD_Signal': MACD_Signal,
        'MACD_Hist': MACD_Hist,
        'date': date
    }


@app.route('/backend/get_moving_avg', methods=['GET', "POST"])
def get_moving_avg():
    ticker = request.form.get('ticker')
    time_type = request.form.get('time_type')
    from_time = request.form.get('from_time')
    to_time = request.form.get('to_time')
    SMA = query_info.query_info_moving_avg(ticker, time_type, from_time, to_time)
    prices = query_info.query_info_close(ticker, time_type, from_time, to_time)
    date = query_info.query_info_date(ticker, time_type, from_time, to_time)
    print((SMA['SMA1']))
    print((SMA['SMA2']))
    print(len(date))
    print(len(prices))
    assert len(SMA['date1']) == len(SMA['date2']) == len(date) == len(prices)
    data = {
        'prices': prices,
        'SMA1': SMA['SMA1'],
        'SMA2': SMA['SMA2'],
        'date': date
    }
    return jsonify(data)


@app.route('/backend/get_neural_network', methods=['GET', "POST"])
def get_neural_network():
    ticker = request.form.get('ticker')
    time_type = request.form.get('time_type')
    from_time = request.form.get('from_time')
    to_time = request.form.get('to_time')
    data = query_info.query_info_neural_network(ticker, time_type, from_time, to_time)


@app.route('/backend/get_bayesian', methods=['GET', "POST"])
def get_bayesian():
    ticker = request.form.get('ticker')
    time_type = request.form.get('time_type')
    from_time = request.form.get('from_time')
    to_time = request.form.get('to_time')
    data = query_info.query_info_bayesian(ticker)
    return data


@app.route('/backend/get_svm', methods=['GET', "POST"])
def get_svm():
    ticker = request.form.get('ticker')
    time_type = request.form.get('time_type')
    from_time = request.form.get('from_time')
    to_time = request.form.get('to_time')
    data = query_info.query_info_svm(ticker)
    return data

