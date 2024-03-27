import random
import string
def genrate():
    """generates a password for the user"""
    password = ''.join(random.choices(
        string.ascii_letters + string.digits, k=20))
    return password
