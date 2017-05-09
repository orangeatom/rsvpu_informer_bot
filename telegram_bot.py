import telebot
import config
import flask
import schedule
import locale
from time import time
from peewee import *
import os
import datetime
from pprint import pprint
from models import *

app = flask.Flask(__name__)

bot = telebot.TeleBot(config.TOKEN)

Weekdays = ('🌕 *Понедельник*',
            '🌖 *Вторник*',
            '🌗 *Среда*',
            '🌘 *Четверг*',
            '🌑 *Пятница*',
            '🌒 *Суббота*',
            '🌓 *Воскресенье*')


localbase = SqliteDatabase('base.db')
print('local db connect')
localbase.connect()


def format_schedule_group(schedule: list, date: datetime.date) -> str:
    """Make something"""
    pass


@bot.message_handler(commands=['/start'])
def hello(message):
    """add user into base"""
    User.get_or_create()


@bot.message_handler(content_types=['text'])
def text_handler(message):
    groups = schedule.get_groups()
    msg = schedule.schedule_group_query(1709, '05.08.17')
    pprint(msg)
    print(type(msg))
    bot.send_message(message.chat.id, 'text')


print('run')
if __name__ == '__main__':
    # set locale to send weekdays in RU format
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

    bot.polling(none_stop=True)

