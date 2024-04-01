from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import hashlib
from models.storage_models import User
from sqlalchemy.orm import sessionmaker
from models.storage_models import Base1, Base2, Base3, engine1, engine2, engine3, User, Vault, SecretGuard


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
        username = hashlib.sha256(username.data.encode()).hexdigest()
        user = session1.query(User).filter_by(username=username).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = hashlib.sha256(email.data.encode()).hexdigest()
        email = session1.query(User).filter_by(email=email).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
