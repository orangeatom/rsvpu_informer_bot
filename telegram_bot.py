import telebot
import config
import flask
import schedule_db
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

localbase = config.LOCALBASE
print('local db connect')
localbase.connect()


def format_schedule_group(pairs: dict, date: datetime.date, group_id) -> str:
    """Make schedule in str, ready to send end user"""
    course = schedule_db.get_groups_course(group_id)
    text = ' {0}. _{1}_\n'.format(weekdays[date.weekday()], date.strftime('%d %B'))
    first, last = 0, 8
    for l in reversed(pair_time):
        if len(pairs[l[0]]) != 0:
            last = pair_time.index(l) + 1
            if last == 9:
                last = 8
            break
        elif pair_time.index(l) == 0:
            text += '🎉*Выходной!!!*🎉'
            return text

    for pair in range(first, last):
        if course in (1, 2) and pair_time[pair][0] == 43200:
            continue
        elif course > 2 and pair_time[pair][0] == 41400:
            continue

        text += '{0} '.format(pair_time[pair][1])
        if len(pairs[pair_time[pair][0]]):
            for subject in pairs[pair_time[pair][0]]:
                text += '{0} ({1})  *{2}* {3} {4} _{5}_\n'.format(subject['subject'],
                                                                  subject['type'],
                                                                  subject['classroom'],
                                                                  subject['teacher'],
                                                                  str(subject['subgroup_name'])[-3:-1] + ' п/г) ' if subject['subgroup_name'] else '',
                                                                  str(subject['note']) if subject['note'] else '')
        else:
            text += ' --- \n'
            pass
    return text


def format_schedule_teacher(pairs: dict, date: datetime.date, teacher_id) -> str:
    """Make schedule in str, ready to send end user"""
    text = ' {0}. _{1}_\n'.format(weekdays[date.weekday()], date.strftime('%d %B'))
    first, last = 0, 8
    for l in reversed(pair_time):
        if len(pairs[l[0]]) != 0:
            last = pair_time.index(l) + 1
            if last == 9:
                last = 8
            break
        elif pair_time.index(l) == 0:
            text += '🎉*Выходной!!!*🎉'
            return text

    for pair in range(first, last):
        if len(pairs[43200]):
            if pair_time[pair][0] == 41400:
                continue
        elif len(pairs[41400]):
            if pair_time[pair][0] == 43200:
                continue

        text += '{0} '.format(pair_time[pair][1])
        if len(pairs[pair_time[pair][0]]):
            for subject in pairs[pair_time[pair][0]]:
                target_audience = ''
                if subject['stream']:
                    stream = schedule_db.lecturers_stream(subject['stream'])
                    target_audience = ', '.join(stream)
                elif subject['subgroup_name']:
                    target_audience = subject['subgroup_name']
                else:
                    target_audience = subject['group_name']

                text += '{0} ({1})  *{2}* {3} {4} _{5}_\n'.format(subject['subject'],
                                                                  subject['type'],
                                                                  subject['classroom'],
                                                                  subject['teacher'],
                                                                  target_audience,
                                                                  str(subject['note']) if subject['note'] else '')
        else:
            text += ' --- \n'
            pass
    return text


def get_group(name=None, group_id=None) -> list:
    if name:
        result = schedule_db.get_groups(group_substr=name)
    elif group_id:
        result = schedule_db.get_groups(id=group_id)
    else:
        result = schedule_db.get_groups()
    return result

# here start bot's logic


@bot.message_handler(commands=['start'])
def hello(message):
    """add user into base"""
    # todo create user, and set his state on 'imagine value'
    # User.get_or_create()
    start_board = telebot.types.ReplyKeyboardMarkup()
    start_board.row('Оформить подписку на расписание')
    start_board.row('Найти расписание')
    start_board.row('Зайти в timeline')
    start_board.row('В меню')
    bot.send_message(message.chat.id,
                     'Hello nigga [О боте](telegra.ph/RGPPU-informer-bot-05-11)',
                     parse_mode='MARKDOWN',
                     reply_markup=start_board)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    groups = schedule_db.get_groups()

    text = schedule_db.get_groups(message.text)
    keyboart = telebot.types.ReplyKeyboardMarkup()
    stext = message.text
    for i in range(15, 22):
        msg = schedule_db.schedule_teacher_query(stext,
                                                 '05.{0}.17'.format(i))
        bot.send_message(message.chat.id,
                         format_schedule_teacher(msg, datetime.date(17, 5, i), message.text),
                         reply_markup=telebot.types.ReplyKeyboardRemove(),
                         parse_mode='MARKDOWN')


if __name__ == '__main__':
    # set locale to send weekdays in RU format
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    print('run')
    bot.polling(none_stop=True)

