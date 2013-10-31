#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import calendar
from datetime import date, datetime
import cgi
import feedparser
import urllib2
import shutil


_calendar = calendar.Calendar(0)

def getListOfWeeks(courseQuarter, courseYear):
    """
    Lista de semanas para cuatrimestre del curso que empieza en el año indicado.
    La lista es: [(n,w)]
       - n es el nº de semana en el cuatrimestre (vacío si no está en el cuatrimestre)
       - w es una lista de días de una semana
    """
    if courseQuarter == 1:
        listOfMonths = [(month,courseYear) for month in range(9,13)] + [(1,courseYear+1)]
    elif courseQuarter == 2:
        listOfMonths = [(month,courseYear) for month in range(1,6)]
    else:
        raise ValueError("Nº de cuatrimestre incorrecto: {0}".format(courseQuarter))
    rawListOfWeeks = []
    for (m,y) in listOfMonths:
        rawListOfWeeks.extend(_calendar.monthdatescalendar(y,m))

    #
    # @TODO Recuperar de la BBDD o servicio correspondiente las fechas de inicio y fin
    #       del cuatrimestre.
    #
    if courseQuarter == 1:
        firstWeek = 2
    elif courseQuarter == 2:
        firstWeek = 3

    weeks = []
    nWeek = 1 - firstWeek
    prevWeek = [None]
    for week in rawListOfWeeks:
        # Tal y como funciona monthdatscalendar, la última semana de un mes puede conicidir
        # con la primera del siguiente
        if prevWeek[0] == week[0]:    
            continue
        nWeek = nWeek + 1
        if nWeek > 0 and nWeek < 16:
            weeks.append((nWeek, week))
        else:
            weeks.append((None, week))
        prevWeek = week
    return weeks

def printCalendarRows(weeks):
    today = date.today()
    for (nWeek, week) in weeks:
        print "      <tr>"
        if nWeek:
            print "        <td>{0}</td>".format(str(nWeek))
        else:
            print "        <td></td>"
        for day in week:
            if day.day == 1:
                s = str(day.day) + " " + calendar.month_abbr[day.month]
            else:
                s = str(day.day)
            if day == today:
                attrs = " class=\"today\""
            else:
                attrs = ""
            print "        <td{0}>{1}</td>".format(attrs,s)
        print "      </tr>"

def sendError(msg):
    print """Status: 400 Bad Request
Content-type: text/html

<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>Solicitud con parámetros incorrectos</title>
  </head>
  <body>
    <p>Lo sentimos, pero no los datos del calendario solicitado no son correctos. {0}</p>
    <p><a href="/index.html">Volver a solicitar.</a></p>
  </body>
</html>
""".format(msg)
    exit()

def getUDCNoticiasFeed():
    feed = None
    CACHE_DIR = 'cache'
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    cacheFilename = os.path.join(CACHE_DIR, "udc-rss.xml")
    # ¿ Existe cache ?   ¿ Es de hace menos de 60*60 segundos ?
    if os.path.isfile(cacheFilename) and (time.mktime(datetime.now().timetuple()) - os.path.getmtime(cacheFilename) < 60*60):
        feed = feedparser.parse(cacheFilename)
    else:
        try:
            file = urllib2.urlopen("http://www.udc.es/rss/fontesRSS/principais/rss_comunicacion.xml", None, 2)
            if file.getcode() == 200:
                shutil.copyfileobj(file, open(cacheFilename, 'w'))
                feed = feedparser.parse(cacheFilename)
        except :
            pass
    return feed
        

calendarQuarter = None
calendarYear = None
form = cgi.FieldStorage()
try:
    calendarQuarter = int(form['cuatrimestre'].value)
except ValueError:
    sendError("El cuatrimestre especficidado: {0}, no es válido.".format(form['cuatrimestre'].value))
except KeyError:
    sendError("No se especifica el cuatrimestre.")

try:
    calendarYear = int(form['curso'].value)
except ValueError:
    sendError("El curso especficidado: año {0}, no es válido.".format(form['curso'].value))
except KeyError:
    sendError("No se especifica el curso.")

if calendarQuarter == 1:
    calendarQuarterName = "primer"
else:
    calendarQuarterName = "segundo"


calendarWeeks = getListOfWeeks(calendarQuarter, calendarYear)

print """Content-Type: text/html

<!doctype html>

<html lang="es">

  <head>
    <meta charset="utf-8"/>
    <title>[Calendario] Ejemplo de vista con html5+css3</title>
    <link rel="icon" type="image/png" href="/schedule.png" />
    <link href="/styles.css" rel="stylesheet" type="text/css" />
  </head>

  <body>
    <header>
      <h1>{0} cuatrimestre de {1}/{2}</h1>
    </header>

    <section id="main">
      <table class="calendar-weeks">
	<caption>{0} cuatrimestre del curso {1}/{2}</caption>
	<thead>
	  <tr>
	    <th scope="col"></th>
	    <th scope="col">Lun</th>
	    <th scope="col">Mar</th>
	    <th scope="col">Mié</th>
	    <th scope="col">Jue</th>
	    <th scope="col">Vie</th>
	    <th scope="col">Sáb</th>
	    <th scope="col">Dom</th>
	  </tr>
	</thead>
	<tbody>

""".format(calendarQuarterName.title(), str(calendarYear), str(calendarYear+1))

printCalendarRows(calendarWeeks)

print """
	</tbody>
      </table>
    </section>
"""

feed = getUDCNoticiasFeed()
if feed:
    feedTitle = feed.feed.title
else:
    feedTitle = "Noticias no disponibles"

print u"""
    <aside>
      <header>
	<h1>{0}</h1>
      </header>
""".format(feedTitle).encode('utf-8')

if feed:
    print "      <ul>"
    for entry in feed.entries:
        print u"<li><p>{0}</p>{1}</li>".format(entry.title, entry.description).encode('utf-8')
    print "      </ul>"

print """
    </aside>

  </body>

</html>
"""
