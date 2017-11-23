"""this module contain models to this bot"""
from peewee import *

from config import LOCALBASE


class ChoiceField(IntegerField):
    def db_value(self, value):
        return self.choices.index(value)

    def python_value(self, value):
        return self.choices[value]


class User(Model):
    """this model contain user data"""
    state = IntegerField(default=0)  # todo make it choice field
    state_data = CharField(default='{}')
    sub_news = IntegerField(default=0)
    sub_schedule = CharField(null=True)
    timeline_login = CharField(null=True)
    chat_id = IntegerField()
    user_id = IntegerField(null=False, primary_key=True)
    last_action = DateField(null=True)
    number_of_queries = IntegerField(default=0)

    class Meta:
        database = LOCALBASE

