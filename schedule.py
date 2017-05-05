"""this module send query to ScheduleDB to get Schedule"""

from config import ScheduleDatabase
from enum import Enum
import pymssql
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


class ScheduleType(Enum):
    group = 0
    teacher = 1
    auditorium = 2


class Days:
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



def _schedule_teacher_query(teacher_id, day):
    cursor = connect.cursor()
    try:
        cursor.execute(sql.schedule_teacher.format(date=day, id=teacher_id))
        row = cursor.fetchone()
        while row:
            # get data from row
            print(row)
            print(row[0])
            row = cursor.fetchone()

    except:
        print('error')


def _schedule_classroom_query(classroom_id, day):
    cursor = connect.cursor()
    try:
        cursor.execute(sql.schedule_auditorium.format(date=day, id=classroom_id))
        row = cursor.fetchone()
        while row:
            # get data from row
            print(row)
            print(row[0])
            row = cursor.fetchone()

    except:
        print('error')


def get_teachers_of_subjects():
    """"""


def get_schedule(type, date, id):
    """this function return schedule in dictionary"""
    schedule = {}
    if type == ScheduleType.group:
        schedule = _schedule_group_query(id,date)
    elif type == ScheduleType.teacher:
        schedule = _schedule_teacher_query()
    elif type == ScheduleType.auditorium:
        schedule = _schedule_classroom_query()
    else:
        """generate error"""



def get_groups(group_substr = None):
    """return all groups or only the matching with math substr"""
    cursor = connect.cursor()
    if group_substr is None:
        cursor.execute("select Name from [Group] ")
    else:
        cursor.execute("select Name from [Group] Where Lower(Name) LIKE '%{0}%'".format(group_substr))
    raw = cursor.fetchone()
    groups = [raw]
    while raw:
        raw=cursor.fetchone()
        groups.append(raw)
    return groups


def get_teachers(teacher_substr = None):
    """return all teachers or only the matching with math substr"""
    cursor = connect.cursor()
    if teacher_substr is None:
        cursor.execute("select Name from [Lecturer]")
    else:
        cursor.execute("select Name from [Lecturer] where lower(Name) like '%{0}%'".format(teacher_substr))
    raw = cursor.fetchone()
    lecturers = [raw]
    while raw:
        raw = cursor.fetchone()
        lecturers.append(raw)
    return lecturers


def get_classrooms(group_substr = None):
    """return all classrooms or only the matching with math substr"""
    cursor = connect.cursor()
    if group_substr is None:
        cursor.execute("select Name from [Auditorium]")
    else:
        cursor.execute("select Name from [Auditorium] where lower(Name) like '%{0}%'".format(group_substr))
    raw = cursor.fetchone()
    classrooms = [raw]
    while raw:
        raw = cursor.fetchone()
        classrooms.append(raw)
    return classrooms


total = 0
count = 1
for timer in range(count):
        tt = time.time()
        print(get_classrooms('2-9'))

        tt2 = time.time()
        total = total+(tt2-tt)


total=total/count
print(total)
connect.close()