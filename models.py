"""this module contain models to this bot"""
from peewee import *
from config import LOCALBASE

localbase = LOCALBASE

class User(Model):
    last_action = DateTimeField(null=True)
    news = IntegerField(null=True)
    number_of_queries = IntegerField(null=True)
    timeline_login = CharField(null=True)
    timeline_pass = CharField(null=True)
    uid = CharField(unique=True)
    state = IntegerField(default=0)
    state_data = CharField(null=True)
    subscription = CharField(null=True)

    class Meta:
        database = localbase


class GroupFullDay(Model):
    # FIXME delete it after getting query groups
    group_name = CharField(unique=True)
    group_id = CharField(null=True)

    class Meta:
        database = localbase


class GroupHalfDay(Model):
    # FIXME delete it after getting query groups
    group_name = CharField(unique=True)
    group_id = CharField(null=True)

    class Meta:
        database = localbase


class Teacher(Model):
    # FIXME delete it after getting query groups
    teacher_name = CharField(unique=True)
    teacher_id = IntegerField(null=True)

    class Meta:
        database = localbase
