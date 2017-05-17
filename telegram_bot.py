import schedule_db
import state
import telebot
import config
import flask
import locale
import datetime
import end_user
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
[timeline](http://timeline.rsvpu.ru) - Информационная система 

[Электронная библиотека](http://umkd.rsvpu.ru) - Скачайте нужное вам методическое пособие

[Мои документы](http://www.rsvpu.ru/moi-dokumenty/) - Закажи любую справку в *одном* месте

[Об университете](http://www.rsvpu.ru/sveden/) - Сведения об образовательной организации
'''

primary_timetable = '''
`1️⃣  `1) 08:00 - 08:45
`        `2) 08:50 - 09:35

`2️⃣  `1) 09:45 - 10:30
`        `2) 10:35 - 11:20
`Перерыв 40 минут🍏` 
`3️⃣  `1) 12:00 - 12:45
`        `2) 12:50 - 13:35

`4️⃣  `1) 13:45 - 14:30
`        `2) 14:35 - 15:20

`5️⃣  `1) 15:30 - 16:15
`        `2) 16:20 - 17:05

`6️⃣  `1) 17:15 - 18:00
`        `2) 18:05 - 18:50

`7️⃣  `1) 19:00 - 19:45
`        `2) 19:50 - 20:35
'''

senior_timetable = '''
`1️⃣  `1) 08:00 - 08:45
`        `2) 08:50 - 09:35

`2️⃣  `1) 09:45 - 10:30
`        `2) 10:35 - 11:20
     
`3️⃣  `1) 11:30 - 12:15
`        `2) 12:20 - 13:05
`Перерыв 40 минут🍏`
`4️⃣  `1) 13:45 - 14:30
`        `2) 14:35 - 15:20

`5️⃣  `1) 15:30 - 16:15
`        `2) 16:20 - 17:05

`6️⃣  `1) 17:15 - 18:00
`        `2) 18:05 - 18:50

`7️⃣  `1) 19:00 - 19:45
`        `2) 19:50 - 20:35
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
                      ('Поркус 666', 'sssss'),
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
WEEK = 'Неделя 🕯'
TODAY = 'Сегодня ⌛️'
TOMORROW = 'Завтра ⏳'
MENU = 'В меню 🏠'
SENIOR_TIMETABLE = '3, 4 и 5 курсы'
PRIMARY_TIMETABLE = '1 и 2 курс'
ON_NEWS = 'Отключить новости❎️'
OFF_NEWS = 'Включить новости✅'
TIMELINE = 'timeline 📎'
SCHEDULE_SUB = 'Подписка на расписание'


def menu_kb(user)-> telebot.types.ReplyKeyboardMarkup:
    """Main menu keyboard"""
    user.set_state(state.states['Menu'])
    kb = telebot.types.ReplyKeyboardMarkup()
    kb.row(TODAY, TOMORROW)
    kb.row(WEEK, DATE)
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
        kb.row(OFF_NEWS)
    else:
        kb.row(ON_NEWS)
    kb.row(TIMELINE)
    kb.row(MENU)
    return kb


def search_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    """Search menu for user"""
    user.set_state(state.states['Get_search_schedule'])
    kb = telebot.types.ReplyKeyboardMarkup()
    kb.row(TODAY, TOMORROW)
    kb.row(WEEK, DATE)
    kb.row(MENU)
    return kb


def timetable_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    user.set_state(state.states['Get_timetable'])
    kb = telebot.types.ReplyKeyboardMarkup()
    kb.row(PRIMARY_TIMETABLE, SENIOR_TIMETABLE)
    kb.row(MENU)
    return kb


def sub_schedule_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    user.set_state(state.states['Set_sub_schedule'])
    kb = telebot.types.ReplyKeyboardMarkup()
    kb.row('Группа')
    kb.row('Преподаватель')
    kb.row('Отмена')
    return kb


def academic_buldings_kb(user) -> telebot.types.ReplyKeyboardMarkup:
    user.set_state(state.states['Get_academic_buildings'])
    kb = telebot.types.ReplyKeyboardMarkup()
    for ab in academic_buildings:
        print([ab][0][0])
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
                    target_audience = subject['subgroup_name']
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


