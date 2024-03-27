from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship



engine = create_engine('sqlite:///Guard.db')
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    credentials = relationship('UserCredentials', backref='user')

class UserCredentials(Base):
    __tablename__ = 'user_credentials'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    url_password = Column(String)
class DB_Storage:
    """Class to interact with the database to do CRUD operations"""

    def __init__(self):
        Base.metadata.create_all(engine)
        self.__session = sessionmaker(bind=engine)()

    def save_user(self, username, password):
        """Save a user to the database"""
        new_user = User(username=username, password=password)
        self.__session.add(new_user)
        self.__session.commit()

    def check_for_user(self, username):
        """Check if a user exists in the database"""
        user = self.__session.query(User).filter_by(username=username).first()
        if user:
            return True
        return False

    def check_for_pass(self, password, username):
        """Check if a password exists in the database"""
        user = self.__session.query(User).filter_by(username=username, password=password).first()
        if user:
            return True
        return False

    def delete_user(self, username):
        """Delete a user from the database by username"""
        user = self.__session.query(User).filter_by(username=username).first()
        if user:
            self.__session.delete(user)
            self.__session.commit()
            return True
        return False

    def all_users(self):
        """Return all the users in the database"""
        users = self.__session.query(User).all()
        return [user.username for user in users]

    def add_data(self, username, url, url_password, password):
        """addes a new password to the database"""
        user = self.__session.query(User).filter_by(username=username, password=password).first()
        if user:
            new_data = UserCredentials(user_id=user.id, url=url, url_password=url_password)
            self.__session.add(new_data)
            self.__session.commit()
            return True
        return False

    def all_passes(self, username, password):
        """Return all the passwords for a user"""
        user = self.__session.query(User).filter_by(username=username, password=password).first()
        if user:
            credentials = self.__session.query(UserCredentials).filter_by(user_id=user.id).all()
            return [(credential.url, credential.url_password) for credential in credentials]
        return False

    def update_data(self, username, url, url_password, password):
        """Update a password in the database"""
        user = self.__session.query(User).filter_by(username=username, password=password).first()
        if user:
            credential = self.__session.query(UserCredentials).filter_by(user_id=user.id, url=url).first()
            if credential:
                credential.url_password = url_password
                self.__session.commit()
                return True
        return False

    def delete_data(self, username, url, password):
        """Delete a password from the database"""
        user = self.__session.query(User).filter_by(username=username, password=password).first()
        if user:
            credential = self.__session.query(UserCredentials).filter_by(user_id=user.id, url=url).first()
            if credential:
                self.__session.delete(credential)
                self.__session.commit()
                return True
        return False
