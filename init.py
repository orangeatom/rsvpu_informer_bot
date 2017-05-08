from bs4 import BeautifulSoup
import requests
from models import *
from telegram_bot import localbase

# FIXME more than 70% of this will be deleted when I gor a query for a groups
schedule_url_full_day = 'http://www.rsvpu.ru/raspisanie-zanyatij-ochnoe-otdelenie/'
schedule_url_half_day = 'http://www.rsvpu.ru/racpisanie-zanyatij-zaochnoe-otdelenie/'


def validate_option(opt):
    text = opt.text.lower()
    if 'вакан' in text or 'выберите' in text:
        return False
    else:
        return True


def get_info(soup, text):
    container = {}
    box = soup.find(id=text)
    for opt in box.find_all('option'):
        if(validate_option(opt)):
            container[opt.text] = opt['value']
    return container


def update_links():
    dictionary = {}
    site = requests.get(schedule_url_full_day)
    site.encoding = 'utf-8'
    soup = BeautifulSoup(site.text, 'html.parser')
    dictionary['groups_full_day'] = get_info(soup, 'get_group')
    dictionary['teachers'] = get_info(soup, 'fprep')

    site = requests.get(schedule_url_half_day)
    site.encoding = 'utf-8'
    soup = BeautifulSoup(site.text, 'html.parser')
    dictionary['groups_half_day'] = get_info(soup, 'get_group')
    return dictionary


print('creation tables')
try:
    localbase.drop_tables([GroupFullDay, GroupHalfDay, Teacher])
except:
    pass
localbase.create_tables([GroupFullDay, GroupHalfDay, Teacher], safe=True)
localbase.create_table(User)
localbase.close()

schedule_id = update_links()

groups_full_day, groups_half_day, teachers = schedule_id['groups_full_day'], \
                                             schedule_id['groups_half_day'], \
                                             schedule_id['teachers']


print('fill fields of groups full day')
for group in groups_full_day:
    GR = GroupFullDay.create(group_id=groups_full_day[group], group_name=group)
    GR.save()


print('fill fields of groups half day')
for group in groups_half_day:
    GR = GroupHalfDay.create(group_id=groups_half_day[group], group_name=group)
    GR.save()


print('fill fields of teachers')
for teacher in teachers:
    TC = Teacher.create(teacher_id=teachers[teacher], teacher_name=teacher)
    TC.save()
print('complete!')
