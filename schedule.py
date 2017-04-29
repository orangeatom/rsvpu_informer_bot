"""this module send query to ScheduleDB to get Schedule"""

import pymssql
from config import ScheduleDatabase
import sql
import datetime

connect = pymssql.connect(server='127.0.0.1',
                          password=ScheduleDatabase.pwd,
                          database=ScheduleDatabase.dbname,
                          user=ScheduleDatabase.user,
                          )


def _get_schedule_group(date):
    return sql.group.format()


class DatabaseError(Exception):
    pass


def schedule_group_query():
    cursor = connect.cursor()
    try:
        strr = (sql.query_group.format(date=datetime.date(2017,4, 24), id ='1510'))
        cursor.execute(strr)
        print(2)
        row = cursor.fetchone()
        print(3)
        while row:
            print(4)
            print(row)
            row = cursor.fetchone()


    except:
        print('ahahahah')
    connect.close()


def schedule_teacher_query():
    pass


def schedule_auditorium_query():
    pass




def get_schedule_today():
    cursor = connect.cursor()
    try:
        b = 1/0
    except:
        raise DatabaseError
    connect.close()



def get_schedule_tomorrow():
    _get_schedule_group()


def get_schedule_week():
    pass


def get_schedule_date(date):
    pass


def get_teachers_of_subjects():
    pass



schedule_group_query()
