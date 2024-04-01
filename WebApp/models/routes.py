from flask import Flask, render_template, url_for, redirect, flash, request
from models.forms import RegistrationForm, LoginForm
from models.storage_models import Base1, Base2, Base3, engine1, engine2, engine3, User, Vault, SecretGuard
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
import hashlib
from flask_login import UserMixin, login_user, current_user, logout_user, login_required
from models.extensions import login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = '2a67f7d6ba6bb5c0e829e3a4f99237f7'

bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

Base1.metadata.create_all(engine1)
Base2.metadata.create_all(engine2)
Base3.metadata.create_all(engine3)

session1 = sessionmaker(bind=engine1)()
session2 = sessionmaker(bind=engine2)()
session3 = sessionmaker(bind=engine3)()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html' , footer=True)

@app.route('/Getintouch')
def Getintouch():
    return render_template('Getintouch.html' , footer=False)

@app.route('/about')
def about():
    return render_template('About.html' , footer=True)

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = hashlib.sha256(form.email.data.encode()).hexdigest()
        password = form.password.data
        user = session1.query(User).filter_by(email=email).first()
        if user and Bcrypt().check_password_hash(user.password, password):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html' , footer=False, form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = Bcrypt().generate_password_hash(form.password.data).decode('utf-8')
        username = hashlib.sha256(form.username.data.encode()).hexdigest()
        email = hashlib.sha256(form.email.data.encode()).hexdigest()
        user = User(username=username, email=email, password=hashed_password)
        session = sessionmaker(bind=engine1)()
        session.add(user)
        session.commit()
        flash(f"You'r Account Has Been Created! You'r now able to login.", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html' , footer=False, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html' , footer=True)
