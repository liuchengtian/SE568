# init
from flask import Flask, render_template, request, redirect, url_for
from StockTracking.backendserver.rss import rss
from StockTracking.backendserver import app
from flask import request, render_template, jsonify
from StockTracking.backendserver.temple import readFile
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/Users/sunshuaishuai/SE568.database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager = init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.column(db.String(15), unique=True)
    email = db.column(db.String(50), unique=True)
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


@app.route('/')
def start():
    return render_template('mainPage.html')


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

    return render_template('signup .html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)