"""this module send query to ScheduleDB to get Schedule"""
import datetime
import pymssql
from enum import Enum
import config
from schedule_db import sql

pair_time = (
    28800,
    35100,
    41400,
    43200,
    49500,
    55800,
    62100,
    68400, )

_connect = pymssql.connect(server=config.SCHEDULEDB.server,
                           password=config.SCHEDULEDB.pwd,
                           database=config.SCHEDULEDB.db,
                           user=config.SCHEDULEDB.user)

_cursor = _connect.cursor(as_dict=True)

_db_value_form_of_education = {'full day': '4, 6',
                               'half day': '5, 6',
                               'all': '4, 5, 6'}


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
    def tomorrow(self) -> datetime:
        dt = datetime.date(2017, 3, 15)
        """return datetime object with tomorrow """
        return datetime.date.today() + datetime.timedelta(days=1)

    @classmethod
    def today(self) -> datetime:
        """return datetime object with today"""
        dt = datetime.date(2017, 3, 15)
        return datetime.date.today()

    @classmethod
    def days_from_today(self, days: int) -> list:
        dates = []

        for day in range(days):
            dates.append(datetime.date.today() + datetime.timedelta(days=day))
        return dates


def _do_query(query) -> list:
    cursor = _connect.cursor(as_dict=True)
    cursor.execute(query)
    return cursor.fetchall()


def schedule_group_query(group_id: int, day) -> dict:
    """return schedule_db for entered group and selected day"""
    group = _do_query(sql.select_group_name.format(id=group_id))
    try:
        if group:  # if database have this group
            pairs = _do_query(sql.schedule_group.format(date=day, id=group_id))
            schedule = {}
            for pair in pair_time:
                schedule[pair] = tuple(s for s in pairs if s['start_time'] == pair)
            return schedule
        else:
            raise DatabaseError
        # todo error when group field is empty
    except:
        # todo make exception to db error
        print('something wrong')


def schedule_teacher_query(teacher_id: int, day) -> dict:
    """return teachers schedule to today"""
    try:
        pairs = _do_query(sql.schedule_teacher.format(date=day, id=teacher_id))
        schedule = {}
        for pair in pair_time:
            schedule[pair] = tuple(s for s in pairs if s['start_time'] == pair)
        return schedule
    except:
        print('error')


def schedule_classroom_query(classroom_id, day) -> dict:
    """return slassrooms schedule to today"""
    try:
        pairs = _do_query(sql.schedule_classroom.format(date=day, id=classroom_id))
        schedule = {}
        for pair in pair_time:
            schedule[pair] = tuple(s for s in pairs if s['start_time'] == pair)
        return schedule
    except:
        print('error')


def get_groups(group_substr=None, id=None, form_of_education=_db_value_form_of_education['all']) -> list:
    """return all groups or only the matching with math substr or set group id"""
    groups = _do_query(sql.select_groups.format(form_of_education))
    result = []
    if group_substr:
        for gr in groups:
            gr_part1, gr_part2 = gr['group_name'].split('-')
            if gr_part1.lower() in group_substr.lower() \
                    and gr_part2.lower() in group_substr.lower() \
                    and len(group_substr) <= len(gr['group_name']):
                result.append(gr)
            elif group_substr.lower() in gr_part1.lower() and len(group_substr) <= len(gr_part1):
                result.append(gr)
            elif group_substr.lower() in gr_part2.lower() and len(group_substr) <= len(gr_part2):
                result.append(gr)
    elif id:
        result = [gr for gr in groups if gr["group_id"] == id]
    return result


def get_teachers(teacher_substr=None, id=None):
    """return all teachers or only the matching with math substr"""
    if teacher_substr:
        teachers = _do_query(sql.select_all_teachers)
        found_teachers = []
        for t in teachers:
            if teacher_substr.lower() in t['fullname'].lower():
                found_teachers.append(t)
        return found_teachers
    elif id:
        teachers = _do_query(sql.select_all_teachers)
        found_teachers = []
        for t in teachers:
            if id == t['teacher_id']:
                found_teachers.append(t)
        return found_teachers
    else:
        return _do_query(sql.select_all_teachers)


def get_classrooms(classroom_substr=None):
    """return all classrooms or only the matching with math substr"""
    classrooms = _do_query(sql.select_classrooms)
    if classroom_substr:
        for classroom in classrooms:
            if classroom_substr == classroom['classroom_name']:
                return classroom
    return None


def lecturers_stream(stream_id: int) -> list:
    """:returns the list of groups integrated in this stream"""
    stream = _do_query(sql.lecturers_stream.format(stream_id=stream_id))
    stream_names = [gr['group'] for gr in stream]
    return stream_names


def get_groups_course(group_id):
    """return course of this group"""
    course = _do_query(sql.groups_course.format(group_id))
    return course[0]['Course']


def get_teachers_of_subjects():
    """this function return teacher/teachers whose teach this subject"""
