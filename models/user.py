from models import storage

class User():
    """User model for creating user objects and storing user data"""

    def new_user(self, username, password):
        """Create a new user object"""
        self.username = username
        self.password = password
        storage.save_user(self.username, self.password)
