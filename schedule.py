"""this module send query to ScheduleDB to get Schedule"""

import pymssql
from config import ScheduleDatabase
import sql
import datetime
import time
import re

connect = pymssql.connect(server='127.0.0.1',
                          password=ScheduleDatabase.pwd,
                          database=ScheduleDatabase.dbname,
                          user=ScheduleDatabase.user,
                          )

FormOfEducation = {4: 'bachelor_full_day',
                   5: 'half_day',
                   6: 'master'}

primary_schedule_time = ('1️⃣ 08:00',
                         '2️⃣ 09:45',
                         '3️⃣ 12:00',
                         '4️⃣ 13:45',
                         '5️⃣ 15:30',
                         '6️⃣ 17:15',
                         '7️⃣ 19:00')


senior_schedule_time = ('1️⃣ 08:00',
                        '2️⃣ 09:45',
                        '3️⃣ 11:30',
                        '4️⃣ 13:45',
                        '5️⃣ 15:30',
                        '6️⃣ 17:15',
                        '7️⃣ 19:00')

class DatabaseError(Exception):
    pass

class ScheduleType():
    group = 0
    teacher = 1
    auditorium = 2
    pass

class days():

    def tomorrow(self):
        """return datetime object with tomorrow """
        return datetime.timedelta(days=1) + datetime.date.today()


    def today(self):
        """return datetime object with today"""
        return datetime.date.today()


def _schedule_group_query(group_id, day):
    """return schedule for entered group and selected day"""
    cursor = connect.cursor()
    try:
        cursor.execute('select Course,FormOfEducation, Name from [Group] Where [Group].OID = {id}'.format(id=group_id))
        course = cursor.fetchone()
        print(course)
        if course is not None:

            cursor.execute(sql.schedule_group.format(date=day(), id =group_id))
            row = cursor.fetchone()
            while row:
                # get data from row
                print(row)
                print(row[0])
                row = cursor.fetchone()

    except:
        print('error')



def _schedule_teacher_query():
    cursor = connect.cursor()
    try:
        cursor.execute(sql.schedule_teacher.format(date=tomorrow(), id='156'))
        row = cursor.fetchone()
        while row:
            # get data from row
            print(row)
            print(row[0])
            row = cursor.fetchone()

    except:
        print('error')


def _schedule_auditorium_query():
    cursor = connect.cursor()
    try:
        cursor.execute(sql.schedule_auditorium.format(date=tomorrow(), id='156'))
        row = cursor.fetchone()
        while row:
            # get data from row
            print(row)
            print(row[0])
            row = cursor.fetchone()

    except:
        print('error')




def get_schedule(day):
    cursor = connect.cursor()
    try:
        b = 1/0
    except:
        raise DatabaseError
    connect.close()



def get_schedule_tomorrow():
    pass

def get_schedule_week():
    pass


def get_schedule_date(date):
    """"""


def get_teachers_of_subjects():
    """"""

def get_groups():
    """"""
    cursor = connect.cursor()
    cursor.execute("select Name from [Group] ")



def get_teachers():
    """"""
    cursor = connect.cursor()
    cursor.execute("select Name from [Lecturer] ")

def get_auditorium():
    """"""
    cursor = connect.cursor()
    cursor.execute("select Name from [Auditorium]")


total = 0
count = 100
for timer in range(count):
        tt = time.time()
        get_groups()
        tt2 = time.time()
        total = total+(tt2-tt)


total=total/count
print(total)
connect.close()