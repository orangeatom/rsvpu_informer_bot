import datetime
import locale
import logging
from threading import Thread
import time


import telebot
import flask
import requests

import config
import state
import user
import schedule_db
from contents import *


app = flask.Flask(__name__)

bot = telebot.TeleBot(config.TOKEN)
WEBHOOK_URL_BASE = 'https://%s' % (config.HOST)#, config.FLASKCONNECTION.port)
WEBHOOK_URL_PATH = '/bot/%s/' % (config.TOKEN)

print('local db connect')
config.LOCALBASE.connect()


def compare_state(expected_state):
    """if state of user match with expected state return True, otherwise False"""
    def compare(msg):
        usr = user.User(msg)
        return usr.get_state() == expected_state

    return compare


def menu_kb(user)-> telebot.types.ReplyKeyboardMarkup:
    """Main menu keyboard"""
    user.set_state(state.states['Menu'])
    user.set_state_data({})
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.row(TODAY, TOMORROW, WEEK)
    kb.row(SCHEDULE_TEACHER)
    kb.row(SCHEDULE_GROUP)
    kb.row(SCHEDULE_CLASSROOM)
    kb.row(TIMETABLE)
    kb.row(IMPORTANT_LINS)
    kb.row(SOCIAL_NETS)
    kb.row(LOCATION_OF_BUILDINGS)
    kb.row(SETTINGS)
    return kb


def setting_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    """Setting menu keyboard"""
    user.set_state(state.states['Settings'])
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    kb.row(SCHEDULE_SUB)
    kb.row(MENU)
    return kb


def search_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    """Search menu for user"""
    user.set_state(state.states['Get_search_schedule_step2'])
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.row(TODAY, TOMORROW)
    kb.row(WEEK, TWO_WEEK)
    kb.row(MENU)
    return kb


def timetable_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    user.set_state(state.states['Get_timetable'])
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.row(PRIMARY_TIMETABLE, SENIOR_TIMETABLE)
    kb.row(MENU)
    return kb


def sub_schedule_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    """menu where user can change his schedule subscription"""
    user.set_state(state.states['Set_sub_schedule'])
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.row(SCHEDULE_GROUP)
    kb.row(SCHEDULE_TEACHER)
    kb.row(CANCEL)
    return kb


def academic_buldings_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    """return keyaboadr with academic buildings"""
    user.set_state(state.states['Get_academic_buildings'])
    kb = telebot.types.ReplyKeyboardMarkup()
    for ab in academic_buildings:
        kb.row([ab][0][0])
    kb.row(MENU)
    return kb


# formatting schedule


def format_schedule_group(pairs: dict, date: datetime.date, group_id) -> str:
    """Make schedule in str, ready to send end user"""
    text = ' {0}. _{1}_\n'.format(weekdays[date.weekday()], date.strftime('%d %B'))
    last = 8
    for l in reversed(pair_time):
        if len(pairs[l[0]]) != 0:
            last = pair_time.index(l) + 1
            if last == 9:
                last = 8
            break
        elif pair_time.index(l) == 0:
            text += '🎉*Выходной!!!*🎉'
            return text

    for pair in range(last):
        if len(pairs[43200]):
            if pair_time[pair][0] == 41400:
                continue
        elif len(pairs[41400]):
            if pair_time[pair][0] == 43200:
                continue

        text += '`{0}` '.format(pair_time[pair][1])
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
    last = 8
    for l in reversed(pair_time):
        if len(pairs[l[0]]) != 0:
            last = pair_time.index(l) + 1
            if last == 9:
                last = 8
            break
        elif pair_time.index(l) == 0:
            text += '🎉*Выходной!!!*🎉'
            return text

    for pair in range(last):
        if len(pairs[43200]):
            if pair_time[pair][0] == 41400:
                continue
        elif len(pairs[41400]):
            if pair_time[pair][0] == 43200:
                continue

        text += '`{0}` '.format(pair_time[pair][1])
        if len(pairs[pair_time[pair][0]]):
            for subject in pairs[pair_time[pair][0]]:
                target_audience = ''
                if subject['stream']:
                    stream = schedule_db.lecturers_stream(subject['stream'])
                    target_audience = ', '.join(stream)
                elif subject['subgroup_name']:
                    target_audience = subject['subgroup_name'][:-1] + 'п/г) '
                else:
                    target_audience = subject['group_name']

                text += '{0} ({1})  *{2}* {3} {4} \n'.format(subject['subject'],
                                                             subject['type'],
                                                             subject['classroom'],
                                                             target_audience,
                                                             str(subject['note']) if subject['note'] else '')
        else:
            text += ' --- \n'
            pass
    return text


