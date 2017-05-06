"""this module contain models to this bot"""
from peewee import *
from config import localbase


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



