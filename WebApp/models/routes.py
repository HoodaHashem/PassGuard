from flask import Flask, render_template, url_for, redirect, flash, request
from models.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateNewPassword, UpdatePassword, DeletePassword
from models.storage_models import Base1, Base2, Base3, engine1, engine2, engine3, User, Vault, SecretGuard
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
import hashlib
from flask_login import UserMixin, login_user, current_user, logout_user, login_required
from models.extensions import login_manager
from models.encryption import Encryption

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
        email = form.email.data
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
        username = form.username.data
        email = form.email.data
        inst = Encryption()
        key = inst.create_key(password=form.password.data)
        user = User(username=username, email=email, password=hashed_password)
        secret = SecretGuard(user_name=username, secret_key=key)
        session = sessionmaker(bind=engine1)()
        session2 = sessionmaker(bind=engine3)()
        session2.add(secret)
        session2.commit()
        session.add(user)
        session.commit()
        inst = Encryption()
        key = inst.create_key(form.password.data)
        secret = SecretGuard(user_name=username, secret_key=key)
        session3 = sessionmaker(bind=engine3)()
        session3.add(secret)
        session3.commit()
        flash(f"You'r Account Has Been Created! You'r now able to login.", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html' , footer=False, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user = session1.query(User).filter_by(id=current_user.id).first()
        user.username = hashlib.sha256(form.username.data.encode()).hexdigest()
        current_user.username = hashlib.sha256(form.username.data.encode()).hexdigest()
        current_user.email = hashlib.sha256(form.email.data.encode()).hexdigest()
        session1.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    count = session2.query(Vault).filter_by(username=current_user.username).count()
    if count > 1 or count == 0:
        flag = True
    else:
        flag = False
    return render_template('account.html' , footer=True, form=form, count=count, flag=flag)


@app.route('/create/new/password', methods=['GET', 'POST'])
@login_required
def create_password():
    form = CreateNewPassword()
    if form.validate_on_submit():
        inst = Encryption()
        key = session3.query(SecretGuard).filter_by(user_name=current_user.username).first().secret_key
        title = form.title.data
        password = form.password.data
        username = current_user.username
        url = form.URL.data
        email = form.email.data
        entitle = inst.encrypt_message(title, key)
        enpass = inst.encrypt_message(password, key)
        enurl = inst.encrypt_message(url, key)
        enemail = inst.encrypt_message(email, key)
        info = Vault(title=entitle, username=username, password=enpass, email=enemail, url=enurl)
        session2 = sessionmaker(bind=engine2)()
        session2.add(info)
        session2.commit()
        flash('Password has been created!', 'success')
        return redirect(url_for('account'))
    return render_template('create_password.html' , footer=True, form=form)


@app.route('/delete/password/', methods=['GET', 'POST'])
@login_required
def delete_password():
    form = DeletePassword()
    if form.validate_on_submit():
        url = form.URL.data
        password = form.password.data
        email = form.email.data
        key = session3.query(SecretGuard).filter_by(user_name=current_user.username).first().secret_key
        inst = Encryption()
        urls = session2.query(Vault).filter_by(username=current_user.username).all()
        for i in urls:
            if inst.decrypt_message(i.url, key) == url and inst.decrypt_message(i.email, key) == email and inst.decrypt_message(i.password, key) == password:
                session2.delete(i)
                session2.commit()
                break
            else:
                flash('Invalid Credentials!', 'danger')
                return redirect(url_for('delete_password'))
        flash('Password has been deleted!', 'success')
        return redirect(url_for('account'))
    return render_template('delete_password.html' , footer=True, form=form)

@app.route('/show/passwords/', methods=['GET', 'POST'])
@login_required
def show_passwords():
    passwords = session2.query(Vault).filter_by(username=current_user.username).all()
    inst = Encryption()
    key = session3.query(SecretGuard).filter_by(user_name=current_user.username).first().secret_key
    return render_template('show_passwords.html' , footer=True, key=key, passwords=passwords, inst=inst)

@app.route('/update/password/', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePassword()
    if form.validate_on_submit():
        title = form.title.data
        password = form.password.data
        email = form.email.data
        url = form.URL.data
        key = session3.query(SecretGuard).filter_by(user_name=current_user.username).first().secret_key
        inst = Encryption()
        urls = session2.query(Vault).filter_by(username=current_user.username).all()
        for i in urls:
            if inst.decrypt_message(i.url, key) == url:
                i.title = inst.encrypt_message(title, key)
                i.password = inst.encrypt_message(password, key)
                i.email = inst.encrypt_message(email, key)
                session2.commit()
                break
            else:
                flash('Invalid Credentials!', 'danger')
                return redirect(url_for('update_password'))
        flash('Password has been updated!', 'success')
        return redirect(url_for('account'))
    return render_template('update_password.html' , footer=True, form=form)
