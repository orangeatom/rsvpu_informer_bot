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

weekdays = ('🌕 *Понедельник*',
            '🌖 *Вторник*',
            '🌗 *Среда*',
            '🌘 *Четверг*',
            '🌑 *Пятница*',
            '🌒 *Суббота*',
            '🌓 *Воскресенье*')

pair_time = [
            (28800, '1️⃣ *08:00*'),
            (35100, '2️⃣ *09:45*'),
            (41400, '3️⃣ *11:30*'),
            (43200, '3️⃣ *12:00*'),
            (49500, '4️⃣ *13:45*'),
            (55800, '5️⃣ *15:30*'),
            (62100, '6️⃣ *17:15*'),
            (68400, '7️⃣ *19:00*')]

localbase = SqliteDatabase('base.db')
print('local db connect')
localbase.connect()


def format_schedule_group(pairs: dict, date: datetime.date, gruop_id) -> str:
    """Make schedule in str, ready to send end user"""
    course = schedule.get_groups_course(gruop_id)
    print(course)
    text = ' {0}. _{1}_\n'.format(weekdays[date.weekday()], date.strftime('%d %B'))
    for pair in pair_time:
        if course in (1, 2) and pair[0] == 41400:
            continue
        elif course > 2 and pair[0] == 43200:
            continue
        text += '{0} '.format(pair[1])
        if len(pairs[pair[0]]):
            for subject in pairs[pair[0]]:
                text += '{0} ({1})  *{2}* {3}\n'.format(subject['subject'],
                                                        subject['type'],
                                                        subject['classroom'],
                                                        str(subject['subgroup_name']) if subject['subgroup_name'] else '')
        else:
            text += ' --- \n'
        pass
    return text
    pass


@bot.message_handler(commands=['/start'])
def hello(message):
    """add user into base"""
    User.get_or_create()


@bot.message_handler(content_types=['text'])
def text_handler(message):
    t = time()
    groups = schedule.get_groups()
    msg = schedule.schedule_group_query(1709, '05.18.17')
    text = format_schedule_group(msg, datetime.date(17, 5, 18), 1709)
    print(schedule.lecturers_stream(1812))
    bot.send_message(message.chat.id, text, parse_mode='MARKDOWN')
    t2 = time()
    print(t2-t)


#print('run')
if __name__ == '__main__':
    # set locale to send weekdays in RU format
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    bot.polling(none_stop=True)

