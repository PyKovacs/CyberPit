import sqlite3
from typing import Dict

DB_FILE = "data/main.db"


class DBHandler:
    def __init__(self):
        self.conn: sqlite3.Connection = sqlite3.connect(DB_FILE)
        if not self.table_exists('users'):
            if not self.create_users_table():
                print('ERROR: Failed creating users db table!')
                exit(5)

    def table_exists(self, table: str) -> bool:
        '''
        Return bool if table exists in db
        '''
        cursor = self.conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        return bool(cursor.fetchall())

    def create_users_table(self) -> bool:
        '''
        Creates users table.
        '''
        self.conn.execute('CREATE TABLE users (name TEXT PRIMARY KEY NOT NULL, '
                          'pwd BLOB NOT NULL, robot TEXT, balance INT);')
        self.conn.commit()
        return self.table_exists('users')

    def create_user(self, table: str, name: str, passwd: str, robot: str = '', balance: int = 0) -> None:
        '''
        Creates user row with provided values.
        '''
        try:
            self.conn.execute(f"INSERT INTO {table} VALUES ((?),(?),(?),(?))", (name, passwd, robot, balance))
            self.conn.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as emsg:
            print('ERROR: Crashed while creating user entry.')
            print(emsg)
            exit(5)

    def update_robot(self, table: str, user: str, robot: str) -> None:
        '''
        Updates the robot value for specific user.
        '''
        try:
            self.conn.execute(f"UPDATE {table} SET robot = '{robot}' WHERE name = '{user}'")
            self.conn.commit()
        except Exception as emsg:
            print('ERROR: Crashed while updating user entry.')
            print(emsg)
            exit(5)

    def update_balance(self, table: str, user: str, balance: int) -> None:
        '''
        Updates the balance value for specific user.
        '''
        try:
            self.conn.execute(f"UPDATE {table} SET balance = '{balance}' WHERE name = '{user}'")
            self.conn.commit()
        except Exception as emsg:
            print('ERROR: Crashed while updating user entry.')
            print(emsg)
            exit(5)

    def get_user_data(self, table: str, username: str) -> Dict[str,str]:
        '''
        Returns dict of user data from users table.
        '''
        columns = ['name', 'robot', 'balance']
        cursor = self.conn.execute(f"SELECT {', '.join(columns)} from {table} where name='{username}'")
        row = cursor.fetchall()
        data = {}
        for index, column in enumerate(columns):
            data[column] = row[0][index]
        return data

    def user_exists(self, table: str, name: str) -> bool:
        '''
        Returns True if user exists in users table.
        '''
        cursor = self.conn.execute(f"SELECT name from {table} where name='{name}'")
        return bool(cursor.fetchall())

    def get_pwdhash(self, table: str, name: str) -> bytes:  # TODO - set table default value to users, for each func in db handle, adjust all calls
        '''
        Returns pwd hash for specific user from specific table.
        '''
        cursor = self.conn.execute(f"SELECT pwd from {table} where name='{name}'")
        stored_pwd = cursor.fetchall()[0][0]
        return stored_pwd
