import unittest
from datetime import date
import sys
import os
#Python interpretter needs to search up on directory for the duebot package
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "//..//")
from duebot.duebot import Duebot, TEST_MODE_BOT_ID
from duebot.event import Event

BOT_NAME = "TestBot"

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

if __name__ == '__main__':
	unittest.main()
