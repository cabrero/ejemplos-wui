UDC_Calendar = function (data, dayNames) {

    var _data = data;
    var _dayNames = dayNames;
    console.log("[calendario] Inicio.");
    updateCalendar(data);
    document.querySelector('#dialog form').addEventListener('submit', onSubmit, false);

    function ordinal(n) {
	return n ==1 ? "primer" : "segundo";
    }
    function capitalize(s) {
	return s[0].toUpperCase() + s.slice(1);
    }

    function createCalendarTable(data) {
	var table = document.createElement('table');
	table.className = 'calendar-weeks';
	var caption = document.createElement('caption');
	caption.appendChild(document.createTextNode("Calendario del "+ ordinal(data.cuatrimestre) +" cuatrimestre del curso "+data.curso +"/"+data.curso+1));
	table.appendChild(caption);
	var thead = document.createElement('thead');
	var tr = document.createElement('tr');
	var th = document.createElement('th');
	th.scope="col";
	th.appendChild(document.createTextNode(""));
	tr.appendChild(th);
	for (var i=0; i<dayNames.length; i++) {
	    th = document.createElement('th');
	    th.scope="col";
	    th.appendChild(document.createTextNode(dayNames[i]));
	    tr.appendChild(th);
	}
	thead.appendChild(tr);
	table.appendChild(thead);
	table.appendChild(createCalendarTBody(data));
	return table;
    }

    function createCalendarTBody(data) {
	var today = new Date();
	var tbody = document.createElement('tbody');
	var tr = document.createElement('tr');
	var nweek = -1;
	var td;
	for(var i=0; i<data.dayList.length; i++) {
	    if ((i % 7) == 0) {
		td = document.createElement('td');
		td.appendChild(document.createTextNode(((nweek > 0) && (nweek <16)) ? nweek.toString() : ""));
		tr.appendChild(td);
	    }
	    td = document.createElement('td');
	    var date = new Date(data.dayList[i].date);
	    if ((date.getDate() == today.getDate()) && (date.getMonth() == today.getMonth()) &&
		(date.getFullYear() == today.getFullYear())) {
		td.className = 'today';
	    }
	    td.appendChild(document.createTextNode(date.getDate().toString()));
	    tr.appendChild(td);
	    if ((i % 7) == 6) {
		nweek = nweek + 1;
		tbody.appendChild(tr);
		tr = document.createElement('tr');
	    }
	}
	return tbody;
    }

    function onSubmit(e) {
	console.log("onSubmit");
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/cgi-bin/weeks.py', true);
	xhr.onload = function (e) {
	    if (this.status == 200) {
		var response = JSON.parse(this.response);
		updateCalendar(response.data);
	    }
	}
	var formData = new FormData(e.target);
	xhr.send(formData);
	window.location.href= "#";
	e.preventDefault();
    }

    function updateCalendar(data) {
	var oldH1A = document.querySelector('body > header h1 a');
	var newH1A = document.createElement('a');
	newH1A.href = oldH1A.href;
	newH1A.appendChild(document.createTextNode(capitalize(ordinal(data.cuatrimestre)) + " cuatrimestre del curso "+ data.curso+"/"+data.curso+1));
	oldH1A.parentNode.replaceChild(newH1A, oldH1A);
	var oldCalendar = document.querySelector('#main table');
	oldCalendar.parentNode.replaceChild(createCalendarTable(data), oldCalendar);
    }

}
