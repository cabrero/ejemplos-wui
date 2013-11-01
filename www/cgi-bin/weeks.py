#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import json
import calendar
import datetime
import time

def send_error(msg):
    body = json.dumps({'data': {'error': msg}})
    print """Status: 400 Bad Request
Content-type: application/json
Content-length: {0}
""".format(len(body)).encode('utf-8')
    print body
    exit()

form = cgi.FieldStorage()
cuatrimestre = None
curso = None
if form.has_key('cuatrimestre'):
    cuatrimestre = form['cuatrimestre'].value
if form.has_key('curso'):
    curso = form['curso'].value

try:
    year = int(curso)
except (ValueError, TypeError):
    send_error(u"El año no es válido.")

if cuatrimestre == "1":
    months = [(month,year) for month in range(9,13)] + [(1,year+1)]
    cuatrimestreOrdinal = "primer"
elif cuatrimestre == "2":
    months = [(month,year+1) for month in range(1,6)]
    cuatrimestreOrdinal = "segundo"
else:
    send_error("El cuatrimestre no es válido.")

cal = calendar.Calendar(0)
today = datetime.date.today()
weeks = []
for (month,y) in months:
    weeks.extend(cal.monthdatescalendar(y, month))

dias = []
week = -1
prevweek = [None]
for week in weeks:
    if prevweek[0] == week[0]:
        continue
    for date in week:
        dias.append({'date': date.isoformat()})
    prevweek = week

body = json.dumps({'data': { 'cuatrimestre': cuatrimestre, 'curso': curso,
                             'dayNames': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                             'dayList': dias } })

# Cabecera
print "Content-Type: application/json"
print "Content-Length: {0}".format(len(body))
print ""
print body

