"""logic of work with User"""
import datetime
from models import *
import json


class ScheduleType:
    Teacher = 0
    Group = 1


class EndUser:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.user, self.new = User.get_or_create(user_id=chat_id)

    def __increment_query(self):
        self.user.number_of_queries = self.user.number_of_queries+1

    def __update_last_action(self):
        self.user.last_action = datetime.datetime.now()

    # logging as action in db

    def set_state_data(self, data, **kwargs):
        self.user.state_data = json.dumps(data)
        self.__increment_query()
        self.__update_last_action()
        self.user.save()

    def create_user(self, user_id):
        user = User.get_or_create(user_id=user_id)
        self.__increment_query()
        self.__update_last_action()
        self.user.save()

    def set_state(self, state):
        self.user.state = state
        self.__increment_query()
        self.__update_last_action()
        self.user.save()

    # without logging

    def get_user(self):
        return User.get(user_id=self.chat_id)

    def get_state(self):
        return self.user.state

    def set_timeline(self, login):
        self.user.timeline_login = login
        self.user.save()

    def change_news(self):
        if self.user.sub_news == 0:
            self.user.sub_news = 1
        else:
            self.user.sub_news = 0
        self.user.save()

    def get_sub_news(self)-> bool:
        if self.user.sub_news == 0:
            sub = False
        else:
            sub = True
        return sub

    def set_sub_schedule(self, type, schedule_id):
        self.user.state_data = {}
        sub = json.dumps({'type': type, 'schedule_id': schedule_id})
        self.user.sub_schedule = sub
        self.user.save()

    def get_sub_schedule(self) -> dict:
        try:
            return json.loads(self.user.sub_schedule)
        except:
            return None

    def get_state_data(self) -> dict:
        if self.user.state_data:
            return json.loads(str(self.user.state_data))
        else:
            return {}

