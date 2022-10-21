import sqlite3
from typing import Dict

DB_FILE = "data/main.db"
USER_TABLE = 'users'


class DBHandler:
    def __init__(self):
        self.conn: sqlite3.Connection = sqlite3.connect(DB_FILE)
        if not self.table_exists(USER_TABLE) and not self.create_table():
            print('ERROR: Failed creating users db table!')
            exit(5)

    def table_exists(self, table: str) -> bool:
        '''
        Return bool if table exists in db
        '''
        cursor = self.conn.execute("SELECT name FROM sqlite_master "
                                   f"WHERE type='table' AND name='{table}';")
        return bool(cursor.fetchall())

    def create_table(self, table_name: str = USER_TABLE) -> bool:
        '''
        Creates table with predefined collumns in sqlite db.
        '''
        self.conn.execute(f'CREATE TABLE {table_name} (name TEXT PRIMARY KEY NOT NULL, '
                          'pwd BLOB NOT NULL, robot TEXT, robot_name TEXT, balance INT);')
        self.conn.commit()
        return self.table_exists(table_name)

    def create_user(self, name: str, passwd: str,
                    table: str = USER_TABLE) -> None:
        '''
        Creates user row with provided values.
        '''
        try:
            self.conn.execute(f"INSERT INTO {table} VALUES ((?),(?),(?),(?),(?))",
                              (name, passwd, '', '', 0))
            self.conn.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as emsg:
            print('ERROR: Crashed while creating user entry.')
            print(emsg)
            exit(5)

    def update_robot(self, user: str, robot: str, robot_name: str, table: str = USER_TABLE) -> None:
        '''
        Updates the robot value for specific user.
        '''
        try:
            self.conn.execute(f"UPDATE {table} SET robot = "
                              f"'{robot}' WHERE name = '{user}'")
            self.conn.execute(f"UPDATE {table} SET robot_name = "
                              f"'{robot_name}' WHERE name = '{user}'")
            self.conn.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as emsg:
            print('ERROR: Crashed while updating user entry.')
            print(emsg)
            exit(5)

    def update_balance(self, user: str, balance: int, table: str = USER_TABLE) -> None:
        '''
        Updates the balance value for specific user.
        '''
        try:
            self.conn.execute(f"UPDATE {table} SET balance = '{balance}' WHERE name = '{user}'")
            self.conn.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as emsg:
            print('ERROR: Crashed while updating user entry.')
            print(emsg)
            exit(5)

    def get_user_data(self, username: str, table: str = USER_TABLE) -> Dict[str,str]:
        '''
        Returns dict of user data from users table.
        '''
        columns = ['name', 'robot', 'robot_name', 'balance']
        cursor = self.conn.execute(f"SELECT {', '.join(columns)} from "
                                   f"{table} where name='{username}'")
        row = cursor.fetchall()
        data = {}
        for index, column in enumerate(columns):
            data[column] = row[0][index]
        return data

    def user_exists(self, name: str, table: str = USER_TABLE) -> bool:
        '''
        Returns True if user exists in users table.
        '''
        cursor = self.conn.execute(f"SELECT name from {table} where name='{name}'")
        return bool(cursor.fetchall())

    def get_pwdhash(self, name: str, table: str = USER_TABLE) -> bytes:
        '''
        Returns pwd hash for specific user from specific table.
        '''
        cursor = self.conn.execute(f"SELECT pwd from {table} where name='{name}'")
        stored_pwd = cursor.fetchall()[0][0]
        return stored_pwd