def get_group(name=None, group_id=None) -> list:
    if name:
        result = schedule_db.get_groups(group_substr=name)
    elif group_id:
        result = schedule_db.get_groups(id=group_id)
    else:
        result = schedule_db.get_groups()
    return result


def get_self_schedule(user, day) -> str:
    schedule_sub = user.get_sub_schedule()
    if 'type' in schedule_sub.keys():
        if schedule_sub['type'] == end_user.ScheduleType.Teacher:
            pairs = schedule_db.schedule_teacher_query(schedule_sub['schedule_id'], day)
            text = format_schedule_teacher(pairs, day, schedule_sub['schedule_id'])
        else:
            pairs = schedule_db.schedule_group_query(schedule_sub['schedule_id'], day)
            text = format_schedule_group(pairs, day, schedule_sub['schedule_id'])
    else:
        text = 'Оформите подписку что бы получать расписание'
    return text
# here start bot's logic


@bot.inline_handler(func=lambda query: True)
def some_action(query):
    user = end_user.EndUser(query=query)
    schedule_type = user.get_sub_schedule()['type']
    schedule_id = user.get_sub_schedule()['schedule_id']
    day = schedule_db.Days.today()
    if schedule_type == end_user.ScheduleType.Teacher:
        pairs = schedule_db.schedule_teacher_query(schedule_id, day)
        text = format_schedule_group(pairs, day, schedule_id)
        answer = telebot.types.InlineQueryResultArticle(id='1',
                                                        title='Сегодня',
                                                        description=schedule_db.get_teachers(id=schedule_id)[0]['shortname'],
                                                        input_message_content=telebot.types.InputTextMessageContent(
                                                            message_text=text, parse_mode='MARKDOWN'))
        bot.answer_inline_query(query.id, [answer])
    elif schedule_type == end_user.ScheduleType.Group:
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
    user = end_user.EndUser(message)
    user.set_state(state.states['StartMenu'])
    start_board = telebot.types.ReplyKeyboardMarkup()
    start_board.row('Подписаться на расписание')
    start_board.row('Подписаться на новости')
    start_board.row('Зайти в timeline')
    start_board.row('В меню')
    bot.send_message(message.chat.id,
                     '*Приветственное сообщение!!!* [О боте](telegra.ph/RGPPU-informer-bot-05-11)',
                     parse_mode='MARKDOWN',
                     reply_markup=start_board)


@bot.message_handler(func=lambda msg: end_user.EndUser(msg).get_state() == state.states['StartMenu'],
                     content_types=['text'])
def start_menu(message):
    """
    Start menu Handler
    """
    # todo
    user = end_user.EndUser(message)
    if message.text == 'Подписаться на расписание':
        user.set_state(state.states['Set_sub_schedule'])
        sub_keyboard = telebot.types.ReplyKeyboardMarkup()
        sub_keyboard.row('Группа')
        sub_keyboard.row('Преподаватель')
        bot.send_message(message.chat.id, 'Выберите необходимый вам тип расписания: ',
                         reply_markup=sub_keyboard)
    elif message.text == 'Подписаться на новости':
        bot.send_message(message.chat.id, 'Вы подписались на новости. Отменить подписку можно в настройках',
                         reply_markup=menu_kb(user))
    elif message.text == 'Зайти в timeline':
        bot.send_message(message.chat.id, 'Временно не завезли =(')
    elif message.text == 'В меню':
        bot.send_message(message.chat.id, 'Открываю меню',
                         reply_markup=menu_kb(user))
    else:
        bot.send_message(message.chat.id, 'Че ты базаришь, я не понимаю!')


@bot.message_handler(func=lambda msg: end_user.EndUser(msg).get_state() == state.states['Set_sub_schedule'],
                     content_types=['text'])