def format_schedule_classroom(pairs: dict, date: datetime.date, classroom_id) -> str:
    """format schedule in str, ready to send user"""
    text = ' {0}. _{1}_\n'.format(weekdays[date.weekday()], date.strftime('%d %B'))
    last = 8
    for l in reversed(pair_time):
        if len(pairs[l[0]]) != 0:
            last = pair_time.index(l) + 1
            if last == 9:
                last = 8
            break
        elif pair_time.index(l) == 0:
            text += 'Аудитория пустует целый день...'
            return text

    for pair in range(last):
        if len(pairs[43200]):
            if pair_time[pair][0] == 41400:
                continue
        elif len(pairs[41400]):
            if pair_time[pair][0] == 43200:
                continue

        text += '`{0}` '.format(pair_time[pair][1])
        if len(pairs[pair_time[pair][0]]):
            for subject in pairs[pair_time[pair][0]]:
                target_audience = ''
                if subject['stream']:
                    stream = schedule_db.lecturers_stream(subject['stream'])
                    target_audience = ', '.join(stream)
                elif subject['subgroup_name']:
                    target_audience = subject['subgroup_name'][:-1] + ' п/г) '
                else:
                    target_audience = subject['group_name']

                text += '{0} ({1})  *{2}* {3} *{4}* *{5}*\n'.format(subject['subject'],
                                                                    subject['type'],
                                                                    subject['classroom_name'],
                                                                    subject['teacher_name'],
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


def get_self_schedule(usr, day) -> str:
    """return schedule of this user on selected day"""
    schedule_sub = usr.get_sub_schedule()
    if schedule_sub:
        if 'type' in schedule_sub.keys():
            if schedule_sub['type'] == user.ScheduleType.Teacher:
                pairs = schedule_db.schedule_teacher_query(schedule_sub['schedule_id'], day)
                text = format_schedule_teacher(pairs, day, schedule_sub['schedule_id'])
            else:
                pairs = schedule_db.schedule_group_query(schedule_sub['schedule_id'], day)
                text = format_schedule_group(pairs, day, schedule_sub['schedule_id'])
        else:
            pass
    else:
        text = SUB_ERROR
    return text


def get_schedule(type, schedule_id, day):
    """return schedule from search on selected day """
    if type == user.ScheduleType.Teacher:
        pairs = schedule_db.schedule_teacher_query(schedule_id, day)
        text = format_schedule_teacher(pairs, day, schedule_id)
    elif type == user.ScheduleType.Group:
        pairs = schedule_db.schedule_group_query(schedule_id, day)
        text = format_schedule_group(pairs, day, schedule_id)
    elif type == user.ScheduleType.Classroom:
        pairs = schedule_db.schedule_classroom_query(schedule_id, day)
        text = format_schedule_classroom(pairs, day, schedule_id)
    else:
        text = 'я тут что то запутался, походу вы меня сломали'
    return text
# web server logic


@app.route('/', methods=['GET'])
def index():
    return ""


@app.route('/{0}/<username>'.format('timeline'), methods=['GET', 'HEAD', 'POST'])
def timeline(username):
    return ''


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# here start bot's logic


@bot.inline_handler(func=lambda query: True)
def send_schedule(query):
    # todo make it in multithreading
    usr = user.User(query=query)
    if usr.get_sub_schedule():
        schedule_type = usr.get_sub_schedule()['type']
        live_time = 1000
        icon_url = 'https://cs7061.userapi.com/c812726/u47444051/docs/f397e837e006/geometry123_3.png?extra=LSfxXeiPTx-k8bmpqASfMtgvIbXmcZSOV6p6sCWZFFZxo2N_OqRH0qJEC6TpyxULig8a6Vnzmp5MXvlc6jsioeLwWq1Sq6eyywMiVf9C1hSwmPKz9Rjp'
        schedule_id = usr.get_sub_schedule()['schedule_id']
        if schedule_type == user.ScheduleType.Teacher:
            schedule = []
            days = schedule_db.Days.days_from_today(15)
            i = 1
            for d in days:
                pairs = schedule_db.schedule_teacher_query(schedule_id, d)
                text = format_schedule_group(pairs, d, schedule_id)
                schedule.append(telebot.types.InlineQueryResultArticle(id=str(i),
                                                                       title=d.strftime('%d %B'),
                                                                       description=schedule_db.get_teachers(id=schedule_id)[0]['shortname'],
                                                                       input_message_content=telebot.types.InputTextMessageContent(
                                                                           message_text=text, parse_mode='MARKDOWN'),
                                                                       thumb_url=icon_url, thumb_height=15))
                i += 1
            bot.answer_inline_query(query.id, schedule, cache_time=live_time)
        elif schedule_type == user.ScheduleType.Group:
            schedule = []
            days = schedule_db.Days.days_from_today(15)
            i = 1
            for d in days:
                pairs = schedule_db.schedule_group_query(schedule_id, d)
                text = format_schedule_group(pairs, d, schedule_id)
                schedule.append(telebot.types.InlineQueryResultArticle(id=str(i),
                                                                       title=d.strftime('%d %B'),
                                                                       description=
                                                                       schedule_db.get_groups(id=schedule_id)[0][
                                                                           'group_name'],
                                                                       input_message_content=telebot.types.InputTextMessageContent(
                                                                           message_text=text, parse_mode='MARKDOWN'),
                                                                       thumb_url=icon_url, thumb_height=15))
                i += 1
            bot.answer_inline_query(query.id, schedule, cache_time=live_time)
    else:
        pass


@bot.message_handler(commands=['start'])
def hello(message):
    """add user_of_bot into base"""
    usr = user.User(message)
    usr.set_state(state.states['StartMenu'])
    start_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    start_board.row('Подписаться на расписание')
    start_board.row('В меню')
    bot.send_message(usr.chat_id,
                     '*Привет, я обновленная версия бота!!!* [О боте](telegra.ph/RGPPU-informer-bot-05-11)',
                     parse_mode='MARKDOWN',
                     reply_markup=start_board)


@bot.message_handler(content_types=['sticker', 'voice', 'audio', 'document', 'photo'])
def content_filter(message):
    bot.send_message(message.chat.id, NONE_TEXT_MSG,
                     parse_mode='MARKDOWN')


@bot.message_handler(func=compare_state(state.states['StartMenu']),
                     content_types=['text'])
def start_menu(message):
    """
    Start menu Handler
    """
    # todo
    usr = user.User(message)
    if message.text == 'Подписаться на расписание':
        usr.set_state(state.states['Set_sub_schedule'])
        sub_keyboard = telebot.types.ReplyKeyboardMarkup()
        sub_keyboard.row(SCHEDULE_GROUP)
        sub_keyboard.row(SCHEDULE_TEACHER)
        bot.send_message(usr.chat_id, 'Выберите необходимый вам тип расписания: ',
                         reply_markup=sub_keyboard)
    elif message.text == 'Подписаться на новости':
        bot.send_message(usr.chat_id, 'Вы подписались на новости. Отменить подписку можно в настройках',
                         reply_markup=menu_kb(usr))
    elif message.text == 'Зайти в timeline':
        bot.send_message(usr.chat_id, 'Временно не завезли =(')
    elif message.text == 'В меню':
        bot.send_message(usr.chat_id, 'Открываю меню',
                         reply_markup=menu_kb(usr))
    else:
        bot.send_message(usr.chat_id, 'Я не знаю такой команды!')


@bot.message_handler(func=compare_state(state.states['Set_sub_schedule']),
                     content_types=['text'])
def sub_menu(message):
    """
    Sub schedule Handler
    """
    usr = user.User(message)
    if message.text == SCHEDULE_GROUP:
        usr.set_state_data({"type": user.ScheduleType.Group})
        bot.send_message(usr.chat_id,
                         "Введите нужную вам группу, я попробую её найти.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == SCHEDULE_TEACHER:
        usr.set_state_data({"type": user.ScheduleType.Teacher})
        bot.send_message(usr.chat_id,
                         "Введите имя преподавателя, я попробую найти.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif 'type' in usr.get_state_data().keys():
        state_data = usr.get_state_data()
        if state_data['type'] == user.ScheduleType.Teacher:
            teachers = schedule_db.get_teachers(message.text)
            if len(teachers):
                if len(teachers) == 1:
                    usr.set_sub_schedule(user.ScheduleType.Teacher, teachers[0]['teacher_id'])
                    usr.set_state(state.states['Menu'])
                    bot.send_message(usr.chat_id,
                                     "Поздравляю! Вы подписаны на расписание преподавателя!🎉",
                                     reply_markup=menu_kb(usr))
                elif 1 < len(teachers) <= 25:
                    teachers_kb = telebot.types.ReplyKeyboardMarkup()
                    for teach in teachers:
                        teachers_kb.row(teach['fullname'])
                    bot.send_message(usr.chat_id,
                                     'Выберите необходимого вам преподавателя',
                                     reply_markup=teachers_kb)
                else:
                    bot.send_message(usr.chat_id,
                                     "Результат поиска получился слишком большой, попробуйте ввести запрос конктретнее",
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                bot.send_message(usr.chat_id, 'Я ничего не нашел, попробуйте ввести иначе.')
        elif state_data['type'] == user.ScheduleType.Group:
            groups = schedule_db.get_groups(message.text)
            if len(groups):
                if len(groups) == 1:
                    usr.set_sub_schedule(user.ScheduleType.Group, groups[0]['group_id'])
                    usr.set_state(state.states['Menu'])
                    bot.send_message(usr.chat_id,
                                     "Поздравляю! Вы подписаны на группу {0}🎉".format(groups[0]['group_name']),
                                     reply_markup=menu_kb(usr))
                elif 1 < len(groups) <= 15:
                    groups_kb = telebot.types.ReplyKeyboardMarkup()
                    for gr in groups:
                        groups_kb.row(gr['group_name'])
                    bot.send_message(usr.chat_id,
                                     "Выберите из данного списка нужную вам группу, или введите заного,"
                                     " если я не нашел нужную вам группу.",
                                     reply_markup=groups_kb)
                else:
                    bot.send_message(usr.chat_id,
                                     "Результат поиска получился слишком большой, попробуйте ввести запрос конктретнее",
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                bot.send_message(usr.chat_id, 'Я ничего не нашел, попробуйте ввести иначе.')
            pass
    elif (message.text == CANCEL and usr.get_sub_schedule() is not None):
        bot.send_message(usr.chat_id, 'Перехожу обратно в настройки', reply_markup=setting_kb(usr))
    else:
        bot.send_message(usr.chat_id, 'Я такого не ожидал, выберите пожалуйста пункт из списка')


@bot.message_handler(func=compare_state(state.states['Menu']),
                     content_types=['text'])
def main_menu(message):
    """
    Main menu
    """
    usr = user.User(message)
    if message.text == TODAY:
        text = get_self_schedule(usr, schedule_db.Days.today())
        bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN')

    elif message.text == TOMORROW:
        text = get_self_schedule(usr, schedule_db.Days.tomorrow())
        bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN')

    elif message.text == WEEK:
        schedule_sub = usr.get_sub_schedule()
        days = schedule_db.Days.days_from_today(8)
        final_text = ''
        for day in days:
            text = get_self_schedule(usr, day)
            if text == SUB_ERROR:
                bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN', disable_notification=True)
                break
            else:
                final_text += get_self_schedule(usr, day) + '\n\n'
        bot.send_message(usr.chat_id, final_text, parse_mode='MARKDOWN', disable_notification=True)
    elif message.text == SCHEDULE_GROUP:
        usr.set_state_data({'type': user.ScheduleType.Group})
        usr.set_state(state.states['Get_search_schedule_step1'])
        bot.send_message(usr.chat_id, 'Введите необходимую группу',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == SCHEDULE_TEACHER:
        usr.set_state_data({'type': user.ScheduleType.Teacher})
        usr.set_state(state.states['Get_search_schedule_step1'])
        bot.send_message(usr.chat_id, 'Введите имя или фамилию преподавателя, я попробую найти.',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == SCHEDULE_CLASSROOM:
        usr.set_state_data({'type': user.ScheduleType.Classroom})
        usr.set_state(state.states['Get_search_schedule_step1'])
        bot.send_message(usr.chat_id, 'Введите необходимую аудиторию в формате X-XXX',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    elif message.text == DATE:
        canсel_kb = telebot.types.ReplyKeyboardMarkup()
        canсel_kb.row('Отмена')
        bot.send_message(usr.chat_id,
                         'Введите необходимую вам дату в формате дд мм или дд месяц', reply_markup=canсel_kb)
        usr.set_state(state.states['Get_self_schedule_date'])

    elif message.text == TIMETABLE:
        bot.send_message(usr.chat_id,
                         'Выберите пункт',
                         reply_markup=timetable_kb(usr))

    elif message.text == IMPORTANT_LINS:
        bot.send_message(usr.chat_id, important_links, parse_mode='MARKDOWN',disable_web_page_preview=True)

    elif message.text == SOCIAL_NETS:
        bot.send_message(usr.chat_id, social_nets, parse_mode='MARKDOWN',disable_web_page_preview=True)

    elif message.text == LOCATION_OF_BUILDINGS:
        bot.send_message(usr.chat_id, "Выберите интересующий вас корпус, я скажу где он",
                         reply_markup=academic_buldings_kb(usr))
    elif message.text == SETTINGS:
        bot.send_message(usr.chat_id, 'Выберите пункт', reply_markup=setting_kb(usr))

    else:
        try:
            try:
                date = datetime.datetime.strptime('{0} {1}'.format(message.text, datetime.datetime.today().year),
                                                  '%d %B %Y')
            except:
                date = datetime.datetime.strptime('{0} {1}'.format(message.text, datetime.datetime.today().year),
                                                  '%d %m %Y')
            text = get_self_schedule(usr, date.date())
            bot.send_message(usr.chat_id,
                             text,
                             parse_mode='MARKDOWN',
                             reply_markup=menu_kb(usr))
        except:
            bot.send_message(usr.chat_id, 'Я не смог найти такую дату =(, введи дату заново')


@bot.message_handler(func=compare_state(state.states['Settings']),
                     content_types=['text'])
def setting(message):
    usr = user.User(message)
    if message.text == SCHEDULE_SUB:
        bot.send_message(usr.chat_id, 'Выберите необходимый вам тип расписания', reply_markup=sub_schedule_kb(usr))
    elif (message.text == ON_NEWS or message.text == OFF_NEWS):
        if usr.get_sub_news():
            bot.send_message(usr.chat_id, 'Подписка отменена', reply_markup=setting_kb(usr))
        else:
            bot.send_message(usr.chat_id, 'Я оповещу вас о свежих новостях', reply_markup=setting_kb(usr))
        usr.change_news()
        pass
    elif message.text == TIMELINE:
        # todo
        usr.set_state(state.states['Timeline_login'])
        bot.send_message(usr.chat_id, 'Введите логин от вашей учетной записи в Таймлайн',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        pass
    elif message.text == MENU:
        bot.send_message(usr.chat_id, 'Открываю меню', reply_markup=menu_kb(usr))
    else:
        bot.send_message(usr.chat_id, 'Выберите одну из предложенных вам команд')


@bot.message_handler(func=compare_state(state.states['Get_self_schedule_date']),
                     content_types=['text'])
def self_date_schedule(message):
    usr = user.User(message)
    if message.text != 'Отмена':
        try:
            try:
                date = datetime.datetime.strptime('{0} {1}'.format(message.text, datetime.datetime.today().year),
                                                  '%d %B %Y')
            except:
                date = datetime.datetime.strptime('{0} {1}'.format(message.text, datetime.datetime.today().year),
                                                  '%d %m %Y')
            text = get_self_schedule(usr, date.date())
            bot.send_message(usr.chat_id,
                             text,
                             parse_mode='MARKDOWN',
                             reply_markup=menu_kb(usr))
        except:
            bot.send_message(usr.chat_id, 'Я не смог найти такую дату =(, введи дату заново')
    else:
        bot.send_message(usr.chat_id, MENU_ENTER, reply_markup=menu_kb(usr))


@bot.message_handler(func=compare_state(state.states['Get_timetable']),
                     content_types=['text'])
def timetable(message):
    usr = user.User(message)
    if message.text == PRIMARY_TIMETABLE:
        bot.send_message(usr.chat_id, primary_timetable, reply_markup=menu_kb(usr), parse_mode='MARKDOWN')
    elif message.text == SENIOR_TIMETABLE:
        bot.send_message(usr.chat_id, senior_timetable, reply_markup=menu_kb(usr), parse_mode='MARKDOWN')
    elif message.text == MENU:
        bot.send_message(usr.chat_id, 'Открываю меню', reply_markup=menu_kb(usr))
    else:
        bot.send_message(usr.chat_id, 'Неизвестная команда')


@bot.message_handler(func=compare_state(state.states['Get_search_schedule_step1']),
                     content_types=['text'])
def search_target(message):
    usr = user.User(message)
    if usr.get_state_data().keys():
        if 'type' in usr.get_state_data().keys():
            if usr.get_state_data()['type'] == user.ScheduleType.Classroom:
                classroom = schedule_db.get_classrooms(message.text)
                if classroom:
                    usr.set_state_data({'type': user.ScheduleType.Classroom,
                                        'schedule_id': classroom['classroom_id']})
                    bot.send_message(usr.chat_id, SELECT_INTERVAL+';', reply_markup=search_kb(usr))
                else:
                    bot.send_message(usr.chat_id, 'Я не смог найти такую аудиторию, попробуй ввести еще раз')

            elif usr.get_state_data()['type'] == user.ScheduleType.Teacher:
                teachers = schedule_db.get_teachers(message.text)
                if teachers:
                    if len(teachers) == 1:
                        # if search return one result
                        usr.set_state_data({'type': user.ScheduleType.Teacher,
                                            'schedule_id': teachers[0]['teacher_id']})
                        bot.send_message(usr.chat_id, SELECT_INTERVAL, reply_markup=search_kb(usr))
                    elif 1<len(teachers) <= 30:
                        kb = telebot.types.ReplyKeyboardMarkup()
                        for t in teachers:
                            kb.row(t['fullname'])
                        bot.send_message(usr.chat_id, 'Выберите необходимого преподавателя из списка', reply_markup=kb)
                    elif len(teachers) > 30:
                        bot.send_message(usr.chat_id,
                                         'Результат поиска получил слишком много результатов, попробуйте ввести более конкретное значение')
                else:
                    pass
                pass

            elif usr.get_state_data()['type'] == user.ScheduleType.Group:
                groups = schedule_db.get_groups(message.text)
                if groups:
                    if len(groups) == 1:
                        usr.set_state_data({'type': user.ScheduleType.Group,
                                            'schedule_id': groups[0]['group_id']})
                        bot.send_message(usr.chat_id, SELECT_INTERVAL, reply_markup=search_kb(usr))
                    elif 1 < len(groups) <= 50:
                        kb = telebot.types.ReplyKeyboardMarkup()
                        for t in groups:
                            kb.row(t['group_name'])
                        bot.send_message(usr.chat_id, 'Выберите необходимого преподавателя из списка', reply_markup=kb)
                    elif len(groups) > 50:
                        bot.send_message(usr.chat_id,
                                         'Результат поиска получил слишком много результатов, попробуйте ввести более конкретное значение')


@bot.message_handler(func=compare_state(state.states['Get_search_schedule_step2']),
                     content_types=['text'])
def search_schedule(message):
    usr = user.User(message)
    if message.text == TODAY:
        schedule = get_schedule(usr.get_state_data()['type'],
                                usr.get_state_data()['schedule_id'],
                                schedule_db.Days.today())
        bot.send_message(usr.chat_id, schedule, parse_mode='MARKDOWN')
    elif message.text == TOMORROW:
        schedule = get_schedule(usr.get_state_data()['type'],
                                usr.get_state_data()['schedule_id'],
                                schedule_db.Days.tomorrow())
        bot.send_message(usr.chat_id, schedule, parse_mode='MARKDOWN')
    elif message.text == WEEK:
        days = schedule_db.Days.days_from_today(8)
        text = ''
        for d in days:
            schedule = get_schedule(usr.get_state_data()['type'],
                                    usr.get_state_data()['schedule_id'],
                                    d)
            if datetime.date.weekday(d) == 6:
                text += schedule + '\n\n{0}\n'.format(SPLIT_WEEKS)
            else:
                text += schedule + '\n\n'
        bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN')
    elif message.text == TWO_WEEK:
        days = schedule_db.Days.days_from_today(15)
        text = ''
        for d in days[:-7]:
            schedule = get_schedule(usr.get_state_data()['type'],
                                    usr.get_state_data()['schedule_id'],
                                    d)
            text += schedule
            if datetime.date.weekday(d) == 6:
                text += '\n{0}\n'.format(SPLIT_WEEKS)
            else:
                text += '\n\n'
        bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN')
        text = ''
        for d in days[-7:]:
            schedule = get_schedule(usr.get_state_data()['type'],
                                    usr.get_state_data()['schedule_id'],
                                    d)
            text += schedule
            if datetime.date.weekday(d) == 6:
                text += '\n\n{0}\n'.format(SPLIT_WEEKS)
            else:
                text += '\n\n'
        bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN')

    elif message.text == MENU:
        bot.send_message(usr.chat_id, MENU_ENTER, reply_markup=menu_kb(usr))
    else:
        bot.send_message(usr.chat_id, SELECT_INTERVAL)


@bot.message_handler(func=compare_state(state.states['Get_academic_buildings']),
                     content_types=['text'])
def get_academic_buildings(message):
    usr = user.User(message)
    if message.text == MENU:
        bot.send_message(usr.chat_id, MENU_ENTER, reply_markup=menu_kb(usr))
    else:
        for ab in academic_buildings:
            if message.text == ab[0]:
                text = ab[1]
                bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN', disable_web_page_preview=True)
                break

        else:
            bot.send_message(usr.chat_id, "Я не знаю такого корпуса, выберите из списка")


@bot.message_handler(func=compare_state(state.states['Timeline_login']),
                     content_types=['text'])
def login_timeline(message):
    """auth user in Timeline"""
    usr = user.User(message)
    if usr.get_state_data():
        print('hehe')
    pass


@bot.message_handler(content_types=['text'])
def text_handler(message):
    bot.send_message(message.chat.id, 'оооопс, ты поломал меня, нажми /start и начни работу с начала, '
                                      'подписка сохранится, и доложи об этом автору, пусть чистит за собой косяки',
                     parse_mode='MARKDOWN')


# set locale to send weekdays in RU format

locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)#,
