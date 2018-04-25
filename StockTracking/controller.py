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
from .backendserver.rss import rss
from .backendserver.data import read_file, query_info


app = Flask(__name__, template_folder='templates', static_folder='static')

Bootstrap(app)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.column(db.String(15))
    email = db.column(db.String(50))
    password = db.column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=4, max=15)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index1.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index1.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                logout_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password!</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been created!</h1>'

    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    print('in stock')
    return render_template('mainPage.html')


@app.route('/stock?ticker=<ticker_id>', methods=['GET', 'POST'])
def stock_with_id(ticker_id):
    print("have ticker name:", ticker_id)
    return render_template('mainPage.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('userPage.html')


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


@app.route('/backend/get_prediction', methods=['GET', "POST"])
def get_prediction():
    ticker = request.form.get('ticker')
    interval = request.form.get('interval')
    query_info.function(ticker, interval)
    return
