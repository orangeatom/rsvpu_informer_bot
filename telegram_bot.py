import schedule_db
import state
import telebot
import config
import flask
import locale
import datetime
import user
from pprint import pprint

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
            (28800, '1️⃣ 08:00'),
            (35100, '2️⃣ 09:45'),
            (41400, '3️⃣ 11:30'),
            (43200, '3️⃣ 12:00'),
            (49500, '4️⃣ 13:45'),
            (55800, '5️⃣ 15:30'),
            (62100, '6️⃣ 17:15'),
            (68400, '7️⃣ 19:00')]

localbase = config.LOCALBASE
print('local db connect')
localbase.connect()

important_links = '''
[Таймлайн](http://timeline.rsvpu.ru) - Информационная система 

[Электронная библиотека](http://umkd.rsvpu.ru) - Скачайте нужное вам методическое пособие

[Мои документы](http://www.rsvpu.ru/moi-dokumenty/) - Закажи любую справку в *одном* месте

[Об университете](http://www.rsvpu.ru/sveden/) - Сведения об образовательной организации
'''

primary_timetable = '''
`I   `1) 08:00 - 08:45
`         `2) 08:50 - 09:35

`II  `1) 09:45 - 10:30
`         `2) 10:35 - 11:20
`Перерыв 40 минут🍏` 
`III `1) 12:00 - 12:45
`         `2) 12:50 - 13:35

`IV  `1) 13:45 - 14:30
`         `2) 14:35 - 15:20

`V   `1) 15:30 - 16:15
`         `2) 16:20 - 17:05

`VI  `1) 17:15 - 18:00
`         `2) 18:05 - 18:50

`VII `1) 19:00 - 19:45
`         `2) 19:50 - 20:35
'''

senior_timetable = '''
`I   `1) 08:00 - 08:45
`         `2) 08:50 - 09:35

`II  `1) 09:45 - 10:30
`         `2) 10:35 - 11:20
     
`III `1) 11:30 - 12:15
`         `2) 12:20 - 13:05
`Перерыв 40 минут🍏`
`IV  `1) 13:45 - 14:30
`         `2) 14:35 - 15:20

`V   `1) 15:30 - 16:15
`         `2) 16:20 - 17:05

`VI  `1) 17:15 - 18:00
`         `2) 18:05 - 18:50

`VII `1) 19:00 - 19:45
`         `2) 19:50 - 20:35
'''

academic_buildings = (('Корпус 0', 'ул. Машиностроителей д. 11 \n Проезд: метро ст. «Уралмаш», троллейбус 8, 10, 17, трамвай 5, 24, автобус 56, 33, 36 остановка «Площадь 1-ой Пятилетки».'),
                      ('Корпус 1', 'ул. Машиностроителей д. 2, Проезд: метро ст. «Уралмаш», троллейбус 8, 10, 17, трамвай 5, 24, автобус 56, 33, 36 остановка «Площадь 1-ой Пятилетки».'),
                      ('Корпус 2', 'ул. Машиностроителей д. 11 \n Проезд: метро ст. «Уралмаш», троллейбус 8, 10, 17, трамвай 5, 24, автобус 56, 33, 36 остановка «Площадь 1-ой Пятилетки».'),
                      ('Корпус 3', 'ул. Каширская, 73 \n Проезд: троллейбус 13, 16, остановка «Таганская»'),
                      ('Корпус 4', 'ул. Каширская, 73 \n Проезд: троллейбус 13, 16, остановка «Таганская»'),
                      ('Корпус 5', 'ул. Каширская, 73 \n Проезд: троллейбус 13, 16, остановка «Таганская»'),
                      ('Корпус 6', 'ул. Каширская, 73 \n Проезд: троллейбус 13, 16, остановка «Таганская»'),
                      ('Корпус 7', 'ул. Машиностроителей д. 11 \n Проезд: метро ст. «Уралмаш», троллейбус 8, 10, 17, трамвай 5, 24, автобус 56, 33, 36 остановка «Площадь 1-ой Пятилетки».'),
                      ('Корпус 8', 'ул. Машиностроителей д. 11 \n Проезд: метро ст. «Уралмаш», троллейбус 8, 10, 17, трамвай 5, 24, автобус 56, 33, 36 остановка «Площадь 1-ой Пятилетки».'),
                      ('Корпус 9', 'ул. Ильича, 26 \n Проезд: троллейбус 10, остановка «Библиотека»'),
                      ('Корпус 10', 'ул. Луначарского, 85а \nПроезд: трамвай 2, 3, 8, 14, 20, 25, 26, остановка «Шевченко»'),
                      ('Корпус 11', 'ул. Машиностроителей, 9 \n Проезд: метро ст. «Уралмаш», троллейбус 8, 10, 17, трамвай 5, 24, автобус 56, 33, 36 остановка «Площадь 1-ой Пятилетки».'),
                      ('Корпус 12', 'ул. Машиностроителей, 9 \n Проезд: метро ст. «Уралмаш», троллейбус 8, 10, 17, трамвай 5, 24, автобус 56, 33, 36 остановка «Площадь 1-ой Пятилетки».'),
                      ('Корпус 13', 'ул. Таганская, 75, 75а (Колледж электроэнергетики и машиностроения) \nПроезд: троллейбус 13, 16, остановка «Таганская»'),
                      ('Корпус 14', 'ул. Таганская, 75, 75а (Колледж электроэнергетики и машиностроения) \nПроезд: троллейбус 13, 16, остановка «Таганская»'),
                      ('Корпус 15', 'ул. Фрезеровщиков, 78а'),
                      ('Корпус 16', 'ул. Баумана, дом 28 а, г. Екатеринбург (здание бывшего научно-учебного центра)\nПроезд: метро ст. «Уралмаш», автобус 36, 149, 148 остановка «ДК УЭТМ». Троллейбус 16,  автобус 148 остановка «Шефская».'),
                      ('Корпус 17', 'ул. Энгельса, дом 12 а, г. Первоуральске (здание дома культуры «Горняк»)'))


