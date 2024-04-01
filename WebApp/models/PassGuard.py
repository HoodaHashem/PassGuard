import string
import secrets

def generate_password(length=20, charset=string.ascii_letters + string.digits + string.punctuation):
    """Generates a secure password for the user."""
    password = ''.join(secrets.choice(charset) for _ in range(length))
    return password
