# /usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import copy
from datetime import datetime, timedelta
from icalendar import Calendar, Event

isDEBUG = 0
friendlyName = {
    "zcd": "lengthAndJump",
    "xqj": "date",
    "jcor": "time",
    "kcmc": "summary",
    "cdmc": "location",
    "xm": "teacher",
    "jxbrs": "menber",
    "khfsmc": "examtype",
}
classBegintime = {
    1: [8, 20],
    3: [10, 20],
    5: [14, 30],
    7: [16, 30],
    9: [19, 00]
}


class WhenWhoWhere:
    """Storage environment variables, which semester, which class and which school"""

    year = '18-19'
    semester = '第一学期'
    ssalc = '一班'  # ssalc is r'class'
    grand = '16级'
    major = '软件工程'
    college = '数据科学与软件工程学院'
    university = '保定学院'
    firstDay = datetime.strptime('2018-09-03', "%Y-%m-%d")

    def __init__(self):
        pass

    def genname(self):
        return '18-19·第一学期·一班·16级·软件工程·数据科学与软件工程学院·保定学院'


env = WhenWhoWhere()
with open('/Users/siyang/kb_tem.json', 'r') as kb_file:
    kb_raw = json.load(kb_file)

temForOneClass = {"": ""}
lessons = []

for cla in kb_raw["kbList"]:
    temForOneClass.clear()
    for i in friendlyName:
        temForOneClass[friendlyName[i]] = cla[i]
    lessons.append(copy.deepcopy(temForOneClass))

if (isDEBUG):
    with open('/tmp/lesson.json', 'w') as f:
        f.write(json.dumps(lessons))

wholeiCal = Calendar()

wholeiCal.add("prodid", "-//Siyang Zhang//ZhengFang 2017 iCal Builder 1.0//CN")
wholeiCal.add("X-WR-CALNAME", "{}课表".format(env.genname()))
wholeiCal.add("X-WR-TIMEZONE", "Asia/Shanghai")

temForEvent = Event()
for lesson in lessons:
    del temForEvent
    temForEvent = Event()
    temForEvent.add('summary', lesson['summary'])
    lessonBeginTime = env.firstDay + timedelta(hours=classBegintime[int(lesson['time'][0:1])][0],
                                               minutes=classBegintime[int(lesson['time'][0:1])][1],
                                               days=(int(lesson['date']) - 1))
    lengthAndDanshuangZhou = lesson['lengthAndJump'].split('周')
    lengtha = lengthAndDanshuangZhou[0].split('-')
    if (lengthAndDanshuangZhou[1] != ''):
        temForEvent.add('RRULE',
                        {'FREQ': 'WEEKLY', 'COUNT': str(int((int(lengtha[1]) - int(lengtha[0])) / 2 + 1)),
                         'INTERVAL': '2'})
        if ('双' in lengthAndDanshuangZhou[1]):
            lessonBeginTime = lessonBeginTime + timedelta(weeks=1)
    else:
        temForEvent.add('RRULE',
                        {'FREQ': 'WEEKLY', 'COUNT': str(int((int(lengtha[1]) - int(lengtha[0])) + 1)),
                         'INTERVAL': '1'})
    temForEvent.add('dtstart', lessonBeginTime, parameters={'TZID': 'Asia/Shanghai'})
    temForEvent.add('dtend', lessonBeginTime + timedelta(minutes=100), parameters={'TZID': 'Asia/Shanghai'})
    temForEvent.add('location', lesson['location'])
    temForEvent.add('description', lesson['teacher'] + "~" + lesson['menber'] + "人~" + lesson['examtype'])
    wholeiCal.add_component(copy.deepcopy(temForEvent))

with open('classTable.ics', 'wb') as f:
    f.write(wholeiCal.to_ical())