TIMETABLE = 'Расписание звонков ⏰'
IMPORTANT_LINS = 'Важные ссылки 📌'
LOCATION_OF_BUILDINGS = 'Расположение корпусов 🏛'
SETTINGS = 'Настройки 🛠'
DATE = 'Дата 📅'
WEEK = 'Неделя 🗓'
TWO_WEEK = 'Две недели 🗒'
TODAY = 'Сегодня 📅️'
TOMORROW = 'Завтра 📆'
MENU = 'В меню 🏠'
SENIOR_TIMETABLE = '3, 4 и 5 курсы'
PRIMARY_TIMETABLE = '1 и 2 курс'
ON_NEWS = 'Отключить новости❎️'
OFF_NEWS = 'Включить новости✅'
TIMELINE = 'Таймлайн 📎'
SCHEDULE_SUB = 'Подписка на расписание 📭'
SUB_ERROR = 'Оформите подписку что бы получать расписание'
SCHEDULE_TEACHER = 'Преподаватель 👤'
SCHEDULE_GROUP = 'Группа 👥'
SCHEDULE_CLASSROOM = 'Аудитория 🔢'
MENU_ENTER = 'Открываю меню'
SELECT_INTERVAL = 'Выберите нобходимый промежуток.'
SPLIT_WEEKS = '🖤💜💙💚💛❤️💛💚💙💜🖤'


def menu_kb(user)-> telebot.types.ReplyKeyboardMarkup:
    """Main menu keyboard"""
    user.set_state(state.states['Menu'])
    user.set_state_data({})
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=9)
    kb.row(TODAY, TOMORROW, WEEK)
    kb.row(SCHEDULE_TEACHER)
    kb.row(SCHEDULE_GROUP)
    kb.row(SCHEDULE_CLASSROOM)
    kb.row(TIMETABLE)
    kb.row(IMPORTANT_LINS)
    kb.row(LOCATION_OF_BUILDINGS)
    kb.row(SETTINGS)
    return kb


def setting_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    """Setting menu keyboard"""
    user.set_state(state.states['Settings'])
    kb = telebot.types.ReplyKeyboardMarkup()
    kb.row(SCHEDULE_SUB)
    if user.get_sub_news():
        kb.row(ON_NEWS)
    else:
        kb.row(OFF_NEWS)
    kb.row(TIMELINE)
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
    kb.row('Группа')
    kb.row('Преподаватель')
    kb.row('Отмена')
    return kb


def academic_buldings_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    user.set_state(state.states['Get_academic_buildings'])
    kb = telebot.types.ReplyKeyboardMarkup()
    for ab in academic_buildings:
        kb.row([ab][0][0])
    kb.row(MENU)
    return kb


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
# here start bot's logic


@bot.inline_handler(func=lambda query: True)
def some_action(query):
    usr = user.User(query=query)
    schedule_type = usr.get_sub_schedule()['type']
    schedule_id = usr.get_sub_schedule()['schedule_id']
    day = schedule_db.Days.today()
    if schedule_type == user.ScheduleType.Teacher:
        pairs = schedule_db.schedule_teacher_query(schedule_id, day)
        text = format_schedule_group(pairs, day, schedule_id)
        answer = telebot.types.InlineQueryResultArticle(id='1',
                                                        title='Сегодня',
                                                        description=schedule_db.get_teachers(id=schedule_id)[0]['shortname'],
                                                        input_message_content=telebot.types.InputTextMessageContent(
                                                            message_text=text, parse_mode='MARKDOWN'))
        bot.answer_inline_query(query.id, [answer])
    elif schedule_type == user.ScheduleType.Group:
        pairs = schedule_db.schedule_group_query(schedule_id, day)
        text = format_schedule_group(pairs, day, schedule_id)
        print()
        answer = telebot.types.InlineQueryResultArticle(id='1',
                                                        title='Сегодня',
                                                        description=schedule_db.get_groups(id=schedule_id)[0]['group_name'],
                                                        input_message_content=telebot.types.InputTextMessageContent(
                                                            message_text=text, parse_mode='MARKDOWN'))
        bot.answer_inline_query(query.id, [answer])
    else:
        print('asds')


