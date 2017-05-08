"""this module contain models to this bot"""
from peewee import *
from telegram_bot import localbase


class User(Model):
    uid = CharField(unique=True)
    state = IntegerField()
    state_data = CharField()
    subscription = CharField()
    timeline_login = CharField()
    timeline_pass = CharField()
    news = IntegerField()
    last_action = DateTimeField()
    number_of_queries = IntegerField()

    class Meta:
        localbase


class GroupFullDay(Model):
    group_name = CharField(unique=True)
    group_id = CharField(null=True)

    class Meta:
        database = localbase


class GroupHalfDay(Model):
    group_name = CharField(unique=True)
    group_id = CharField(null=True)

    class Meta:
        database = localbase


class Teacher(Model):
    teacher_name = CharField(unique=True)
    teacher_id = IntegerField(null=True)

    class Meta:
        database = localbase
