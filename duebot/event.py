from xml.dom import minidom
from datetime import date, datetime, time, timedelta
import sys
import re

DEFAULT_YEAR = 1900

class Event(object):

	def __init__(self, title, due_date, due_time=None):
		"""Constructor"""
		self.title = title
		self.due_date = due_date
		if self.due_date.year == DEFAULT_YEAR:
			today = date.today()
			year = today.year if due_date.month >= today.month else today.year + 1
			self.due_date = date(year, due_date.month, due_date.day)
		self.due_time = due_time

	def to_xml(self):
		"""Returns the xml representation of an event as a string"""
		s = "<event>\n"
		s += "\t<title>" + self.title + "</title>\n"
		s += "\t<date>\n"
		s += "\t\t<year>" + str(self.due_date.year) + "</year>\n"
		s += "\t\t<month>" + str(self.due_date.month) + "</month>\n"
		s += "\t\t<day>" + str(self.due_date.day) + "</day>\n"
		s += "\t</date>\n"
		s += "\t<time>" + str(self.due_time) + "</time>\n"
		s += "</event>\n"
		return s

	def __eq__(self, other):
		return self.title == other.title and self.due_date == other.due_date \
			and self.due_time == other.due_time

	def __str__(self):
		s = self.title + " is due on " + self.due_date.strftime("%B %d %Y")
		if self.due_time:
			s += " at " + self.due_time.strftime("%I:%M%p")
		return s

def parseDate(date):
	"""Parses a date tag from xml input
	returns a tuple containing the year, month, and day as strings
	"""
	yearNode = date.getElementsByTagName('year').item(0)
	monthNode = date.getElementsByTagName('month').item(0)
	dayNode = date.getElementsByTagName('day').item(0)

	year = yearNode.firstChild.data
	month = monthNode.firstChild.data
	day = dayNode.firstChild.data

	return year, month, day

def parseEvent(event):
	"""parses an event tag from xml input
	returns the event represented by the event tag
	"""
	titleNode = event.getElementsByTagName('title').item(0)
	#The first child is a text node containing the title
	title = str(titleNode.firstChild.data)
	year, month, day = parseDate(event.getElementsByTagName('date').item(0))

	timeNode = event.getElementsByTagName('time').item(0)
	time = str(timeNode.firstChild.data)
	if time != "None":
		try:
			time = datetime.strptime(time, "%H:%M:%S").time()
		except ValueError:
			print "Fatal! An invalid time was found in the xml file, it is possible corrupted"
			print "<" + title + "> (HH:MM:SS) " + str(time)
			raise ValueError
	else: time = None

	try:
		d = date(int(year), int(month), int(day))
	except ValueError:
		print "Fatal! An invalid date was found in the xml file, it is possibly corrupted"
		print "<" + title + "> (YYYY/MM/DD) " + str(year) + "/" + str(month) + "/" + str(day)
		raise ValueError
	return Event(title, d, time)

def from_xml(xml_file):
	"""
	Parses an xml file for any events
	xml_file: path to the xml file containing the events
	returns a list of all events contained withing an xml file
	"""
	events = []
	xmldoc = minidom.parse(xml_file)
	eventlist = xmldoc.getElementsByTagName('event')
	for e in eventlist:
		try:
			events.append(parseEvent(e))
		except ValueError:
			print "Event is being skipped!"
	return events