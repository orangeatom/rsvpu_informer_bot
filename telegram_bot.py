import telebot
import config
import flask

bot = telebot.TeleBot(config.token)

app = flask.Flask(__name__)

@bot.message_handler(func=lambda: True)
def hello(message):
    pass



if __name__ == '__main__':
    bot.polling(none_stop=True)
