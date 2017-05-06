import telebot
import config
import flask
import schedule
import pprint
from time import time
from peewee import *

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


@bot.message_handler(commands=['/start'])
def hello(message):
    """add user into base"""



@bot.message_handler(content_types=['text'])
def text_handler(message):
    var = schedule.get_groups()
    print('ghge')
    print(var)


if __name__ == '__main__':
    bot.polling(none_stop=True)
