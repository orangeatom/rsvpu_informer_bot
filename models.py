"""this module contain models to this bot"""
from peewee import *
from config import LOCALBASE

localbase = LOCALBASE


class User(Model):
    """this model contain user data"""
    state = IntegerField(default=0)
    state_data = CharField(null=True)
    sub_news = IntegerField(default=0)
    sub_schedule = CharField(null=True)
    timeline_login = CharField(null=True)
    user_id = IntegerField(null=False, primary_key=True)
    last_action = DateField(null=True)
    number_of_queries = IntegerField(default=0)

    class Meta:
        database = localbase

