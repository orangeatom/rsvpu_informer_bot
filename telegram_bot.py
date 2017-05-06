import telebot
import config
import flask
import schedule
import locale
import pprint
from time import time
from peewee import *
from models import User

app = flask.Flask(__name__)

bot = telebot.TeleBot(config.token)

Weekdays = ('🌕 *Понедельник*',
            '🌖 *Вторник*',
            '🌗 *Среда*',
            '🌘 *Четверг*',
            '🌑 *Пятница*',
            '🌒 *Суббота*',
            '🌓 *Воскресенье*')

localbase = config.localbase
print('local db connect')
localbase.connect()


@bot.message_handler(commands=['/start'])
def hello(message):
    """add user into base"""


@bot.message_handler(content_types=['text'])
def text_handler(message):
    var = schedule.get_groups()
    print(var)


# set locale to send weekdays in RU format
locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

print('run')
if __name__ == '__main__':

    bot.polling(none_stop=True)
