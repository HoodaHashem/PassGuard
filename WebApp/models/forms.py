from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.storage_models import User
from sqlalchemy.orm import sessionmaker
from models.storage_models import Base1, Base2, Base3, engine1, engine2, engine3, User, Vault, SecretGuard
from flask_login import UserMixin, login_user, current_user, logout_user, login_required
import requests
from models.PassGuard import generate_password
from models.encryption import Encryption

session1 = sessionmaker(bind=engine1)()
session2 = sessionmaker(bind=engine2)()
session3 = sessionmaker(bind=engine3)()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        username = username.data
        user = session1.query(User).filter_by(username=username).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = email.data
        email = session1.query(User).filter_by(email=email).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_password(self, password):
        password = password.data
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not any(char in ['$', '@', '#', '%', '!', '&', '-', '_'] for char in password):
            raise ValidationError('Password must contain at least one special character.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        username = username.data
        if username != current_user.username:
            user = session1.query(User).filter_by(username=username).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = email.data
        if email != current_user.email:
            email = session1.query(User).filter_by(email=email).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')

class CreateNewPassword(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    URL = StringField('URL', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Create')

    def validate_URL(self, URL):
        url = URL.data
        if not url.startswith('http://') and not url.startswith('https://'):
            raise ValidationError('Invalid URL. Please include http:// or https://')
        if requests.get(url).status_code != 200:
            raise ValidationError('Invalid URL. Please enter a valid URL.')

    def recommend_password(self):
        recommended_password = generate_password()
        return recommended_password

class UpdatePassword(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    URL = StringField('URL', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_URL(self, URL):
        url = URL.data
        urls = session2.query(Vault).filter_by(username=current_user.username).all()
        lst = []
        inst = Encryption()
        key = session3.query(SecretGuard).filter_by(user_name=current_user.username).first().secret_key
        for i in urls:
            lst.append(inst.decrypt_message(i.url, key))
        if url not in lst:
            raise ValidationError('URL does not exist in your vault.')

class DeletePassword(FlaskForm):
    URL = StringField('URL', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Delete')

    def validate_URL(self, URL):
        url = URL.data
        urls = session2.query(Vault).filter_by(username=current_user.username).all()
        lst = []
        inst = Encryption()
        key = session3.query(SecretGuard).filter_by(user_name=current_user.username).first().secret_key
        for i in urls:
            lst.append(inst.decrypt_message(i.url, key))
        if url not in lst:
            raise ValidationError('URL does not exist in your vault.')

class SecretGuardForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Generate Secret Key')

    def validate_email(self, email):
        email = email.data
        user = session1.query(User).filter_by(email=email).first()
        if not user:
            raise ValidationError('Email does not exist. Please enter a valid email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        password = password.data
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not any(char in ['$', '@', '#', '%', '!', '&', '-', '_'] for char in password):
            raise ValidationError('Password must contain at least one special character.')
