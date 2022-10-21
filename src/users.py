from dataclasses import dataclass
from getpass import getpass
from time import sleep
from typing import Dict

import bcrypt  # type: ignore

from src.db import DBHandler
from src.robots import Robot, RobotManager, RobotShop
from src.utils import clear_console


@dataclass
class User:
    name: str
    db_handle: DBHandler
    robot: Robot = RobotManager().blank_build
    balance: int = 0

    @staticmethod
    def init_from_dict(user_data: Dict[str, str], db_handle: DBHandler, robot: Robot) -> 'User':
        '''
        Reads the dictionary (provided by DB) and instantiate a user
        based on dict values.
        '''
        try:
            return User(user_data['name'],
                        db_handle,
                        robot,
                        int(user_data['balance']))
        except KeyError:
            print('Failed to initiate a user from dictionary')
            exit(2)

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

    def get_balance_int(self) -> int:
        '''
        Prints user balance integer.
        '''
        return self.balance

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
        self.db_handle.update_robot(self.name, self.robot.build, self.robot.name)

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

    def buy_robot(self, robot_shop: RobotShop) -> None:
        '''
        Function for buying a new robot. 
        Enters robot shop, evaluate selection,
        pays for the robot and set the robot to the user.
        '''
        robot_build_data = robot_shop.select_build()
        if not robot_build_data:
            return
        while True:
            name = str(input('Name your robot: '))
            if len(name) not in range(1,16):
                print('Name must be 1 to 15 characters long.\n')
                sleep(.5)
                continue
            break

        robot = Robot(name, robot_build_data)
        self.pay_btc(robot.cost)
        self.set_robot(robot)
        sleep(2)


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
        bytes_string = string.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes_string, salt)


class UserManager:
    def __init__(self, db_handler: DBHandler, pwd_manager: PwdManager, robot_manager: RobotManager) -> None:
        self.db_handle = db_handler
        self.pwd_manager = pwd_manager
        self.robot_manager = robot_manager

    def read_username(self) -> User:
        '''
        Prompts for username. Calls new_user or existing_user func.
        Returns User object.
        '''
        while True:
            if not (username := input('If you have a user, enter you username, '
                            'otherwise press Enter to create a user:\n')):
                self.current_user = self.create_new_user()
                return self.current_user
            if not self.db_handle.user_exists(username):
                print(f'User with name "{username}" does not exist.\n')
                sleep(.5)
                continue

            self.current_user = self.load_existing_user(username)
            return self.current_user
            
    def create_new_user(self) -> User:
        '''
        Creates a new user + password. Writes to DB.
        Returns tuple of user object and bool (True as user is new).
        '''
        while True:
            if not (username := str(input('Enter username for new user: '))):
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
            if not (access := self.pwd_manager.eval_match(username, self.db_handle)):
                print(':-(')

        print('<-- ACCESS GRANTED -->')
        sleep(1)
        user_data = self.db_handle.get_user_data(username)      # TODO - fail to load when no robot at the start of game
        return User.init_from_dict(user_data,
            self.db_handle,
            Robot(user_data['robot_name'],
                  self.robot_manager.get_build_data(user_data['robot'])))

    def new_user_procedure(self, user: User) -> None:
        '''
        Grants starting BTC to balance, calls purchase robot func.
        Sequence to start if user is new.
        '''
        clear_console()
        print('It seems you are new here.')
        sleep(1)
        print('You were granted 300 bitcoins for a start, use them wisely!\n')
        user.set_balance(300, show=False)
        sleep(2)
        user.buy_robot(RobotShop(self.robot_manager, user.get_balance_int()))
