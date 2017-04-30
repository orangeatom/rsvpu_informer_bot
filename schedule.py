"""this module send query to ScheduleDB to get Schedule"""

import pymssql
from config import ScheduleDatabase
import sql
import datetime
import time

connect = pymssql.connect(server='127.0.0.1',
                          password=ScheduleDatabase.pwd,
                          database=ScheduleDatabase.dbname,
                          user=ScheduleDatabase.user,
                          )


primary_schedule_time = ('1. 08:00',
                         '2. 09:45',
                         '3. 12:00',
                         '4. 13:45',
                         '5. 15:30',
                         '6. 17:15',
                         '7. 19:00')


senior_schedule_time = ('1. 08:00',
                        '2. 09:45',
                        '3. 11:30',
                        '4. 13:45',
                        '5. 15:30',
                        '6. 17:15',
                        '7. 19:00')



def _format_query_schedule_group(date):
    return sql.group.format()


class DatabaseError(Exception):
    pass


def schedule_group_query():


    cursor = connect.cursor()
    try:
        cursor.execute(sql.schedule_group.format(date=datetime.date(2017,4, 24), id ='1479'))
        row = cursor.fetchone()
        while row:
            # get data from row
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
    _format_query_schedule_group()


def get_schedule_week():
    pass


def get_schedule_date(date):
    """"""


def get_teachers_of_subjects():
    """"""



total = 0
count = 1
for timer in range(count):
        tt = time.time()
        schedule_group_query()
        tt2 = time.time()
        total = total+(tt2-tt)


total=total/count
print(total)