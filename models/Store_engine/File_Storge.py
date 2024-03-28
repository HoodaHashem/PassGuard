import json
from models.encryption import Encryption
from models.hashgen import HashGen

class File_Storage:
    """This class is responsible for storing and retrieving data from the json file."""

    __path = "data.json"
    __secret = "secret.json"
    __objects = {}
    __secret_objects = {}

    def load_data(self):
        """Load the data from the file"""
        try:
            with open(File_Storage.__path, "r") as file:
                File_Storage.__objects = json.load(file)
        except:
            return False

    def load_secret_data(self):
        """Load the secret data from the file"""

        try:
            with open(File_Storage.__secret, "r") as secret_file:
                File_Storage.__secret_objects = json.load(secret_file)
        except:
            return False


    def save_user(self, UserName, PassWord):
        """Save The UserName And Pass For The User"""

        inst = Encryption()
        Key = inst.create_key(PassWord)
        hashed_lock = HashGen()
        hashed_lock.update(Key)
        hashed_lock = hashed_lock.hexdigest()
        Usr, Pw = inst.encrypt_user_data(Key, UserName, PassWord)
        File_Storage.__objects[Usr.decode()+"@"+Pw.decode()+"@"+hashed_lock] = {}
        File_Storage.__secret_objects[hashed_lock] = Key.decode()
        with open(File_Storage.__path, "w") as file:
            json.dump(File_Storage.__objects, file)
        with open(File_Storage.__secret, "w") as secret_file:
            json.dump(File_Storage.__secret_objects, secret_file)


    def check_for_user(self, UserName):
        """Check if the user exists"""

        if self.load_data() == False:
            return False
        if self.load_secret_data() == False:
            return False
        for i in File_Storage.__objects.keys():
            Usr, Pw, hash = i.split("@")
            for x in File_Storage.__secret_objects.keys():
                if hash == x:
                    inst = Encryption()
                    master_key = File_Storage.__secret_objects[x]
                    username = inst.decrypt_user(master_key.encode(), Usr.encode())
                    if username == UserName:
                        return True
        return False

    def check_for_pass(self, PassWord, UserName):
        """Check if the password is correct"""

        if self.load_data() == False:
            return "No Users Found"
        if self.load_secret_data() == False:
            return "No Users Found"
        for i in File_Storage.__objects.keys():
            Usr, Pw, hash = i.split("@")
            for x in File_Storage.__secret_objects.keys():
                if hash == x:
                    inst = Encryption()
                    master_key = File_Storage.__secret_objects[x]
                    username, password = inst.decrypt_user_data(master_key.encode(), Usr.encode(), Pw.encode())
                    if username == UserName and password == PassWord:
                        return True
        return False

    def delete_user(self, UserName):
        """Delete the user"""

        if self.load_data() == False:
            return "No Users Found"
        if self.load_secret_data() == False:
            return "No Users Found"
        for i in File_Storage.__objects.keys():
            Usr, Pw, hash = i.split("@")
            for x in File_Storage.__secret_objects.keys():
                if hash == x:
                    inst = Encryption()
                    master_key = File_Storage.__secret_objects[x]
                    username, password = inst.decrypt_user_data(master_key.encode(), Usr.encode(), Pw.encode())
                    if username == UserName:
                        del File_Storage.__objects[i]
                        del File_Storage.__secret_objects[x]
                        with open(File_Storage.__path, "w") as file:
                            json.dump(File_Storage.__objects, file)
                        with open(File_Storage.__secret, "w") as secret_file:
                            json.dump(File_Storage.__secret_objects, secret_file)
                        return True
        return False

    def add_data(self, UserName, URL, Password, PassWord):
        """Add data to the user"""

        if self.load_data() == False:
            return "No Users Found"
        if self.load_secret_data() == False:
            return "No Users Found"
        for i in File_Storage.__objects.keys():
            Usr, Pw, hash = i.split("@")
            for x in File_Storage.__secret_objects.keys():
                if hash == x:
                    inst = Encryption()
                    master_key = File_Storage.__secret_objects[x]
                    username, password = inst.decrypt_user_data(master_key.encode(), Usr.encode(), Pw.encode())
                    if username == UserName and password == PassWord:
                        url, password = inst.encrypt_passwords(master_key.encode(), URL, Password)
                        File_Storage.__objects[i][url.decode()] = password.decode()
                        with open(File_Storage.__path, "w") as file:
                            json.dump(File_Storage.__objects, file)

    def all_passes(self, UserName, PassWord):
        """Get all the passwords"""

        lst = []
        if self.load_data() == False:
            return "No Users Found"
        if self.load_secret_data() == False:
            return "No Users Found"
        else:
            inst = Encryption()
            for keys, values in File_Storage.__objects.items():
                user, password, hash = keys.split("@")
                master_key = File_Storage.__secret_objects[hash]
                r_user, r_password = inst.decrypt_user_data(master_key.encode(), user.encode(), password.encode())
                if r_user == UserName and r_password == PassWord:
                    for i in values.keys():
                        url ,password = inst.decrypt_passwords(master_key.encode(), i.encode(), values[i].encode())
                        lst.append(f"URL: {url} Password: {password}")
        return lst

    def check_for_url(self, UserName, URL, PassWord):
        """Check if the URL exists"""

        if self.load_data() == False:
            return "No Users Found"
        if self.load_secret_data() == False:
            return "No Users Found"
        else:
            inst = Encryption()
            for keys, values in File_Storage.__objects.items():
                user, password, hash = keys.split("@")
                master_key = File_Storage.__secret_objects[hash]
                r_user, r_password = inst.decrypt_user_data(master_key.encode(), user.encode(), password.encode())
                if r_user == UserName and r_password == PassWord:
                    for i in values.keys():
                        url, password = inst.decrypt_passwords(master_key.encode(), i.encode(), values[i].encode())
                        if url == URL:
                            return True
        return False

    def delete_data(self, UserName, URL, PassWord):
        """Delete the data"""

        if self.load_data() == False:
            return "No Users Found"
        if self.load_secret_data() == False:
            return "No Users Found"
        if self.check_for_url(UserName, URL, PassWord) == False:
            return "No URL Found"
        else:
            inst = Encryption()
            for keys, values in File_Storage.__objects.items():
                user, password, hash = keys.split("@")
                master_key = File_Storage.__secret_objects[hash]
                r_user, r_password = inst.decrypt_user_data(master_key.encode(), user.encode(), password.encode())
                if r_user == UserName and r_password == PassWord:
                    for i in values.keys():
                        url, password = inst.decrypt_passwords(master_key.encode(), i.encode(), values[i].encode())
                        if url == URL:
                            del File_Storage.__objects[keys][i]
                            with open(File_Storage.__path, "w") as file:
                                json.dump(File_Storage.__objects, file)

    def update_pass(self, UserName, URL, Password, PassWord):
        """Update the password"""

        if self.load_data() == False:
            return "No Users Found"
        if self.load_secret_data() == False:
            return "No Users Found"
        else:
            inst = Encryption()
            for keys, values in File_Storage.__objects.items():
                user, password, hash = keys.split("@")
                master_key = File_Storage.__secret_objects[hash]
                r_user, r_password = inst.decrypt_user_data(master_key.encode(), user.encode(), password.encode())
                if r_user == UserName and r_password == PassWord:
                    for i in values.keys():
                        url, password = inst.decrypt_passwords(master_key.encode(), i.encode(), values[i].encode())
                        if url == URL:
                            url, password = inst.encrypt_passwords(master_key.encode(), URL, Password)
                            File_Storage.__objects[keys][i] = password.decode()
                            with open(File_Storage.__path, "w") as file:
                                json.dump(File_Storage.__objects, file)

#################### test cases ####################
# test = File_Storage()
# test.save_user("test", "test")
# test.add_data("test", "test", "facebook", "test")
# test.add_data("test", "test", "twitter", "test")
# test.add_data("test", "test", "instagram", "test")
# print(test.all_passes("test", "test"))
# print("=============================================")
# test2 = File_Storage()
# test2.save_user("test2", "test2")
# test2.add_data("test2", "test2", "lichess", "test2")
# test2.add_data("test2", "test2", "chess.com", "test2")
# test2.add_data("test2", "test2", "chess24", "test2")
# test2.all_passes("test2", "test2")
# print("=============================================")
# test3 = File_Storage()
# test3.save_user("test3", "test3")
# test3.add_data("test3", "test3", "google", "test3")
# test3.add_data("test3", "test3", "youtube", "test3")
# test3.add_data("test3", "test3", "gmail", "test3")
# test3.all_passes("test3", "test3")

# test.update_data("test", "instagram", "instagram", "test")
# test.all_passes("test", "test")

# test.delete_data("test", "twitter", "test")
# test.all_passes("test", "test")

# print(test.check_for_url("test", "sdff", "test"))
