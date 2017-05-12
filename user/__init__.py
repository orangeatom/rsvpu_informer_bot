"""logic of work with User"""
import datetime
from models import *
import json


def __increment_query(id):
    user = User.get(user_id=id)
    user.number_of_queries = user.number_of_queries+1
    user.save()


def __update_last_action(id):
    user = User.get(user_id=id)
    user.last_action = datetime.datetime.now()
    user.save()


def user_action(func):
    def updates(*args, **kwargs):
        func(*args, **kwargs)
        __increment_query(*args, **kwargs)
        __update_last_action(*args, **kwargs)
    return updates


@user_action
def create_user(user_id):
    user = User.get_or_create(user_id=user_id)


def get_user(user_id):
    return User.get(user_id=user_id)


def get_state(user_id):
    user = User.get(user_id)
    return user.state


def set_state(user_id, state):
    user = User.get(user_id=user_id)
    user.state = state
    user.save()


def set_timeline(user_id, login):
    user = User.get(user_id=user_id)
    user.timeline_login = login
    user.save()


def change_news(user_id):
    user = User.get(user_id=user_id)
    if user.sub_news == 0:
        user.sub_news = 1
    else:
        user.sub_news = 0
    user.save()


def get_sub_news(user_id)-> str:
    user = User.get(user_id=user_id)
    if user.sub_news == 0:
        sub = 'Вы подписка'
    else:
        sub = 'Вы не подписаны'
    return sub


def set_sub_schedule(user_id, type, schedule_id):
    user = User.get(user_id=user_id)
    sub = str({'type': type, 'schedule_id': schedule_id})
    user.save()


def get_sub_schedule(user_id) -> dict:
    user = User.get(user_id=user_id)
    return json.loads(user.sub_schedule)


def set_state_data(user_id, **kwargs):
    # todo
    pass


def get_state_data(user_id) -> dict:
    user = User.get(user_id=user_id)
    return json.loads(user.state_data)
