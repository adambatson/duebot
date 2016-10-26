import unittest
from datetime import date, time
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
		e = Event("SYSC4504 A1", date(2016, 12, 12))
		self.bot.parseInstruction("SYSC4504 A1 is due on December 12 2016")
		self.assertEqual(e, self.bot.events[0])

	def testCreateEventLongFormDate2(self):
		e = Event("SYSC3101 Assignment 2 Flex/Bison", date(2015, 10, 31))
		self.bot.parseInstruction("SYSC3101 Assignment 2 Flex/Bison due October 31 2015")
		self.assertEquals(e, self.bot.events[0])

	def testCreateEventLongFormDateNoDelimeter(self):
		"""Invalid event now delimeter for start of the date
		"""
		self.bot.parseInstruction("SYSC4101 A2 December 9 2016")
		self.assertEquals(0, len(self.bot.events))

	def testCreateEventShortFormDate1(self):
		e = Event("SYSC4504 A1", date(2016, 1, 12))
		self.bot.parseInstruction("SYSC4504 A1 is due on 12/01/2016")
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
		e = Event("SYSC2300 A2", date(2016, 12, 14), "9AM")
		self.bot.parseInstruction("SYSC2300 A2 is due December 14 2016 at 9AM")
		self.assertEquals(e, self.bot.events[0])

	def testWriteEventsToXML(self):
		"""
		Test that events are written to the xml file correctly
		"""
		# First clear the file from earlier tests
		if os.path.isfile(self.bot.event_xml): os.remove(self.bot.event_xml)
		#Use a different bot to avoid conflicts with the data file
		bot2 = Duebot(BOT_NAME, True)
		bot2.parseInstruction("SYSC4504 A1 is due on 24/10/2016")
		bot2.parseInstruction("SYSC4602 A3 is due October 23 2016")
		self.assertTrue(filecmp.cmp(TEST_XML, bot2.event_xml))
		#Delete the xml file
		os.remove(bot2.event_xml)


if __name__ == '__main__':
	unittest.main()
