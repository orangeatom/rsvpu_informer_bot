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
    query = ""


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


