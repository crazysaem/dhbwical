from bs4 import BeautifulSoup
import urllib

def convertstring(str):
	str = str.replace(u"\xe4", "ae")
	str = str.replace(u"\xc4", "Ae")
	str = str.replace(u"\xf6", "oe")
	str = str.replace(u"\xd6", "Oe")
	str = str.replace(u"\xfc", "ue")
	str = str.replace(u"\xdc", "Ue")
	str = str.replace(u"\xdf", "ss")
	return str

link = 'http://vorlesungsplan.dhbw-mannheim.de/index.php?action=view&gid=3067001&uid=3865001&date=1346623200'
ical = open("tai10abc.ics", "w")
#uncomment to use a proxy
#proxies = {'http': 'http://PROXY_URL:PROXY_PORT'}
ical.write("BEGIN:VCALENDAR\n")
ical.write("METHOD:PUBLISH\n")
ical.write("PRODID:-//crzy//iCal 3.0//EN\n")
ical.write("CALSCALE:GREGORIAN\n")
ical.write("X-WR-CALNAME:TAI10ABC\n")
ical.write("X-WR-TIMEZONE:Europe/Berlin\n")
ical.write("VERSION:2.0\n")
ical.write("BEGIN:VTIMEZONE\n")
ical.write("TZID:Europe/Berlin\n")
ical.write("BEGIN:DAYLIGHT\n")
ical.write("TZOFFSETFROM:+0100\n")
ical.write("TZOFFSETTO:+0200\n")
ical.write("DTSTART:19810329T020000\n")
ical.write("RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\n")
ical.write("TZNAME:CEST\n")
ical.write("END:DAYLIGHT\n")
ical.write("BEGIN:STANDARD\n")
ical.write("TZOFFSETFROM:+0200\n")
ical.write("TZOFFSETTO:+0100\n")
ical.write("DTSTART:19961027T030000\n")
ical.write("RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\n")
ical.write("TZNAME:CET\n")
ical.write("END:STANDARD\n")
ical.write("END:VTIMEZONE\n")

for weeks in range(12):
	#html = urllib.urlopen(link, proxies=proxies)
	html = urllib.urlopen(link)
	soup = BeautifulSoup(html)
	weekdays = soup.find_all('ul')

	for weekday in weekdays:
		month = weekday.li.text[-2:]
		day = weekday.li.text[-5:]
		day = day[:2]
		date = "2012%s%s" % (month, day)
		for appointment in weekday.find_all('li'):
			if len(appointment)>1:
				ical.write("BEGIN:VEVENT\n")
				properties = appointment.find_all('div')
				starttime = properties[0].text[:2] + properties[0].text[:5][-2:]
				endtime = properties[0].text[:8][-2:] + properties[0].text[:11][-2:]
				description = properties[1].text
				location = properties[2].text
				
				location = convertstring(location)
				description = convertstring(description)
				
				ical.write("LOCATION:%s\n" % (location))
				ical.write("SUMMARY:%s\n" % (description))
				ical.write("DESCRIPTION:%s\n" % (description))
				ical.write("DTSTART;TZID=Europe/Berlin:%s\n" % (date + "T" + starttime + "00"))
				ical.write("DTEND;TZID=Europe/Berlin:%s\n" % (date + "T" + endtime + "00"))
				ical.write("END:VEVENT\n")
				
	link = 'http://vorlesungsplan.dhbw-mannheim.de/' + soup.find_all('a')[1].get('href')

ical.write("END:VCALENDAR\n")			
ical.close()