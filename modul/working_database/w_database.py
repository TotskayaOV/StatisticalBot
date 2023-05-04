import sqlite3


class DataBase:
    def __init__(self, db_path: str = './cred/work_db.db'):
        self.db_path = db_path

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS user 
        (id INTEGER PRIMARY KEY, name TEXT, role TEXT)'''
        self.execute(sql, commit=True)

    def create_table_call(self):
        sql = '''CREATE TABLE IF NOT EXISTS call 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME, user INTEGER, count INTEGER)'''
        self.execute(sql, commit=True)

    # def create_table_portal(self):
    #     sql = '''CREATE TABLE IF NOT EXISTS portal
    #      (id INTEGER PRIMARY KEY AUTOINCREMENT,
    #       date DATETIME, user INTEGER, verif INTEGER, check INTEGER)'''
    #     self.execute(sql, commit=True)

    def create_table_portal(self):
        sql = '''CREATE TABLE IF NOT EXISTS portal 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME, user INTEGER, verif INTEGER)'''
        self.execute(sql, commit=True)

    def create_table_jira_count(self):
        sql = '''CREATE TABLE IF NOT EXISTS jira_count 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME, user INTEGER, count INTEGER)'''
        self.execute(sql, commit=True)

    def create_table_jira_sla(self):
        sql = '''CREATE TABLE IF NOT EXISTS jira_sla 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME, user INTEGER, sla FLOAT)'''
        self.execute(sql, commit=True)

    def create_table_jira_time(self):
        sql = '''CREATE TABLE IF NOT EXISTS jira_time 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME, user INTEGER, time TEXT)'''
        self.execute(sql, commit=True)

    def create_table_general_data(self):
        sql = '''CREATE TABLE IF NOT EXISTS general_data 
        (date DATETIME PRIMARY KEY,
        new INTEGER, fast INTEGER)'''
        self.execute(sql, commit=True)

    def add_user(self, user_data: dict):
        parameters = (user_data.get('id'), user_data.get('name'), user_data.get('role'))
        sql = '''INSERT INTO user (id, name, role) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_call(self, call_data: dict):
        parameters = (call_data.get('date'), call_data.get('user'), call_data.get('count'))
        sql = '''INSERT INTO call (date, user, count) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_portal(self, portal_data: dict):
        parameters = (portal_data.get('date'), portal_data.get('user'),
                      portal_data.get('verif'))
        sql = '''INSERT INTO portal (date, user, verif) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_jira_count(self, jira_data: dict):
        parameters = (jira_data.get('date'), jira_data.get('user'), jira_data.get('count'))
        sql = '''INSERT INTO jira_count (date, user, count) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_jira_sla(self, jira_data: dict):
        parameters = (jira_data.get('date'), jira_data.get('user'), jira_data.get('sla'))
        sql = '''INSERT INTO jira_sla (date, user, sla) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_jira_time(self, jira_data: dict):
        parameters = (jira_data.get('date'), jira_data.get('user'), jira_data.get('time'))
        sql = '''INSERT INTO jira_time (date, user, time) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_general(self, general_data: dict):
        parameters = (general_data.get('date'), general_data.get('new'), general_data.get('fast'))
        sql = '''INSERT INTO general_data (date, new, fast) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def update_portal(self, new_data: dict):
        parameters = (new_data.get('verif'), new_data.get('id'))
        sql = '''UPDATE portal SET verif=? WHERE id=? '''
        self.execute(sql, parameters, commit=True)

    def update_general(self, new_data: dict):
        parameters = (new_data.get('new'), new_data.get('fast'), new_data.get('date'))
        sql = '''UPDATE portal SET new=?, fast=? WHERE date=? '''
        self.execute(sql, parameters, commit=True)

    def update_user(self, new_data: dict):
        parameters = (new_data.get('role'), new_data.get('id'))
        sql = '''UPDATE user SET role=? WHERE id=? '''
        self.execute(sql, parameters, commit=True)

    def get_user(self):
        sql = '''SELECT * FROM user'''
        return self.execute(sql, fetchall=True)

    def get_the_user(self, **kwargs):
        sql = '''SELECT * FROM user WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def get_call(self, **kwargs):
        sql = '''SELECT * FROM call WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_portal(self, id_user):
        parameters = (id_user, )
        sql = '''SELECT * FROM portal WHERE user=?'''
        return self.execute(sql, parameters, fetchall=True)

    def get_date_portal(self, date):
        parameters = (date, )
        sql = '''SELECT * FROM portal WHERE date=?'''
        return self.execute(sql, parameters, fetchall=True)

    def get_jira_count(self, **kwargs):
        sql = '''SELECT * FROM jira_count WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_jira_sla(self, **kwargs):
        sql = '''SELECT * FROM jira_sla WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_jira_time(self, **kwargs):
        sql = '''SELECT * FROM jira_time WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_general(self, date):
        parameters = (date, )
        sql = '''SELECT * FROM general_data WHERE date=?'''
        return self.execute(sql, parameters, fetchall=True)

    def remove_user(self, id_user: int):
        parameters = (id_user,)
        sql = '''DELETE FROM user WHERE user_id=?'''
        self.execute(sql, parameters, commit=True)


    def remove_general(self, date):
        parameters = (date,)
        sql = '''DELETE FROM general_data WHERE date=?'''
        self.execute(sql, parameters, commit=True)

    def remove_call(self, date):
        parameters = (date,)
        sql = '''DELETE FROM call WHERE date=?'''
        self.execute(sql, parameters, commit=True)

    @staticmethod
    def extract_kwargs(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())


    def disconnect(self):
        self.connection.close()
