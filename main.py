# /usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import copy
from datetime import datetime, timedelta
from icalendar import Calendar, Event

# Config:
spot = datetime.strptime('2019-05-01', "%Y-%m-%d")
kbSourceJson = 'tem.json'  # 抓包存放位置
firstDay = datetime.strptime('2019-02-25', "%Y-%m-%d")  # 第一周周一
iCalTitle = '18-19·第二学期·一班·16级·软件工程·学院·大学'
timeTable = [{
    1: [8, 20],
    3: [10, 20],
    5: [14, 30],
    7: [16, 30],
    9: [19, 00]}, {1: [8, 20],
                   3: [10, 20],
                   5: [14, 00],
                   7: [16, 00],
                   9: [18, 30]
                   }]  # 两个时刻表，春夏和秋冬

friendlyName = {  # 翻译一下鬼畜级别的字段名
    "kcmc": "summary",
    "xqj": "date",
    "jcor": "time",
    "cdmc": "location",
    "zcd": "lengthAndJump",
    "xm": "teacher",
    "jxbrs": "number",
    "khfsmc": "examtype",
}


class Class:
    '用于表示一门课的类'

    def __init__(self, classWithJson):
        for k, v in friendlyName.items():
            setattr(self, '__' + v, classWithJson[k])

    def __str__(self):
        result = ''
        for k, v in friendlyName.items():
            result += '{} is {}\n'.format(v, getattr(self, '__' + v))
        return result

    def getOneVer(self, name):
        if hasattr(self, '__' + name):
            return getattr(self, '__' + name)
        else:
            return None


class iCalBuilder:
    """课表iCal生成器"""
    Version = "-//Siyang Zhang//ZhengFang 2017 iCal Builder 1.0//CN"
    timeZone = "Asia/Shanghai"

    def __init__(self):
        self.__iCal = Calendar()
        self.__iCal.add("prodid", self.Version)
        self.__iCal.add("X-WR-CALNAME", "{}课表".format(iCalTitle))
        self.__iCal.add("X-WR-TIMEZONE", self.timeZone)

    def add_one_class(self, ClassAsClass: Class):
        tem_for_event = Event()
        tem_for_event.add('summary', ClassAsClass.getOneVer('summary'))
        delay_time = timedelta(days=int(ClassAsClass.getOneVer('date')) - 1)  # 周几的课

        if firstDay + delay_time >= spot:
            delay_time += timedelta(hours=timeTable[0][int(ClassAsClass.getOneVer('time')[0:1])][0],
                                    minutes=timeTable[0][int(ClassAsClass.getOneVer('time')[0:1])][1])
        else:
            delay_time += timedelta(hours=timeTable[1][int(ClassAsClass.getOneVer('time')[0:1])][0],
                                    minutes=timeTable[1][int(ClassAsClass.getOneVer('time')[0:1])][1])
        lessonBeginTime = delay_time + firstDay
        lengthAndDanshuangZhou = ClassAsClass.getOneVer('lengthAndJump').split('周')
        beginAndEndOfClass = lengthAndDanshuangZhou[0].split('-')  # 存储课程起止周数
        if lengthAndDanshuangZhou[1] != '':  # 如果周后面有字，说明分了单双周
            tem_for_event.add('RRULE',
                              {'FREQ': 'WEEKLY',
                               'COUNT': str(int((int(beginAndEndOfClass[1]) - int(beginAndEndOfClass[0])) / 2 + 1)),
                               'INTERVAL': '2'})  # 课程每双周重复
            if '双' in lengthAndDanshuangZhou[1]:
                lessonBeginTime = lessonBeginTime + timedelta(weeks=1)
        else:
            tem_for_event.add('RRULE',
                              {'FREQ': 'WEEKLY',
                               'COUNT': str(int((int(beginAndEndOfClass[1]) - int(beginAndEndOfClass[0])) + 1)),
                               'INTERVAL': '1'})
        class_length = 100  # min
        tem_for_event.add('dtstart', lessonBeginTime, parameters={'TZID': self.timeZone})
        tem_for_event.add('dtend', lessonBeginTime + timedelta(minutes=class_length),
                          parameters={'TZID': self.timeZone})
        tem_for_event.add('location', ClassAsClass.getOneVer('location'))
        tem_for_event.add('description', ClassAsClass.getOneVer('teacher') + "~" + ClassAsClass.getOneVer(
            'number') + "人~" + ClassAsClass.getOneVer('examtype'))
        self.__iCal.add_component(copy.deepcopy(tem_for_event))

    def to_ical(self):
        return self.__iCal.to_ical()


if __name__ == '__main__':

    with open(kbSourceJson, 'r') as kb_file:
        kb_raw = json.load(kb_file)  # 载入课程列表

    semester = iCalBuilder()
    for cla in kb_raw["kbList"]:
        tem_for_one_class = Class(cla)
        semester.add_one_class(tem_for_one_class)

    with open('classTable.ics', 'wb') as f:
        f.write(semester.to_ical())  # 写入文件
