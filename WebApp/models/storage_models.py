from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker, relationship, backref, declarative_base
from models.extensions import login_manager
from flask_login import UserMixin

engine1 = create_engine('sqlite:///users.db')
engine2 = create_engine('sqlite:///user_credentials.db')
engine3 = create_engine('sqlite:///Secret-Guard.db')

Base1 = declarative_base()
Base2 = declarative_base()
Base3 = declarative_base()

session1 = sessionmaker(bind=engine1)()
session2 = sessionmaker(bind=engine2)()
session3 = sessionmaker(bind=engine3)()

class User(Base1, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

class Vault(Base2):
    __tablename__ = 'vault'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    username = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False)


class SecretGuard(Base3):
    __tablename__ = 'secret_guard'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(30), nullable=False)
    secret_key = Column(String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return session1.query(User).get(int(user_id))
