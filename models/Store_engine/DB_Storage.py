from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker



engine = create_engine('sqlite:///Guard.db')
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

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


