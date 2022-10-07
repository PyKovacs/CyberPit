
from dataclasses import dataclass
from getpass import getpass
from typing import Tuple, Optional
import bcrypt
from time import sleep

from src.db import DBHandler
from src.robots import RobotBuilds, Robot
from src.utils import clear_console


@dataclass
class User:
    name: str
    db_handle: DBHandler
    robot: Optional[Robot] = None
    balance: int = 0
    
    def set_balance(self, balance: int, show: bool = True) -> None:
        '''
        Sets user balance to provided value. Writes to DB.
        Calls show_balance.
        show argument sets if balance is printed after update
        '''
        self.balance = balance
        self.db_handle.update_balance(self.name, self.balance)
        if show:
            print(self.get_balance())
        sleep(2)

    def get_balance(self, full: bool = True) -> str:
        '''
        Prints user balance statement.
        full argument sets if to return full statement,
        if False, returns only BTC value
        '''
        if full:
            return f'$$$ Current balance: {self.balance} BTC.'
        return f'{self.balance} BTC'
    
    def set_robot(self, robot: Robot) -> None:
        '''
        Assigns robot to a user. Writes to DB.
        '''
        self.robot = robot
        assert self.robot is not None
        self.db_handle.update_robot(self.name, self.robot.name)

    def get_btc(self, amount: int) -> None:
        '''
        Adds provided amount to balance. Calls set balance.
        '''
        print(f'$$$ {amount} BTC earned!')
        sleep(2)
        self.set_balance(self.balance + amount)

    def pay_btc(self, amount: int) -> bool:
        '''
        Subtracts provided amount from balance. Calls set balance.
        Returns bool (False if balance insufficient)
        '''
        if amount > self.balance:
            print('$$$ Insufficient funds :(')
            sleep(1)
            return False
        print(f'$$$ {amount} BTC paid.')
        sleep(1)
        self.set_balance(self.balance - amount)
        return True

    def purchase_robot(self) -> None:       # TODO refactor - maybe move to RobotBuilds
        '''
        Function for buying a new robot from the showcase.
        '''
        print('*** WELCOME TO TO ROBOT SHOP ***')
        print('Please, have a look on the finest selection.')
        print(self.get_balance())
        print(RobotBuilds._showcase())
        builds = tuple(RobotBuilds._get_all_names())
        while True:
            print('\nSelect a robot you wish to buy.')
            print(builds)
            print('(type "cancel" to return to main menu)')
            build_name = input('').capitalize()
            if build_name == 'Cancel':
                return
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


class PwdManager:
    def get_password(self) -> str:
        '''
        Prompts for new password using getpass. Returns hashed pwd.
        '''
        while True:
            pwd = str(getpass('Enter password for new user: '))
            confirm = str(getpass('Confirm the password for new user: '))
            if pwd != confirm:
                print('Passwords does not match!\n')
                sleep(2)
                continue
            break
        return self._get_hash(pwd)

    def eval_match(self, username: str, db_handle: DBHandler) -> bool:
        '''
        Asks for pwd and returns True if pwd match the one from DB
        '''
        return bcrypt.checkpw(getpass().encode('utf-8'),
                              db_handle.get_pwdhash(username))

    def _get_hash(self, string: str) -> str:
        '''
        Generates hash with salt. Using bcrypt.
        '''
        bytes = string.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes, salt)


class UserManager:
    def __init__(self, db_handler: DBHandler, pwd_manager: PwdManager) -> None:
        self.db_handle = db_handler
        self.pwd_manager = pwd_manager

    def read_username(self) -> User:
        '''
        Prompts for username. Calls new_user or existing_user func.
        Returns User object.
        '''
        while True:
            username = input('If you have a user, enter you username, '
                            'otherwise press Enter to create a user:\n')
            if not username:
                return self.create_new_user()
            if not self.db_handle.user_exists(username):
                print(f'User with name "{username}" does not exist.\n')
                sleep(.5)
                continue
            return self.load_existing_user(username)
            
    def create_new_user(self) -> User:
        '''
        Creates a new user + password. Writes to DB.
        Returns tuple of user object and bool (True as user is new).
        '''
        while True:
            username = str(input('Enter username for new user: '))
            if not username:
                print('Username invalid.')
                continue
            if self.db_handle.user_exists(username):
                print(f'User with name {username} already exists.')
                continue
            break
        password = self.pwd_manager.get_password()
        self.db_handle.create_user(username, password)
        user = User(username, self.db_handle)
        self.new_user_procedure(user)
        return user

    def load_existing_user(self, username: str) -> User:
        '''
        Authenticate existing user,
        instantiate user object from dict.

        Returns tuple of user object and bool (False as user is not new).
        '''
        access = False
        while not access:
            access = self.pwd_manager.eval_match(username, self.db_handle)
            if not access:
                print(':-(')
        print('<-- ACCESS GRANTED -->')
        sleep(1)
        user_data = self.db_handle.get_user_data(username)
        user = User._init_from_dict(user_data, self.db_handle)
        return user

    @staticmethod
    def new_user_procedure(user: User) -> None:
        '''
        Grants 500 BTC to balance, calls purchase robot func.
        Sequence to start if user is new.
        '''
        clear_console()
        print('It seems you are new here.')
        sleep(1)
        print('You were granted 500 bitcoins for a start, use them wisely!\n')
        user.set_balance(500, show=False)
        sleep(2)
        user.purchase_robot()
