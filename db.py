import sqlite3

DB_FILE = "data/main.db"

class DBHandler:
    def __init__(self):
        self.conn: sqlite3.Connection = sqlite3.connect(DB_FILE)
        if not self.table_exists('users'):
            if not self.create_users_table():
                print('ERROR: Failed creating users db table!')
                exit(5)

    def table_exists(self, table) -> bool:
        '''
        Return bool if table exists in db
        '''
        cursor = self.conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        return bool(cursor.fetchall())

    def create_users_table(self):
        cursor = self.conn.execute(' CREATE TABLE users (name TEXT PRIMARY KEY NOT NULL, pwd BLOB NOT NULL);')
        return self.table_exists('users')

    def create_user(self, table, name, passwd):
        try:
            pwd_to_store = memoryview(passwd)

            self.conn.execute(f"INSERT INTO {table} VALUES ((?),(?))", (name, passwd,))
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as emsg: 
            print('ERROR: Crashed while creating user entry.')
            print(emsg)
            exit(5)

    def user_exists(self, table, name):
        cursor = self.conn.execute(f"SELECT name from {table} where name='{name}'")
        return bool(cursor.fetchall())

    def get_pwdhash(self, table, name) -> bytes:
        cursor = self.conn.execute(f"SELECT pwd from {table} where name='{name}'")
        stored_pwd = cursor.fetchall()[0][0]
        return stored_pwd

    def wq(self):
        self.conn.commit()
        self.conn.close()

'''
conn.execute("INSERT INTO users VALUES (1, 'dave','123' )")
cursor = conn.execute("SELECT * from users where name='dave'")
'''