@bot.message_handler(commands=['start'])
def hello(message):
    """add user_of_bot into base"""
    usr = user.User(message)
    usr.set_state(state.states['StartMenu'])
    start_board = telebot.types.ReplyKeyboardMarkup()
    start_board.row('Подписаться на расписание')
    start_board.row('Подписаться на новости')
    start_board.row('Зайти в Таймлайн')
    start_board.row('В меню')
    bot.send_message(usr.chat_id,
                     '*Приветственное сообщение!!!* [О боте](telegra.ph/RGPPU-informer-bot-05-11)',
                     parse_mode='MARKDOWN',
                     reply_markup=start_board)


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['StartMenu'],
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
        sub_keyboard.row('Группа')
        sub_keyboard.row('Преподаватель')
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


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['Set_sub_schedule'],
                     content_types=['text'])
def sub_menu(message):
    """
    Sub schedule Handler
    """
    usr = user.User(message)
    if message.text == 'Группа':
        usr.set_state_data({"type": user.ScheduleType.Group})
        bot.send_message(usr.chat_id,
                         "Введите нужную вам группу, я попробую её найти.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == 'Преподаватель':
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
                    print(groups)
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
    elif (message.text == 'Отмена' and usr.get_sub_schedule() is not None):
        bot.send_message(usr.chat_id, 'Перехожу обратно в настройки', reply_markup=setting_kb(usr))
    else:
        bot.send_message(usr.chat_id, 'Я такого не ожидал, выберите пожалуйста пункт из списка')


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['Menu'],
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
        bot.send_message(usr.chat_id, important_links, parse_mode='MARKDOWN')

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


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['Settings'],
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
        bot.send_message(usr.chat_id, 'скоро добавлю мой дорогой пользователь')
        pass
    elif message.text == MENU:
        bot.send_message(usr.chat_id, 'Открываю меню', reply_markup=menu_kb(usr))
    else:
        bot.send_message(usr.chat_id, 'Выберите одну из предложенных вам команд')


@bot.message_handler(content_types=['text'],
                     func=lambda msg: user.User(msg).get_state() == state.states['Get_self_schedule_date'])
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


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['Get_timetable'],
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


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['Get_search_schedule_step1'])
def search_target(message):
    usr = user.User(message)
    if usr.get_state_data().keys():
        if 'type' in usr.get_state_data().keys():
            if usr.get_state_data()['type'] == user.ScheduleType.Classroom:
                classroom = schedule_db.get_classrooms(message.text)
                print(classroom)
                if classroom:
                    usr.set_state_data({'type': user.ScheduleType.Classroom,
                                        'schedule_id': classroom['classroom_id']})
                    bot.send_message(usr.chat_id, SELECT_INTERVAL+';', reply_markup=search_kb(usr))
                else:
                    bot.send_message(usr.chat_id, 'Я не смог найти такую аудиторию, попробуй ввести еще раз')
                print('aud')

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

                print('gr')


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['Get_search_schedule_step2'])
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
                text += schedule + '\n\n {0}\n'.format(SPLIT_WEEKS)
            else:
                text += schedule + '\n\n'
        bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN')
    elif message.text == TWO_WEEK:
        days = schedule_db.Days.days_from_today(15)
        text = ''
        for d in days:
            schedule = get_schedule(usr.get_state_data()['type'],
                                    usr.get_state_data()['schedule_id'],
                                    d)
            text += schedule
            if datetime.date.weekday(d) == 6:
                text += '\n\n {0}\n'.format(SPLIT_WEEKS)
            else:
                text += '\n\n'
        bot.send_message(usr.chat_id, text, parse_mode='MARKDOWN')
    elif message.text == MENU:
        bot.send_message(usr.chat_id, MENU_ENTER, reply_markup=menu_kb(usr))
    else:
        bot.send_message(usr.chat_id, SELECT_INTERVAL)


@bot.message_handler(func=lambda msg: user.User(msg).get_state() == state.states['Get_academic_buildings'],
                     content_types=['text'])
def get_academic_buildings(message):
    usr = user.User(message)
    if message.text == MENU:
        bot.send_message(usr.chat_id, MENU_ENTER, reply_markup=menu_kb(usr))
    else:
        for ab in academic_buildings:
            if message.text == ab[0]:
                text = ab[1]
                bot.send_message(usr.chat_id, text)
                break

        else:
            bot.send_message(usr.chat_id, "Я не знаю такого корпуса, выберите из списка")


@bot.message_handler(content_types=['text'])
def text_handler(message):
    bot.send_message(message.chat.id, 'оооопс, ты поломал меня, нажми /start и начни работу с начала, '
                                      'подписка сохранится, и доложи об этом автору, пусть чистит за собой косяки',
                     parse_mode='MARKDOWN')


if __name__ == '__main__':
    # set locale to send weekdays in RU format
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    print('run bot')
    bot.polling(none_stop=True)