import telebot
import config
import flask
import schedule
import locale
import pprint
from time import time
from peewee import *
import os

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


@bot.message_handler(commands=['/start'])
def hello(message):
    """add user into base"""


@bot.message_handler(content_types=['text'])
def text_handler(message):
    groups = schedule.get_groups()
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for gr in range(100):
        print(groups[gr])
        keyboard.row(groups[gr])
    bot.send_message(message.chat.id, 'test', reply_markup=keyboard)


print('run')
if __name__ == '__main__':
    # set locale to send weekdays in RU format
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

    bot.polling(none_stop=True)
