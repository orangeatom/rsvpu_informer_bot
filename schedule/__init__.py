"""this module send query to ScheduleDB to get Schedule"""
import datetime
import pymssql
from enum import Enum

import config
from schedule import sql

connect = pymssql.connect(server=config.SCHEDULEDB.server,
                          password=config.SCHEDULEDB.pwd,
                          database=config.SCHEDULEDB.db,
                          user=config.SCHEDULEDB.user,
                          )

cursor = connect.cursor(as_dict=True)

db_value_form_of_education = {'full day': '4, 6',
                              'half day': '5',
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


class EmptyGroupError(DatabaseError):
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


def __prepare_schedule_teacher(schedule):
    pass


def __do_query(query):
    cursor = connect.cursor(as_dict=True)
    cursor.execute(query)
    return cursor.fetchall()


def schedule_group_query(group_id, day):
    """return schedule for entered group and selected day"""
    group = __do_query(sql.select_group_name.format(id=group_id))
    try:
        if group:  # if database have this group
            return __do_query(sql.schedule_group.format(date=day, id=group_id))
        else:
            raise DatabaseError
        # todo error when group field is empty
    except:
        # todo make exception to db error
        print('something wrong')


def schedule_teacher_query(teacher_id, day):
    try:
        return __do_query(sql.schedule_teacher.format(date=day, id=teacher_id))
    except:
        print('error')


def schedule_classroom_query(classroom_id, day):
    # todo change sql query
    try:
        return __do_query(sql.schedule_auditorium.format(date=day, id=classroom_id))
    except:
        print('error')


def get_groups(group_substr=None, id=None, form_of_education=db_value_form_of_education['half day']):
    """return all groups or only the matching with math substr or set group id"""
    # fixme need query for a list of groups

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
    if teacher_substr is None:
        return __do_query(sql.select_all_teachers)
    else:
        return __do_query(sql.selection_teachers_by_name.format(teacher_substr))


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


