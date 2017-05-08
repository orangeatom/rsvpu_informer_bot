"""this module send query to ScheduleDB to get Schedule"""

from enum import Enum
import config
import pymssql
import sql
import datetime
import os
import time

connect = pymssql.connect(server=config.SCHEDULEDB.server,
                          password=config.SCHEDULEDB.pwd,
                          database=config.SCHEDULEDB.db,
                          user=config.SCHEDULEDB.user,
                          )

db_value_form_of_education = {'full day': '4, 6',
                              'half day': 5,
                              }

pair_time = {
    28800: '1️⃣ 08:00',
    35100: '2️⃣ 09:45',
    41400: '3️⃣ 11:30',
    43200: '3️⃣ 12:00',
    49500: '4️⃣ 13:45',
    55800: '5️⃣ 15:30',
    62100: '6️⃣ 17:15',
    68400: '7️⃣ 19:00'
}


class DatabaseError(Exception):
    pass


class ScheduleType(Enum):
    group = 0
    teacher = 1
    auditorium = 2


class Days:
    @classmethod
    def tomorrow(self):
        """return datetime object with tomorrow """
        return datetime.date.today() + datetime.timedelta(days=1)

    @classmethod
    def today(self):
        """return datetime object with today"""
        return datetime.date.today()


def __prepare_schedule(schedule):
    """:return dictionary with schedule in format ready to send in bot module"""
    formatet_schedule = {}
    for pair in pair_time:
        if schedule['start_time'] in pair:
            print('methot one')
    pass


def _schedule_group_query(group_id, day):
    """return schedule for entered group and selected day"""
    cursor = connect.cursor(as_dict=True)
    try:
        cursor.execute('select Name from [Group] Where [Group].OID = {id}'.format(id=group_id))
        course = cursor.fetchone()
        schedule = {}
        print(course)
        if course:
            cursor.execute(sql.schedule_group.format(date=day, id=group_id))
            row = cursor.fetchone()
            while row:
                # get data from row
                row = cursor.fetchone()
        else:
            pass
            # todo error when group field is empty

    except:
        print('error')


def _schedule_teacher_query(teacher_id, day):
    cursor = connect.cursor(as_dict=True)
    try:
        cursor.execute(sql.schedule_teacher.format(date=day, id=teacher_id))
        row = cursor.fetchone()
        while row:
            # get data from row
            row = cursor.fetchone()

    except:
        print('error')


def _schedule_classroom_query(classroom_id, day):
    # todo change sql query
    cursor = connect.cursor(as_dict=True)
    try:
        cursor.execute(sql.schedule_auditorium.format(date=day, id=classroom_id))
        row = cursor.fetchone()
        print(row)
        while row:
            # get data from row
            row = cursor.fetchone()
            print(row)

    except:
        print('error')


def get_schedule(type, date, id):
    """this function return schedule in dictionary"""
    schedule = {}
    if type == ScheduleType.group:
        schedule = _schedule_group_query(id,date)
    elif type == ScheduleType.teacher:
        schedule = _schedule_teacher_query(id,date)
    elif type == ScheduleType.auditorium:
        schedule = _schedule_classroom_query(id,date)
    else:
        """generate error"""
    return schedule


def get_groups(group_substr=None, id=None, form_of_education=db_value_form_of_education['half day']):
    """return all groups or only the matching with math substr or set group id"""
    cursor = connect.cursor(as_dict=True)
    if group_substr:
        cursor.execute("select Name from [Group] Where Lower(Name) LIKE '%{0}%' and FormOfEducation in ({1}})"
                       .format(group_substr, form_of_education))
    elif id:
        cursor.execute("select Name from [Group] where OID = {0}".format(id))
    else:
        cursor.execute("select Name from [Group] where FormOfEducation in ({0})".format(form_of_education))

    raw = cursor.fetchone()
    groups = [raw['Name']]
    while raw:
        raw = cursor.fetchone()
        if raw:
            groups.append(raw['Name'])
    return groups


def get_teachers(teacher_substr=None):
    """return all teachers or only the matching with math substr"""
    cursor = connect.cursor()
    if teacher_substr is None:
        cursor.execute("select Name from [Lecturer]")
    else:
        cursor.execute("select Name from [Lecturer] where lower(Name) like '%{0}%'".format(teacher_substr))
    raw = cursor.fetchone()
    lecturers = [raw[0]]
    while raw:
        raw = cursor.fetchone()
        if raw:
            lecturers.append(raw[0])
    return lecturers


def get_classrooms(group_substr=None):
    """return all classrooms or only the matching with math substr"""
    cursor = connect.cursor()
    if group_substr is None:
        cursor.execute("select Name from [Auditorium]")
    else:
        cursor.execute("select Name from [Auditorium] where lower(Name) like '%{0}%'".format(group_substr))
    raw = cursor.fetchone()
    classrooms = [raw[0]]
    while raw:
        raw = cursor.fetchone()
        if raw:
            classrooms.append(raw[0])
    return classrooms


def get_teachers_of_subjects():
    """this function return teacher/teachers whose teach this subject"""


total = 0
count = 1

for timer in range(count):
        tt = time.time()
        # nice example to test group ID-107 with id = 1709 and date 05.08.17
        _schedule_group_query(1709, '05.08.17')
        print('teacher')
        print(_schedule_teacher_query(2050, '05.12.17'))
        print('classroom')
        _schedule_classroom_query(219, '05.12.17')
        print('endlcassroom')
        cur = connect.cursor()
        cur.execute(sql.lecturers_stream.format(stream_id=1753))
        raw = cur.fetchone()
        print(raw)
        while raw:
            raw = cur.fetchone()
            if raw:
                print(raw)
        print('gruop')
        print(len(get_groups()))
        tt2 = time.time()
        total = total+(tt2-tt)


total = total/count
print(total)
connect.close()
