from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class Encryption:
    """Encryption class for encrypting and decrypting data"""


    def create_key(self, password):
        """Create a key from the password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))


    def encrypt_key(self, key):
        """Encrypt the key"""
        cipher_suite = Fernet(key)
        encrypted_key = cipher_suite.encrypt(key)
        return encrypted_key

    def decrypt_key(self, key, encrypted_key):
        """Decrypt the key"""
        cipher_suite = Fernet(key)
        decrypted_key = cipher_suite.decrypt(encrypted_key)
        return decrypted_key

    def encrypt_user_data(self, key, username, password):
        """Encrypt the user data"""
        cipher_suite = Fernet(key)
        encrypted_username = cipher_suite.encrypt(username.encode())
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_username, encrypted_password

    def decrypt_user_data(self, key, encrypted_username, encrypted_password):
        """Decrypt the user data"""
        cipher_suite = Fernet(key)
        decrypted_username = cipher_suite.decrypt(encrypted_username).decode()
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_username, decrypted_password

    def decrypt_user(self, key, encrypted_user):
        """Decrypt the user"""
        cipher_suite = Fernet(key)
        decrypted_user = cipher_suite.decrypt(encrypted_user).decode()
        return decrypted_user


    def encrypt_user_password(self, key, password):
        """Encrypt the password"""
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def encrypt_passwords(self, key, url, password):
        """Encrypt the passwords"""
        cipher_suite = Fernet(key)
        encrypted_url = cipher_suite.encrypt(url.encode())
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_url, encrypted_password

    def decrypt_passwords(self, key, encrypted_url, encrypted_password):
        """Decrypt the passwords"""
        cipher_suite = Fernet(key)
        decrypted_url = cipher_suite.decrypt(encrypted_url).decode()
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_url, decrypted_password


    def decrypt_password(self, key, encrypted_password):
        """Decrypt the password"""
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_password

    def encrypt_user(self, key, user):
        """Encrypt the user"""
        cipher_suite = Fernet(key)
        encrypted_user = cipher_suite.encrypt(user.encode())
        return encrypted_user
