import unittest
from datetime import date, time, timedelta
import filecmp
import sys
import os
#Python interpretter needs to search up on directory for the duebot package
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "//..//")
from duebot.duebot import Duebot, TEST_MODE_BOT_ID
from duebot.event import Event

#Check which expected_results xml to us
expected_res = "expected_events_WIN.xml" if os.name == "nt" else "expected_events_UNIX.xml"

BOT_NAME = "TestBot"
TEST_XML = os.path.dirname(os.path.realpath(__file__)) + "/data/" + expected_res

class DueBotTest(unittest.TestCase):

	def setUp(self):
		#Create the bot in test mode
		self.bot = Duebot(BOT_NAME, True)

	def testCreateEventLongFormDate1(self):
		e = Event("SYSC4504 A1", date(3012, 12, 12))
		self.bot.parseInstruction("SYSC4504 A1 is due on December 12 3012")
		self.assertEqual(e, self.bot.events[0])

	def testCreateEventLongFormDate2(self):
		e = Event("SYSC3101 Assignment 2 Flex/Bison", date(3015, 10, 31))
		self.bot.parseInstruction("SYSC3101 Assignment 2 Flex/Bison due October 31 3015")
		self.assertEquals(e, self.bot.events[0])

	def testCreateEventLongFormDateNoDelimeter(self):
		"""Invalid event now delimeter for start of the date
		"""
		self.bot.parseInstruction("SYSC4101 A2 December 9 2016")
		self.assertEquals(0, len(self.bot.events))

	def testCreateEventShortFormDate1(self):
		e = Event("SYSC4504 A1", date(3016, 1, 12))
		self.bot.parseInstruction("SYSC4504 A1 is due on 12/01/3016")
		self.assertEquals(e, self.bot.events[0])

	def testCreateEventShortFormDateInvalid(self):
		"""Day and month invalid should fail
		"""
		self.bot.parseInstruction("SYSC4101 A2 due on 31/14/2017")
		self.assertEquals(0, len(self.bot.events))

	def testCreateEventShortFormDateNoDelimeter(self):
		"""No date delimeter, should fail
		"""
		self.bot.parseInstruction("SYSC4504 A3, 12/01/2016")
		self.assertEquals(0, len(self.bot.events))

	def testCreateEventWithTime(self):
		e = Event("SYSC2300 A2", date(3016, 12, 14), time(9))
		self.bot.parseInstruction("SYSC2300 A2 is due December 14 3016 at 9AM")
		self.assertEquals(e, self.bot.events[0])

	def testCreateEventWithInvalidTime(self):
		self.bot.parseInstruction("SYSC2100 A2 is due on December 14 at 27:00")
		self.assertEquals(0, len(self.bot.events))

	def testCreateEventWithInvalidTime2(self):
		self.bot.parseInstruction("SYSC2100 A2 is due on December 14 at 17PM")
		self.assertEquals(0, len(self.bot.events))

	def testCreateEventWithInvalidTime3(self):
		self.bot.parseInstruction("SYSC2100 A2 is due on December 14 at 9:75AM")
		self.assertEquals(0, len(self.bot.events))

	def testWriteEventsToXML(self):
		"""
		Test that events are written to the xml file correctly
		"""
		# First clear the file from earlier tests
		if os.path.isfile(self.bot.event_xml): os.remove(self.bot.event_xml)
		#Use a different bot to avoid conflicts with the data file
		bot2 = Duebot(BOT_NAME, True)
		bot2.parseInstruction("SYSC4504 A1 is due on 24/10/3016 at 9PM")
		bot2.parseInstruction("SYSC4602 A3 is due October 23 3016 at 12PM")
		self.assertTrue(filecmp.cmp(TEST_XML, bot2.event_xml))
		#Delete the xml file
		os.remove(bot2.event_xml)

	def testCleanEvents(self):
		e1 = Event("SYSC4504 A1", date(3000, 10, 19))
		e2 = Event("SYSC3101 A3", date(2010, 12, 21))
		self.bot.events.append(e1)
		self.bot.events.append(e2)
		self.assertEquals(2, len(self.bot.events))
		self.bot.cleanEvents()
		self.assertEquals(1, len(self.bot.events))

	def testCleanEventsUpdateXML(self):
		# First clear the file from earlier tests
		if os.path.isfile(self.bot.event_xml): os.remove(self.bot.event_xml)
		bot2 = Duebot(BOT_NAME, True)
		bot2.parseInstruction("SYSC4504 A1 is due on 24/10/3016 at 9PM")
		bot2.parseInstruction("SYSC4602 A3 is due October 23 3016 at 12PM")
		bot2.parseInstruction("SYSC3101 A2 is due December 11 1995 at 7PM")
		# Ensure the past event is added
		self.assertFalse(filecmp.cmp(TEST_XML, bot2.event_xml))
		bot2.cleanEvents()
		# Now the past event should be deleted
		self.assertTrue(filecmp.cmp(TEST_XML, bot2.event_xml))

	def testWhatDueToday(self):
		e1 = Event("SYSC3101 A1", date.today())
		e2 = Event("SYSC3200 A4", date(3016, 10, 12))
		e3 = Event("SYSC4001 Lab5", date.today())
		self.bot.events.extend([e1, e2, e3])
		expect = str(e1) + "\n" + str(e3) + "\n"
		self.assertEquals(expect, self.bot.getUpcomingEvents("what's due today?"))

	def testWhatDueThisWeek(self):
		e1 = Event("SYSC3200 Lab5", date.today())
		e2 = Event("SYSC4504 A3", date.today() + timedelta(days=5))
		e3 = Event("SYSC4501 A2", date.today() + timedelta(days=7))
		e4 = Event("COMP1805 A4", date.today() + timedelta(days=60))
		self.bot.events.extend([e1, e2, e3, e4])
		expect = str(e1) + "\n" + str(e2) + "\n" + str(e3) + "\n"
		self.assertEquals(expect, self.bot.getUpcomingEvents("what's due this week"))

	def testWhatDueThisMonth(self):
		e1 = Event("SYSC3200 A2", date.today() + timedelta(days=30))
		e2 = Event("SYSC3101 A4", date.today() + timedelta(days=15))
		e3 = Event("SYSC4805 Project", date.today() + timedelta(days=365))
		self.bot.events.extend([e1, e2, e3])
		expect = str(e1) + "\n" + str(e2) + "\n"
		self.assertEquals(expect, self.bot.getUpcomingEvents("what is due this month?"))

	def testWhatsDueNothing(self):
		self.assertEquals("Nothing! :)", self.bot.getUpcomingEvents("whats due?"))

	def testWhatsDueAll(self):
		e1 = Event("SYSC3101 A1", date.today())
		e2 = Event("SYSC3200 A4", date(3016, 10, 12))
		e3 = Event("SYSC4001 Lab5", date.today())
		self.bot.events.extend([e1, e2, e3])
		expect = str(e1) + "\n" + str(e2) + "\n" + str(e3) + "\n"
		self.assertEquals(expect, self.bot.getUpcomingEvents("whats due?"))

	def testGetEventReminders(self):
		e1 = Event("SYSC3101 A1", date.today())
		e2 = Event("SYSC3101 A4", date.today() + timedelta(days=3))
		e3 = Event("SYSC3200 Lab3", date.today() + timedelta(days=7))
		self.bot.events.extend([e1, e2, e3])
		expect = str(e1) + "\n" + str(e2) + "\n"
		self.assertEquals(expect, self.bot.getEventReminders())

if __name__ == '__main__':
	unittest.main()
