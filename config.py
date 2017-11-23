"""this module contain configure data to this bot"""
import os
from collections import namedtuple
from peewee import SqliteDatabase


TOKEN = os.environ['TOKEN_BOT']

__ScheduleDB = namedtuple('ScheduleDB', ['server', 'user', 'pwd', 'db'])

SCHEDULEDB = __ScheduleDB('localhost',  # fixme
                          os.environ['SCHEDULE_DB_USER'],
                          os.environ['SCHEDULE_DB_PASS'],
                          os.environ['SCHEDULE_DB'])

LOCALBASE = SqliteDatabase('base.db')
