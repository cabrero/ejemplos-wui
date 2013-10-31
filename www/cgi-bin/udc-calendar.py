#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
from datetime import date
import cgi

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


    <aside>
      <header>
	<h1>Contenido adicional</h1>
      </header>
      <ul>
	<li><p> Lorem ipsum dolor sit amet, consectetur adipiscing
	    elit. Morbi consectetur, felis et blandit egestas, turpis
	    magna dapibus leo, non ullamcorper tortor justo vel
	    turpis. Nullam id sagittis libero, eu facilisis
	    felis. Duis a faucibus libero. Vestibulum pharetra id
	    tellus vitae fermentum. Quisque ut pulvinar enim. Nam
	    auctor molestie imperdiet. Nulla cursus justo eu tempor
	    accumsan. Donec euismod a turpis vel adipiscing. Morbi
	    commodo ante nec feugiat fringilla. Pellentesque facilisis
	    purus eu magna viverra consequat. Nulla tortor dui,
	    commodo vitae ipsum tincidunt, consectetur blandit
	    metus. Donec eu dui euismod, molestie eros et, euismod
	    purus. Fusce tellus felis, ullamcorper non justo sed,
	    porttitor accumsan eros. Pellentesque habitant morbi
	    tristique senectus et netus et malesuada fames ac turpis
	    egestas.
	</p></li>
	<li><p> In viverra, ante ac placerat sollicitudin, ante diam
	    laoreet justo, suscipit rhoncus metus turpis a
	    magna. Interdum et malesuada fames ac ante ipsum primis in
	    faucibus. Nulla facilisi. Duis accumsan est vel congue
	    consectetur. Praesent pellentesque euismod massa, sed
	    scelerisque justo consectetur suscipit. Nunc a mollis
	    arcu, eu eleifend justo. Proin sodales lectus sed turpis
	    commodo, eget adipiscing arcu consectetur. Curabitur et
	    augue in urna porta condimentum sit amet in lorem. Proin
	    tincidunt velit neque, bibendum euismod mi semper sit
	    amet. In pulvinar leo volutpat turpis auctor vestibulum.
	</p></li>
      </ul>
    </aside>

  </body>

</html>
"""
