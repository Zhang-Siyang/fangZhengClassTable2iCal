# /usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import copy
from datetime import datetime, timedelta
from icalendar import Calendar, Event

isDEBUG = 0

kbSourceJson = '/Users/siyang/kb_tem.json'  # 抓包存放位置

friendlyName = {  # 翻译一下鬼畜级别的字段名
    "zcd": "lengthAndJump",
    "xqj": "date",
    "jcor": "time",
    "kcmc": "summary",
    "cdmc": "location",
    "xm": "teacher",
    "jxbrs": "number",
    "khfsmc": "examtype",
}
classBegintime = {  # 各节课开始时间
    1: [8, 20],
    3: [10, 20],
    5: [14, 30],
    7: [16, 30],
    9: [19, 00]
}


class WhenWhoWhere:
    """Storage environment variables, which semester, which class and which school"""

    firstDay = datetime.strptime('2018-09-03', "%Y-%m-%d")  # 第一周周一

    def __init__(self):
        pass

    def genname(self):
        return '18-19·第一学期·一班·16级·软件工程·AAAA学院·BBBB'


env = WhenWhoWhere()
with open(kbSourceJson, 'r') as kb_file:
    kb_raw = json.load(kb_file)  # 载入课程列表

temForOneClass = {"": ""}  # 临时存储(友好字段名下的)一节课
lessons = []  # 存储所有课程

for cla in kb_raw["kbList"]:
    temForOneClass.clear()
    for i in friendlyName:
        temForOneClass[friendlyName[i]] = cla[i]
    lessons.append(copy.deepcopy(temForOneClass))

if (isDEBUG):
    with open('/tmp/lesson.json', 'w') as f:
        f.write(json.dumps(lessons))  # 输出所有课程信息

wholeiCal = Calendar()

wholeiCal.add("prodid", "-//Siyang Zhang//ZhengFang 2017 iCal Builder 1.0//CN")
wholeiCal.add("X-WR-CALNAME", "{}课表".format(env.genname()))
wholeiCal.add("X-WR-TIMEZONE", "Asia/Shanghai")  # 时区

temForEvent = Event()
for lesson in lessons:
    del temForEvent
    temForEvent = Event()
    temForEvent.add('summary', lesson['summary'])  # 课程名
    lessonBeginTime = env.firstDay + timedelta(days=(int(lesson['date']) - 1),  # 周几的课
                                               hours=classBegintime[int(lesson['time'][0:1])][0],
                                               minutes=classBegintime[int(lesson['time'][0:1])][1]
                                               )
    lengthAndDanshuangZhou = lesson['lengthAndJump'].split('周')
    beginAndEndOfClass = lengthAndDanshuangZhou[0].split('-')  # 存储课程起止周数
    if lengthAndDanshuangZhou[1] != '':  # 如果周后面有字，说明分了单双周
        temForEvent.add('RRULE',
                        {'FREQ': 'WEEKLY',
                         'COUNT': str(int((int(beginAndEndOfClass[1]) - int(beginAndEndOfClass[0])) / 2 + 1)),
                         'INTERVAL': '2'})  # 课程每双周重复
        if '双' in lengthAndDanshuangZhou[1]:
            lessonBeginTime = lessonBeginTime + timedelta(weeks=1)
    else:
        temForEvent.add('RRULE',
                        {'FREQ': 'WEEKLY',
                         'COUNT': str(int((int(beginAndEndOfClass[1]) - int(beginAndEndOfClass[0])) + 1)),
                         'INTERVAL': '1'})
    temForEvent.add('dtstart', lessonBeginTime, parameters={'TZID': 'Asia/Shanghai'})
    temForEvent.add('dtend', lessonBeginTime + timedelta(minutes=100), parameters={'TZID': 'Asia/Shanghai'})
    temForEvent.add('location', lesson['location'])
    temForEvent.add('description', lesson['teacher'] + "~" + lesson['number'] + "人~" + lesson['examtype'])
    wholeiCal.add_component(copy.deepcopy(temForEvent))

with open('classTable.ics', 'wb') as f:
    f.write(wholeiCal.to_ical())  # 写入文件
