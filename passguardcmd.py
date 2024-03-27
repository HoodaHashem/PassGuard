import cmd
from models.genpass import genrate
from models.user import User
from models import storage
class PassGuardCmd(cmd.Cmd):
    """Simple command line interpreter for PassGuard"""

    prompt = "PassGuard => "

    __username = None
    __password = None
    def do_EOF(self, arg):
        """Exit the command line interpreter."""
        print("Bye!")
        return True

    def emptyline(self) -> bool:
        """Do nothing on empty line."""
        return False

    do_quit = do_exit = do_EOF

    def do_genpass(self, arg):
        """Generate a new difficult password."""
        genrated_pass = genrate()
        print(f"Generated password: {genrated_pass}")

    def do_create_new_user(self, arg):
        """Create a new user."""
        while True:
            username = input("Enter username: ")
            if len(username) < 4:
                print("Username must be at least 4 characters long.")
                return
            if storage.check_for_user(username):
                print("User already exists!\nPlease enter a different username.")
            else:
                break
        genpass = input("Do you want to generate a password? (y/n): ")
        if genpass == "y":
            password = genrate()
            print(f"Generated password: {password}")
        else:
            password = input("Enter password: ")
            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                return
        user = User()
        user.new_user(username, password)
        print("User created successfully!")
        PassGuardCmd.__username = username
        PassGuardCmd.__password = password
        print("You are now logged in")

    def do_delete_user(self, arg):
        """Delete a user."""
        username = input("Enter username: ")
        if storage.check_for_user(username):
            password = input("Please provide the password to delete the user: ")
            if storage.check_for_pass(password, username):
                storage.delete_user(username)
                PassGuardCmd.__username = None
                PassGuardCmd.__password = None
                print("User deleted successfully!")
            else:
                print("Invalid password!")
        else:
            print("User not found!")

    def do_select_user(self, arg):
        """Select a user."""
        PassGuardCmd.__username = input("Enter username: ")
        PassGuardCmd.__password = input("Enter password: ")
        if storage.check_for_pass(PassGuardCmd.__password, PassGuardCmd.__username):
            print("User selected successfully!")
        else:
            print("Invalid username or password!")

    def do_logout(self, arg):
        """Log out the user."""
        PassGuardCmd.__username = None
        PassGuardCmd.__password = None
        print("Logged out successfully!")


    def do_add_new_pass(self, arg):
        """Add a new password."""
        if not PassGuardCmd.__username:
            print("Please select a user first or create a new user!")
            return
        url = input("Enter the URL: ")
        genpass = input("Do you want to generate a password? (y/n): ")
        if genpass == "y":
            url_password = genrate()
            print(f"Generated password: {url_password}")
        else:
            url_password = input("Enter the password: ")
        storage.add_data(PassGuardCmd.__username, url, url_password, PassGuardCmd.__password)
        print("Password added successfully!")

    def do_show_users(self, arg):
        """List all users."""
        users = storage.all_users()
        for user in users:
            print(user)

    def do_show_passes(self, arg):
        """List all passwords."""
        passes = storage.all_passes(PassGuardCmd.__username, PassGuardCmd.__password)
        if passes:
            print(passes)
        else:
            print("No passwords found!")

    def do_update_pass(self, arg):
        """Update a password."""
        if not PassGuardCmd.__username:
            print("Please select a user first or create a new user!")
            return
        url = input("Enter the URL: ")
        genpass = input("Do you want to generate a password? (y/n): ")
        if genpass == "y":
            url_password = genrate()
            print(f"Generated password: {url_password}")
        else:
            url_password = input("Enter the password: ")
        storage.update_data(PassGuardCmd.__username, url, url_password, PassGuardCmd.__password)
        print("Password updated successfully!")

    def do_delete_pass(self, arg):
        """Delete a password."""
        if not PassGuardCmd.__username:
            print("Please select a user first or create a new user!")
            return
        url = input("Enter the URL: ")
        storage.delete_data(PassGuardCmd.__username, url, PassGuardCmd.__password)
        print("Record deleted successfully!")

    def do_clear(self, arg):
        """Clear the screen."""
        print("\033c")
if __name__ == "__main__":
    PassGuardCmd().cmdloop()