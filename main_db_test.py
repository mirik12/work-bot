import sqlite3
import re

class DBHelper:
    def __init__(self, dbname = 'hours_notes.db'):
        self.db = sqlite3.connect(dbname)
        self.sql = self.db.cursor()

    def create_working_hours_table(self):
        sql_conn = """CREATE TABLE IF NOT EXISTS working_days (
            id BIGINT,
            date DATE,
            start_time TIME,
            end_time TIME,
            sum_work_hour TIME

        ) """
        self.sql.execute(sql_conn)
        self.db.commit()
        # self.create_table_for_push()


        # return self

    def create_add_to_table(self, id, date, start_time, end_time, sum_work_hour):
        self.sql.execute("INSERT INTO working_days VALUES(?, ?, ?, ?, ?);", (id, date, start_time, end_time, sum_work_hour))
        self.db.commit()

    def get_statistics_from_table(self, id, month):
        # res = self.sql.execute("SElECT id FROM working_days ").fetchall()
        # res = self.sql.execute("SELECT * FROM working_days where MONTH(`Date`) = MONTH(datetime('now')) and YEAR(`Date`) = YEAR(datetime('now'))")
        res = self.sql.execute("SElECT * FROM working_days WHERE id= " + str(id)).fetchall()
        self.db.commit()
        filter_list = []
        for item in res:
            date_month = item[1][3:5] # str[0:5] -> (item[1])[3:5]
            if date_month == str(month).zfill(2):  #- тут так же мы можем вместо date_month использовать сразу item[1][3:5]
                filter_list.append(item)
        print(filter_list)
        return filter_list

    def data_check(self, date):
        is_today = False
        write_list = self.sql.execute("SELECT DISTINCT date FROM working_days").fetchall()
        for item in write_list:
            if date == item[0]:
                is_today = True
        return is_today

    def this_month(self, date):
        list_of_days = self.sql.execute("SELECT * FROM id where MONTH(`Date`) = MONTH(NOW()) and YEAR(`Date`) = YEAR(NOW())")
        return list_of_days

    #####------- Table for PUSH----######

    def  create_table_for_push(self):
        sql_conn1 = """ CREATE TABLE IF NOT EXISTS table_push (
            id BIGINT,
            pushStatus BOOLEAN
            pushTime STRING
        )"""
        self.sql.execute(sql_conn1)
        self.db.commit()
        # self.add_to_create_table_for_push()
        # return self

    def add_user_to_push_table(self, id, status, push_time):
        if self.check_should_add_new_user(id):
            self.sql.execute("INSERT INTO table_push VALUES(?, ?, ?);", (id, status, push_time))
            self.db.commit()

    def update_user_push_status(self, id, pushStatus):
        self.sql.execute("UPDATE table_push SET pushStatus=? WHERE id=?", (pushStatus, id))
        self.db.commit()

        # return self

    def all_in_one_create_tables(self, id):
        self.create_working_hours_table()
        self.create_table_for_push()
        self.add_user_to_push_table(id, True, '20:00')
# calldb = DBHelper()
# mds = calldb.create_table().

    def get_push_status(self, id:str):
        result = self.sql.execute("SELECT * FROM table_push where id= " + str(id)).fetchone()
        result_bool = bool(result[1])
        return result_bool

    def check_should_add_new_user(self, id:int):
        result = self.sql.execute("SELECT id FROM table_push").fetchall()
        for item in result:
            if id == item[0]:
                return False
        return True






# user_login = input('Login: ')
# user_password = input('Password: ')
#
# sql.execute("SELECT login FROM userss")
# if sql.fetchone() is None:
#     #небезопасно
#     # sql.execute(f"INSERT INTO users VALUES ('{user_login}', '{user_password}', {0})")
#     # как делаем
#     sql.execute(f"INSERT INTO userss VALUES (?, ?, ?)", (user_login, user_password, 0))
#     db.commit()
# else:
#     print('Такая запись уже имеется!')
