import schedule_db
import state
import telebot
import config
import flask
import locale
import datetime
import end_user

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

important_links = '''
[timeline](http://timeline.rsvpu.ru) - Информационная система 

[Электронная библиотека](http://umkd.rsvpu.ru) - Скачайте нужное вам методическое пособие

[Мои документы](http://www.rsvpu.ru/moi-dokumenty/) - Закажи любую справку в *одном* месте

[Об университете](http://www.rsvpu.ru/sveden/) - Сведения об образовательной организации
'''

primary_timetable = '''
*I*    1) 08:00 - 08:45
     2) 08:50 - 09:35

*II*   1) 09:45 - 10:30
     2) 10:35 - 11:20

*Перерыв 40 минут*

*III*  1) 12:00 - 12:45
     2) 12:50 - 13:35

*IV*  1) 13:45 - 14:30
     2) 14:35 - 15:20

*V*   1) 15:30 - 16:15
     2) 16:20 - 17:05

*VI*  1) 17:15 - 18:00
     2) 18:05 - 18:50

*VII* 1) 19:00 - 19:45
     2) 19:50 - 20:35
'''

senior_timetable = '''
*I*    1) 08:00 - 08:45
     2) 08:50 - 09:35

*II*   1) 09:45 - 10:30
     2) 10:35 - 11:20
     
*III*  1) 11:30 - 12:15
     2) 12:20 - 13:05
*Перерыв 40 минут*
*IV*  1) 13:45 - 14:30
     2) 14:35 - 15:20

*V*   1) 15:30 - 16:15
     2) 16:20 - 17:05

*VI*  1) 17:15 - 18:00
     2) 18:05 - 18:50

*VII* 1) 19:00 - 19:45
     2) 19:50 - 20:35
'''


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

# here start bot's logic


@bot.inline_handler(func=lambda query: len(query.query)>0)
def some_action(query):
    pass


@bot.message_handler(commands=['start'])
def hello(message):
    """add user_of_bot into base"""
    # todo create user_of_bot, and set his state on 'imagine value'
    user = end_user.EndUser(message.chat.id)
    user.set_state(state.states['StartMenu'])
    start_board = telebot.types.ReplyKeyboardMarkup()
    start_board.row('Подписаться на расписание')
    start_board.row('Подписаться на новости')
    start_board.row('Зайти в timeline')
    start_board.row('В меню')
    bot.send_message(message.chat.id,
                     '*Hello nigga* [О боте](telegra.ph/RGPPU-informer-bot-05-11)',
                     parse_mode='MARKDOWN',
                     reply_markup=start_board)


@bot.message_handler(func=lambda msg: end_user.EndUser(msg.chat.id).get_state() == state.states['StartMenu'], content_types=['text'])
def main_menu(message):
    """
    Start menu Handler
    """
    user = end_user.EndUser(message.chat.id)
    if message.text == 'Подписаться на расписание':
        user.set_state(state.states['Set_sub_schedule'])
        sub_keyboard = telebot.types.ReplyKeyboardMarkup()
        sub_keyboard.row('Группа')
        sub_keyboard.row('Преподаватель')
        bot.send_message(message.chat.id, 'Выберите необходимый вам тип расписания: ', reply_markup=sub_keyboard)
    elif message.text == 'Подписаться на новости':
        pass
    elif message.text == 'Зайти в timeline':
        bot.send_message(message.chat.id, '3')
    elif message.text == 'В меню':
        bot.send_message(message.chat.id, '4')
    else:
        bot.send_message(message.chat.id, 'Че ты базаришь, я не понимаю!')


@bot.message_handler(func=lambda msg: end_user.EndUser(msg.chat.id).get_state() == state.states['Set_sub_schedule'], content_types=['text'])
def sub_menu(message):
    """
    Sub schedule Handler
    """
    user = end_user.EndUser(message.chat.id)
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
                    user.set_sub_schedule(end_user.ScheduleType.Group, teachers[0]['group_id'])
                    user.set_state(state.states['Menu'])
                    bot.send_message(message.chat.id,
                                     "Поздравляю! Вы подписаны на группу {0}🎉".format(teachers[0]['group_name']))
                if 1 < len(teachers) <= 25:
                    for teach in teachers:
                        teachers_kb = telebot.types.ReplyKeyboardMarkup()
                        teachers_kb.row(teach['fullname'])
                else:
                    pass
            else:
                bot.send_message(message.chat.id, 'Я ничего не нашел, попробуйте ввести иначе.')
        elif state_data['type'] == end_user.ScheduleType.Group:
            groups = schedule_db.get_groups(message.text)
            if len(groups):
                if len(groups) == 1:
                    user.set_sub_schedule(end_user.ScheduleType.Group, groups[0]['group_id'])
                    user.set_state(state.states['Menu'])
                    bot.send_message(message.chat.id, "Поздравляю! Вы подписаны на группу {0}🎉".format(groups[0]['group_name']))
                elif 1 < len(groups) <= 15:
                    groups_kb = telebot.types.ReplyKeyboardMarkup()
                    print(groups)
                    for gr in groups:
                        groups_kb.row(gr['group_name'])
                    bot.send_message(message.chat.id,
                                     "Выберите из данного списка нужную вам группу, или введите заного, если я не нашел нужную вам группу.",
                                     reply_markup=groups_kb)
                else:
                    bot.send_message(message.chat.id,
                                     "Результат поиска получился слишком большой, попробуйте ввести запрос конктретнее",
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id, 'Я ничего не нашел, попробуйте ввести иначе.')
            pass
    else:
        bot.send_message(message.chat.id, 'Я такого не ожидал, выберите пожалуйста пункт из списка')


@bot.message_handler(func=lambda msg: end_user.EndUser(msg.chat.id).get_state() == state.states['Menu'], content_types=['text'])
def sub_menu(message):
    """
    Sub schedule Handler
    """

@bot.message_handler(content_types=['text'])
def text_handler(message):

    bot.send_message(message.chat.id, important_links, parse_mode='MARKDOWN')

if __name__ == '__main__':
    # set locale to send weekdays in RU format
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    print('run bot')
    bot.polling(none_stop=True)

