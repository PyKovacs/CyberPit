
from dataclasses import dataclass
from getpass import getpass
from typing import Tuple, Optional
import bcrypt
from time import sleep

from db import DBHandler
from robots import RobotBuilds, Robot


@dataclass
class User:
    name: str
    db_handle: DBHandler
    robot: Optional[Robot] = None
    balance: int = 0
    

    def set_balance(self, balance: int) -> None:
        '''
        Sets user balance to provided value. Writes to DB.
        Calls show_balance.
        '''
        self.balance = balance
        self.db_handle.update_balance('users', self.name, self.balance)
        self.show_balance()
        sleep(2)

    def show_balance(self) -> None:
        '''
        Prints user balance statement.
        '''
        print(f' $$$ Current balance: {self.balance} BTC. $$$')

    
    def set_robot(self, robot: Robot) -> None:
        '''
        Assigns robot to a user. Writes to DB.
        '''
        self.robot = robot
        assert self.robot is not None
        self.db_handle.update_robot('users', self.name, self.robot.name)

    def get_btc(self, amount: int) -> None:
        '''
        Adds provided amount to balance. Calls set balance.
        '''
        print(f' $$$ {amount} BTC earned! $$$')
        sleep(2)
        self.set_balance(self.balance + amount)

    def pay_btc(self, amount: int) -> bool:
        '''
        Subtracts provided amount from balance. Calls set balance.
        Returns bool (False if balance insufficient)
        '''
        if amount > self.balance:
            print(' $$$ Insufficient funds :( $$$')
            sleep(2)
            return False
        print(f' $$$ {amount} BTC paid. $$$')
        sleep(2)
        self.set_balance(self.balance - amount)
        return True

    def purchase_robot(self) -> None:
        '''
        Function for buying a new robot from the showcase.
        '''
        print(RobotBuilds._showcase())
        self.show_balance()
        builds = tuple(RobotBuilds._get_all_names())
        while True:
            build_name = input('\nSelect a robot you wish to buy:\n'
                          f'{builds}\n').capitalize()
            if build_name not in builds:
                print(f'  -> {build_name} is not valid robot build.')
                sleep(2)
                continue
            build = RobotBuilds._get_build_obj(build_name)
            if not self.pay_btc(build.cost):
                continue
            else:
                break
        self.set_robot(build)
        assert self.robot is not None, 'Failed to assign a robot.'
        # asserted here to avoid mypy error on line below
        print(f'You got yourself a new robot: {self.robot.name} !')

    @staticmethod
    def _init_from_dict(dict, db_handle: DBHandler) -> 'User':
        '''
        Reads the dictionary (provided by DB) and instantiate a user
        based on dict values.
        '''
        try:
            return User(dict['name'], db_handle, RobotBuilds._get_build_obj(dict['robot']), dict['balance'])
        except KeyError:
            print('Failed to initiate a user from dictionary')
            exit(2)

class UserHandler:
    def __init__(self, db_handler: DBHandler) -> None:
        self.db_handle = db_handler

    def user_login(self) -> Tuple[User, bool]:
        '''
        Prompts for username.
        Returns tuple of user object and bool (True if user is new).
        '''
        username = input('If you have a user, enter you username, '
                         'otherwise press Enter to create a user:\n')
        if username:
            return self.existing_user(username)
        return self.new_user()

    def new_user(self) -> Tuple[User, bool]:
        '''
        Creates a new user + password. Writes to DB.
        Returns tuple of user object and bool (True as user is new).
        '''
        username = input('Enter username for new user: ')
        while not username:
            username = input('Username invalid, try again: ')
        while self.db_handle.user_exists('users', username):
            username = input(f'\nUser with name {username} already exists.\n'
                             'Choose a different username: ')
        password = self._set_password()
        self.db_handle.create_user('users', username, password)
        user = User(username, self.db_handle)
        return user, True

    def existing_user(self, username: str) -> Tuple[User, bool]:
        '''
        Authenticate existing user,
        instantiate user object from dict.

        Returns tuple of user object and bool (True if user is new).
        '''
        while not self.db_handle.user_exists('users', username):    # TODO - refactor - move the self.new_user elsewhere so this func is for existing users only
            if username == '':
                return self.new_user()
            username = input(f'User with name "{username}" does not exist.\n'
                         'Enter your username: ')
        access = False
        while not access:
            access = bcrypt.checkpw(getpass().encode('utf-8'),
                                    self.db_handle.get_pwdhash('users', username))
            if not access:
                print(':-(')
                sleep(2)
        print('<-- ACCESS GRANTED -->')
        sleep(4)
        user_data = self.db_handle.get_user_data('users', username)
        user = User._init_from_dict(user_data, self.db_handle)
        return user, False

    def _set_password(self) -> str:
        '''
        Prompts for new password using getpass.
        '''
        pwd = str(getpass('Enter password for new user: '))     # TODO - use while
        confirm = str(getpass('Confirm the password for new user: '))
        if pwd != confirm:
            print('Passwords does not match!\n')
            sleep(2)
            self._set_password()
        return self._get_hash(pwd)

    def _get_hash(self, string: str) -> str:
        '''
        Generates hash with salt. Using bcrypt.
        '''
        bytes = string.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes, salt)


def new_user_sequence(user: User) -> None:
    '''
    Grants 500 BTC to balance, calls purchase robot func.
    Sequence to start if user is new.
    '''
    print('It seems you are new here.')
    sleep(2)
    print('You were granted 500 bitcoins for a start, use them wisely!\n')
    user.set_balance(500)
    sleep(3)
    user.purchase_robot()
