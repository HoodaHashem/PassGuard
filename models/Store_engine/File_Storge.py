import json


class File_Storage:
    """This class is responsible for storing and retrieving data from the json file."""

    __path = "data.json"
    __objects = {}

    def load_data(self):
        """Load data from the json file"""
        try:
            with open(self.__path, "r") as file:
                self.__objects = json.load(file)
        except FileNotFoundError:
            return "database is not exist"

    def save_user(self, username, password):
        """Save user data to the json file"""
        self.__objects[username+'@'+password] = {}
        with open(self.__path, "w") as file:
            json.dump(self.__objects, file)

    def save_data(self, data):
        """Save data to the json file"""
        with open(self.__path, "w") as file:
            json.dump(data, file)
    def delete_user(self, username):
        """Delete user data from the json file"""
        File_Storage.load_data(self)
        for data in self.__objects.keys():
            user = data.split('@')[0]
            if user == username:
                del self.__objects[data]
                File_Storage.save_data(self, self.__objects)
                return True
        return False

    def check_for_user(self, username):
        """Check if user exists in the json file"""
        File_Storage.load_data(self)
        for data in self.__objects.keys():
            user = data.split('@')[0]
            if user == username:
                return True
        return False

    def check_for_pass(self, password, username):
        """Check if password exists in the json file"""
        File_Storage.load_data(self)
        for data in self.__objects.keys():
            user = data.split('@')[0]
            passw = data.split('@')[1]
            if user == username and passw == password:
                return True
        return False

    def add_data(self, username, url, url_password, username_password):
        """add the data into the file"""
        File_Storage.load_data(self)
        self.__objects[username+'@'+username_password][url] = url_password
        File_Storage.save_data(self, self.__objects)

    def all_users(self):
        """return all the users"""
        File_Storage.load_data(self)
        users = []
        for data in self.__objects.keys():
            user = data.split('@')[0]
            users.append(user)
        return users

    def all_passes(self, username, password):
        """return all the passwords"""
        File_Storage.load_data(self)
        for data in self.__objects.keys():
            user = data.split('@')[0]
            passw = data.split('@')[1]
            if user == username and passw == password:
                str = ""
                for key, value in self.__objects[data].items():
                    str += f"{key} : {value}\n"
                return str
        return False

    def update_data(self, username, url, url_password, username_password):
        """update the data into the file"""
        File_Storage.load_data(self)
        self.__objects[username+'@'+username_password][url] = url_password
        File_Storage.save_data(self, self.__objects)

    def delete_data(self, username, url, username_password):
        """delete the data into the file"""
        File_Storage.load_data(self)
        del self.__objects[username+'@'+username_password][url]
        File_Storage.save_data(self, self.__objects)
