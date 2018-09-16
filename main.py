# /usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import datetime
import copy
from icalendar import Calendar, Event, vTime

isDEBUG = 1

friendlyName = {
    "zcd": "lengthAndJump",
    "xqj": "date",
    "jcor": "time",
    "kcmc": "name",
    "cdmc": "location",
    "xm": "teacher",
    "jxbrs": "menber",
    "khfsmc": "examtype",
}

with open('/Users/siyang/kb_tem.json', 'r') as kb_file:
    kb_raw = json.load(kb_file)

temForOneClass = {"": ""}
allClassBaseJson = []

for cla in kb_raw["kbList"]:
    temForOneClass.clear()
    for i in friendlyName:
        temForOneClass[friendlyName[i]] = cla[i]
    allClassBaseJson.append(copy.deepcopy(temForOneClass))

wholeiCal = Calendar()

wholeiCal.add("prodid", "-//Siyang Zhang//ZhengFang 2017 iCal Builder 1.0//CN")
wholeiCal.add("version", "2.0")
wholeiCal.add("X-WR-CALNAME", "保定学院·数计系·16级·软件工程·一班·18-19·第一学期课表")  # TODO
wholeiCal.add("X-WR-TIMEZONE", "Asia/Shanghai")

print(wholeiCal.to_ical())
exit(0)
for cla in allClassBaseJson:
    ev = Event()
    ev.add("DTSTART", datetime.time)
