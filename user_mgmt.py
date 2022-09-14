
from getpass import getpass
import bcrypt

from db import DBHandler
from dcs import User

class UserHandler:
    def __init__(self) -> None:
        self.db_handle = DBHandler()

    def load_user(self):
        username = input('If you have a user, enter you username, otherwise press Enter to create a user:\n')
        if username:
            username, new = self.existing_user(username)
        else:
            username = self.new_user()
            new = True
        user = User(username)
        self.db_handle.wq()
        return user, new

    def new_user(self):
        username = input('Enter username for new user: ')
        while not username:
            username = input('Username invalid, try again: ')
        while self.db_handle.user_exists('users', username):
            username = input(f'\nUser with name {username} already exists.\n'
                                'Choose a different username: ')
        password = self._set_password()
        self.db_handle.create_user('users', username, password)
        return username

    def existing_user(self, name):
        while not self.db_handle.user_exists('users', name):
            if name == '':
                return self.new_user(), True
            name = input(f'User with name "{name}" does not exist.\n' 
                          'Enter your username: ')
        access = False
        while not access:
            access = bcrypt.checkpw(getpass().encode('utf-8'), 
                                    self.db_handle.get_pwdhash('users', name))
            if not access:
                print(':-(')
        print('<-- ACCESS GRANTED -->')
        return name, False

    def _set_password(self):
        pwd = str(getpass('Enter password for new user: '))
        confirm = str(getpass('Confirm the password for new user: '))
        if pwd != confirm:
            print('Passwords does not match!\n')
            self._set_password()
        return self._get_hash(pwd)

    def _get_hash(self, string: str):
        bytes = string.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes, salt)
