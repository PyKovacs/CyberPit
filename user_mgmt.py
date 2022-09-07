
from getpass import getpass
from db import DBHandler
import bcrypt

class UserHandler:
    def __init__(self) -> None:
        self.db_handle = DBHandler()

    def new_user(self):
        username = input('Enter username for new user: ')
        while self.db_handle.user_exists('users', username):
                username = input(f'\nUser with name {username} already exists.\n'
                                  'Choose a different username: ')
        password = self.set_password()
        self.db_handle.create_user('users', username, password)
        return username

    def existing_user(self, name):
        while not self.db_handle.user_exists('users', name):
            name = input(f'User with name "{name}" does not exist.\n' 
                          'Enter your username: ')
        access = False
        while not access:
            access = bcrypt.checkpw(getpass().encode('utf-8'), 
                                    self.db_handle.get_pwdhash('users', name))
            if not access:
                print('Wrong password!')

    def set_password(self):
        pwd, confirm = "0", "1"
        pwd = str(getpass('Enter password for new user: '))
        confirm = str(getpass('Confirm the password for new user: '))
        if pwd != confirm:
            print('Passwords does not match!\n')
            self.set_password()
        del confirm
        return self.get_hash(pwd)

    def user_prompt(self):
        username = input('If you have a user, enter you username, otherwise press Enter to create a user:\n')
        if username:
            self.existing_user(username)
        else:
            username = self.new_user()
        self.db_handle.wq()
        return username

    def get_hash(self, string: str):
        bytes = string.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes, salt)