def sub_menu(message):
    """
    Sub schedule Handler
    """
    user = end_user.EndUser(message)
    if message.text == 'Группа':
        user.set_state_data({"type": end_user.ScheduleType.Group})
        bot.send_message(message.chat.id,
                         "Введите нужную вам группу, я попробую её найти.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == 'Преподаватель':
        user.set_state_data({"type": end_user.ScheduleType.Teacher})
        bot.send_message(message.chat.id,
                         "Введите имя преподавателя, я попробую найти.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif 'type' in user.get_state_data().keys():
        state_data = user.get_state_data()
        if state_data['type'] == end_user.ScheduleType.Teacher:
            teachers = schedule_db.get_teachers(message.text)
            if len(teachers):
                if len(teachers) == 1:
                    user.set_sub_schedule(end_user.ScheduleType.Teacher, teachers[0]['teacher_id'])
                    user.set_state(state.states['Menu'])
                    bot.send_message(message.chat.id,
                                     "Поздравляю! Вы подписаны на расписание преподавателя!🎉",
                                     reply_markup=menu_kb(user))
                elif 1 < len(teachers) <= 25:
                    teachers_kb = telebot.types.ReplyKeyboardMarkup()
                    for teach in teachers:
                        teachers_kb.row(teach['fullname'])
                    bot.send_message(message.chat.id,
                                     'Выберите необходимого вам преподавателя',
                                     reply_markup=teachers_kb)
                else:
                    bot.send_message(message.chat.id,
                                     "Результат поиска получился слишком большой, попробуйте ввести запрос конктретнее",
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id, 'Я ничего не нашел, попробуйте ввести иначе.')
        elif state_data['type'] == end_user.ScheduleType.Group:
            groups = schedule_db.get_groups(message.text)
            if len(groups):
                if len(groups) == 1:
                    user.set_sub_schedule(end_user.ScheduleType.Group, groups[0]['group_id'])
                    user.set_state(state.states['Menu'])
                    bot.send_message(message.chat.id,
                                     "Поздравляю! Вы подписаны на группу {0}🎉".format(groups[0]['group_name']),
                                     reply_markup=menu_kb(user))
                elif 1 < len(groups) <= 15:
                    groups_kb = telebot.types.ReplyKeyboardMarkup()
                    print(groups)
                    for gr in groups:
                        groups_kb.row(gr['group_name'])
                    bot.send_message(message.chat.id,
                                     "Выберите из данного списка нужную вам группу, или введите заного,"
                                     " если я не нашел нужную вам группу.",
                                     reply_markup=groups_kb)
                else:
                    bot.send_message(message.chat.id,
                                     "Результат поиска получился слишком большой, попробуйте ввести запрос конктретнее",
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id, 'Я ничего не нашел, попробуйте ввести иначе.')
            pass
    elif (message.text == 'Отмена' and user.get_sub_schedule() is not None):
        bot.send_message(user.chat_id, 'Перехожу обратно в настройки', reply_markup=setting_kb(user))
    else:
        bot.send_message(message.chat.id, 'Я такого не ожидал, выберите пожалуйста пункт из списка')


@bot.message_handler(func=lambda msg: end_user.EndUser(msg).get_state() == state.states['Menu'],
                     content_types=['text'])
def main_menu(message):
    """
    Main menu
    """
    user = end_user.EndUser(message)
    if message.text == TODAY:
        text = get_self_schedule(user, schedule_db.Days.today())
        bot.send_message(message.chat.id, text, parse_mode='MARKDOWN')

    elif message.text == TOMORROW:
        text = get_self_schedule(user, schedule_db.Days.tomorrow())
        bot.send_message(message.chat.id, text, parse_mode='MARKDOWN')

    elif message.text == WEEK:
        schedule_sub = user.get_sub_schedule()
        days = schedule_db.Days.week()
        for day in days:
            text = get_self_schedule(user, day)
            bot.send_message(message.chat.id, text, parse_mode='MARKDOWN', disable_notification=True)

    elif message.text == DATE:
        canсel_kb = telebot.types.ReplyKeyboardMarkup()
        canсel_kb.row('Отмена')
        bot.send_message(message.chat.id,
                         'Введите необходимую вам дату в формате дд мм или дд месяц', reply_markup=canсel_kb)
        user.set_state(state.states['Get_self_schedule_date'])

    elif message.text == TIMETABLE:
        bot.send_message(message.chat.id,
                         'Выберите пункт',
                         reply_markup=timetable_kb(user))

    elif message.text == IMPORTANT_LINS:
        bot.send_message(message.chat.id, important_links, parse_mode='MARKDOWN')

    elif message.text == LOCATION_OF_BUILDINGS:
        # todo
        bot.send_message(message.chat.id, "Скоро я добавлю этот пункт, пока что не сделал карты",
                         reply_markup=academic_buldings_kb(user))
    elif message.text == SETTINGS:
        bot.send_message(message.chat.id, 'Выберите пункт', reply_markup=setting_kb(user))

    else:
        pass
        bot.send_message(message.chat.id, 'скоро так можно будет искать расписание на другие группы/преподавателей/аудитории')
        # todo
        # search schedule for all


@bot.message_handler(func=lambda msg: end_user.EndUser(msg).get_state() == state.states['Settings'],
                     content_types=['text'])
def setting(message):
    user = end_user.EndUser(message)
    if message.text == SCHEDULE_SUB:
        bot.send_message(user.chat_id, 'Выберите необходимый вам тип расписания', reply_markup=sub_schedule_kb(user))
    elif (message.text == ON_NEWS or message.text == OFF_NEWS):
        if user.get_sub_news():
            bot.send_message(user.chat_id, 'Подписка отменена', reply_markup=setting_kb(user))
        else:
            bot.send_message(user.chat_id, 'Я оповещу вас о свежих новостях', reply_markup=setting_kb(user))
        user.change_news()
        pass
    elif message.text == TIMELINE:
        # todo
        bot.send_message(user.chat_id, 'скоро добавлю мой дорогой пользователь')
        pass
    elif message.text == MENU:
        bot.send_message(user.chat_id, 'Открываю меню', reply_markup=menu_kb(user))
    else:
        bot.send_message('Выберите одну из предложенных вам команд')


@bot.message_handler(content_types=['text'],
                     func=lambda msg: end_user.EndUser(msg).get_state() == state.states['Get_self_schedule_date'])
def self_date_schedule(message):
    user = end_user.EndUser(message)
    if message.text != 'Отмена':
        try:
            try:
                date = datetime.datetime.strptime('{0} {1}'.format(message.text, datetime.datetime.today().year),
                                                  '%d %B %Y')
            except:
                date = datetime.datetime.strptime('{0} {1}'.format(message.text, datetime.datetime.today().year),
                                                  '%d %m %Y')
            text = get_self_schedule(user, date.date())
            bot.send_message(message.chat.id,
                             text,
                             parse_mode='MARKDOWN',
                             reply_markup=menu_kb(user))
        except:
            bot.send_message(message.chat.id, 'Я не смог найти такую дату =(, введи дату заново')
    else:
        bot.send_message(message.chat.id, 'Открываю меню', reply_markup=menu_kb(user))


@bot.message_handler(func=lambda msg: end_user.EndUser(msg).get_state() == state.states['Get_timetable'],
                     content_types=['text'])
def timetable(message):
    user = end_user.EndUser(message)
    if message.text == PRIMARY_TIMETABLE:
        bot.send_message(message.chat.id, primary_timetable, reply_markup=menu_kb(user), parse_mode='MARKDOWN')
    elif message.text == SENIOR_TIMETABLE:
        bot.send_message(message.chat.id, senior_timetable, reply_markup=menu_kb(user), parse_mode='MARKDOWN')
    elif message.text == MENU:
        bot.send_message(message.chat.id, 'Открываю меню', reply_markup=menu_kb(user))
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда')


@bot.message_handler(func=lambda msg: end_user.EndUser(msg).get_state() == state.states['Get_academic_buildings'],
                     content_types=['text'])
def get_academic_buildings(message):
    user = end_user.EndUser(message)
    print(message)
    if message.text == MENU:
        bot.send_message(user.chat_id, 'Перехожу в Меню', reply_markup=menu_kb(user))
    else:
        for ab in academic_buildings:
            print(ab[0])
            if message.text == ab[0]:
                text = ab[1]
                bot.send_message(user.chat_id, text)
                break

        else:
            bot.send_message(user.chat_id, "Я не знаю такого корпуса, выберите из списка")


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

