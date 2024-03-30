from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from models.encryption import Encryption
from models.hashgen import HashGen

engine1 = create_engine('sqlite:///Guard.db')
engine2 = create_engine('sqlite:///Secret-Guard.db')

Base1 = declarative_base()
Base2 = declarative_base()
class User(Base1):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    credentials = relationship('UserCredentials', backref='user')

class UserCredentials(Base1):
    __tablename__ = 'user_credentials'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    url_password = Column(String)

class UserSecrets(Base2):
    """Class to store user secrets"""
    __tablename__ = 'user_secrets'

    id = Column(Integer, primary_key=True)
    hash = Column(String)
    secret_key = Column(String)


class DB_Storage:
    """Class to interact with the database to do CRUD operations"""

    def __init__(self):
        Base1.metadata.create_all(engine1)
        Base2.metadata.create_all(engine2)
        self.__session1 = sessionmaker(bind=engine1)()
        self.__session2 = sessionmaker(bind=engine2)()

    def save_user(self, username, password):
        inst = Encryption()
        key = inst.create_key(password)
        UserName = HashGen()
        UserName.update(username.encode())
        hashed_username = UserName.hexdigest()
        PassWord = inst.encrypt_user_password(key, password)
        user = User(username=hashed_username, password=PassWord.decode())
        user_secret = UserSecrets(hash=hashed_username, secret_key=key)
        self.__session2.add(user_secret)
        self.__session1.add(user)
        self.__session2.commit()
        self.__session1.commit()

    def check_for_user(self, username):
        UserName = HashGen()
        UserName.update(username.encode())
        hashed_username = UserName.hexdigest()
        user = self.__session1.query(User).filter_by(username=hashed_username).first()
        if user:
            return True
        return False

    def check_for_pass(self, password, username):
        user_hash = HashGen()
        user_hash.update(username.encode())
        hashed_username = user_hash.hexdigest()
        user = self.__session1.query(User).filter_by(username=hashed_username).first()
        inst = Encryption()
        key = self.__session2.query(UserSecrets).filter_by(hash=hashed_username).first().secret_key
        PassWord = inst.decrypt_password(key, user.password.encode())
        if PassWord == password:
            return True
        return False

    def delete_user(self, username):
        UserName = HashGen()
        UserName.update(username.encode())
        hashed_username = UserName.hexdigest()
        user = self.__session1.query(User).filter_by(username=hashed_username).first()
        if user:
            self.__session1.delete(user)
            self.__session1.commit()
            return True
        return False

    def add_data(self, UserName, URL, Password, PassWord):
        """Method to add data to the database"""
        user_hash = HashGen()
        user_hash.update(UserName.encode())
        hashed_username = user_hash.hexdigest()
        user = self.__session1.query(User).filter_by(username=hashed_username).first()
        inst = Encryption()
        key = self.__session2.query(UserSecrets).filter_by(hash=hashed_username).first().secret_key
        url = inst.encrypt_user_password(key, URL)
        url_password = inst.encrypt_user_password(key, Password)
        user_credentials = UserCredentials(user_id=user.id, url=url.decode(), url_password=url_password.decode())
        self.__session1.add(user_credentials)
        self.__session1.commit()

    def all_passes(self, UserName, PassWord):
        """Method to list all passwords"""
        user_hash = HashGen()
        user_hash.update(UserName.encode())
        hashed_username = user_hash.hexdigest()
        user = self.__session1.query(User).filter_by(username=hashed_username).first()
        inst = Encryption()
        key = self.__session2.query(UserSecrets).filter_by(hash=hashed_username).first().secret_key
        user_credentials = self.__session1.query(UserCredentials).filter_by(user_id=user.id).all()
        if user_credentials:
            passes = []
            for cred in user_credentials:
                url, password = inst.decrypt_passwords(key, cred.url.encode(), cred.url_password.encode())
                passes.append(f"URL=> {url}, Password=> {password}")
            return passes
        return None

    def delete_data(self, UserName, URL, PassWord):
        """Method to delete data"""
        user_hash = HashGen()
        user_hash.update(UserName.encode())
        hashed_username = user_hash.hexdigest()
        user = self.__session1.query(User).filter_by(username=hashed_username).first()
        inst = Encryption()
        key = self.__session2.query(UserSecrets).filter_by(hash=hashed_username).first().secret_key
        user_credentials = self.__session1.query(UserCredentials).filter_by(user_id=user.id).all()
        for cred in user_credentials:
            url, password = inst.decrypt_passwords(key, cred.url.encode(), cred.url_password.encode())
            if url == URL and password == PassWord:
                self.__session1.delete(cred)
                self.__session1.commit()
                return True
        return False

    def update_pass(self, UserName, URL, Password, PassWord):
        """updates user credentials"""
        user_hash = HashGen()
        user_hash.update(UserName.encode())
        hashed_username = user_hash.hexdigest()
        user = self.__session1.query(User).filter_by(username=hashed_username).first()
        inst = Encryption()
        key = self.__session2.query(UserSecrets).filter_by(hash=hashed_username).first().secret_key
        user_credentials = self.__session1.query(UserCredentials).filter_by(user_id=user.id).all()
        for cred in user_credentials:
            url, password = inst.decrypt_passwords(key, cred.url.encode(), cred.url_password.encode())
            if url == URL:
                self.__session1.delete(cred)
                url = inst.encrypt_user_password(key, URL)
                url_password = inst.encrypt_user_password(key, Password)
                user_credentials = UserCredentials(user_id=user.id, url=url.decode(), url_password=url_password.decode())
                self.__session1.add(user_credentials)
                self.__session1.commit()
                return True
        return False

################## TESTING ##################
# test = DB_Storage()
# print(test.check_for_user('test'))
# test.save_user('test', 'test')
# print(test.check_for_user('test'))

# test2 = DB_Storage()
# if test2.check_for_user('test2'):
#     print('User found!')
# else:
#     print('User not found!')
#     test2.save_user('test2', 'test2')
# if test2.check_for_user('test2'):
#     print('User found!')

# print(test.check_for_pass('test1', 'test'))
# print(test.check_for_pass('test2', 'test2'))

# test.delete_user('test')
# print(test.check_for_user('test'))

# test.save_user('test', 'test')
# test.add_data('test', 'chess.com', 'passtest', 'test')
# print(test.all_passes('test', 'test'))

# print(test.delete_data('test', 'chess.com', 'passtest'))
# print(test.add_data('test', 'lichess.org', 'passtest', 'test'))
# print(test.all_passes('test', 'test'))
# print(test.delete_data('test', 'lichess.org', 'passtest'))
# print(test.all_passes('test', 'test'))
# test.update_pass('test', 'chess.com', 'all done!', 'test')
# print(test.all_passes('test', 'test'))
