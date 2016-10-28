import unittest
import sys
import os
#Python interpretter needs to search up on directory for the duebot package
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "//..//")
from datetime import date, time
from duebot.event import Event, from_xml

EVENT1_XML = "<event>\n\
	<title>SYSC4504 A1</title>\n\
	<date>\n\
		<year>3016</year>\n\
		<month>10</month>\n\
		<day>24</day>\n\
	</date>\n\
	<time>21:00:00</time>\n\
</event>\n"

#Tests will work even if not ran directly from tests driectory
TEST_EVENTS = os.path.dirname(os.path.realpath(__file__)) + "/data/test_events.xml"

class EventTest(unittest.TestCase):

	def setUp(self):
		self.e1 = Event("SYSC4504 A1", date(3016, 10, 24), time(21))
		self.e2 = Event("SYSC4602 A3", date(3016, 10, 23), time(12))

	def test_to_xml(self):
		self.assertEqual(EVENT1_XML, self.e1.to_xml())

	def test_from_xml(self):
		events = from_xml(TEST_EVENTS)
		self.assertEquals(2, len(events))
		self.assertEquals(self.e1, events[0])
		self.assertEquals(self.e2, events[1])

	def testToStringWithTime(self):
		self.assertEquals(str(self.e1), "SYSC4504 A1 is due on October 24 3016 at 09:00PM")

	def testToStringWithoutTime(self):
		e = Event("SYSC3101 A2", date(3016, 12, 10))
		self.assertEquals(str(e), "SYSC3101 A2 is due on December 10 3016")

	def testYearSet(self):
		e1 = Event("Event 1", date(1900, date.today().month, 12))
		e2 = Event("Event 2", date(1900, date.today().month - 1, 12))
		today = date.today()
		self.assertEquals(today.year, e1.dueDate.year)
		self.assertEquals(today.year + 1, e2.dueDate.year)

if __name__ == '__main__':
	unittest.main()
