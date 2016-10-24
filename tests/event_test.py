import unittest
import sys
import os
#Python interpretter needs to search up on directory for the duebot package
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "//..//")
print sys.path
from datetime import date
from duebot.event import Event, from_xml

EVENT1_XML = "<event>\n\
	<title>SYSC4504 A1</title>\n\
	<date>\n\
		<year>2016</year>\n\
		<month>10</month>\n\
		<day>24</day>\n\
	</date>\n\
	<time>9PM</time>\n\
</event>\n"

#Tests will work even if not ran directly from tests driectory
TEST_EVENTS = os.path.dirname(os.path.realpath(__file__)) + "/data/test_events.xml"

class EventTest(unittest.TestCase):

	def setUp(self):
		self.e1 = Event("SYSC4504 A1", date(2016, 10, 24), "9PM")
		self.e2 = Event("SYSC4602 A3", date(2016, 10, 23), "12PM")

	def test_to_xml(self):
		self.assertEqual(EVENT1_XML, self.e1.to_xml())

	def test_from_xml(self):
		events = from_xml(TEST_EVENTS)
		self.assertEquals(2, len(events))
		self.assertEquals(self.e1, events[0])
		self.assertEquals(self.e2, events[1])

if __name__ == '__main__':
	unittest.main()
