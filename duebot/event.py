from xml.dom import minidom
from datetime import date
import sys

class Event(object):

	def __init__(self, title, due_date, due_time=None):
		"""Constructor"""
		self.title = title
		self.due_date = due_date
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

	try:
		d = date(int(year), int(month), int(day))
	except ValueError:
		print "Fatal! An invalid date was found in the xml file, it is possibly corrupted"
		print "<" + title + "> (YYYY/MM/DD) " + str(year) + "/" + str(month) + "/" + str(day)
		sys.exit()
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
		events.append(parseEvent(e))
	return events