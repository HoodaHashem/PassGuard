from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


class Encryption:
    

    def create_key(self, password):
        """Create a key from the password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_username(self, key, username):
        """Encrypt the username"""
        f = Fernet(key)
        return f.encrypt(username.encode())

    def decrypt_username(self, key, username):
        """Decrypt the username"""
        f = Fernet(key)
        return f.decrypt(username).decode()

    def encrypt_email(self, key, email):
        """Encrypt the email"""
        f = Fernet(key)
        return f.encrypt(email.encode())

    def decrypt_email(self, key, email):
        """Decrypt the email"""
        f = Fernet(key)
        return f.decrypt(email).decode()
