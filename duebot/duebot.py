import os
import sys
import time as Time
import re
from event import Event, from_xml
from datetime import date as Date, time, datetime
from slackclient import SlackClient

READ_SOCKET_DELAY = 1
TEST_MODE_BOT_ID = -1

class Duebot(object):

	def __init__(self, name, testMode=False):
		"""
		Constructor
		name: The name of this bot
		testMode: Used to trigger testMode for unit tests
			in test mode the bot will not attempt to communicate with
			the slack api through the slack client
		"""
		self.name = name
		self.slack_client = SlackClient(os.environ.get('DUE_BOT_API_TOKEN'))
		self.bot_id = self.get_bot_id() if not testMode else TEST_MODE_BOT_ID
		self.events = []
		self.event_xml = os.path.dirname(os.path.realpath(__file__)) + "/../data/" + \
			str(self.bot_id) + "_events.xml"
		if not os.path.isfile(self.event_xml): self.createXMLFile()

	def get_bot_id(self):
		"""Gets the User id associated with this bots name
		"""
		api_call = self.slack_client.api_call("users.list")
		if api_call.get('ok'):
			users = api_call.get('members')
			for user in users:
				if 'name' in user and user.get('name') == self.name:
					return user.get('id')
			print "Could not get bot id!"
			return -1	

	def listen(self):
		"""Checks for messages from the firehose every READ_SOCKET_DELAY seconds
		"""
		pattern = r"(?<=<@" + str(self.bot_id) + r"> ).+"
		if self.slack_client.rtm_connect():
			print "Duebot <" + str(self.name) + "> up and running"
			while True:
				output_list = self.slack_client.rtm_read()
				if output_list and len(output_list) > 0:
					for output in output_list:
						if 'channel' in output and 'text' in output:
							#Are you talking to me?
							match = re.search(pattern, output['text'])
							if match:
								self.parseInstruction(match.group())
				Time.sleep(READ_SOCKET_DELAY)

	def createXMLFile(self):
		f = open(self.event_xml, "w+")
		f.write("<events>\n</events>")
		f.close()

	def writeEventToFile(self, event):
		f = open(self.event_xml, "r+")
		lines = f.readlines()
		f.seek(0 - len(lines[len(lines) - 1]), 2)
		f.write(event.to_xml())
		f.write("</events>")
		f.close()

	def parseInstruction(self, instruction):
		"""Parses an instruction received through slack
		instruction: the instruction to be parsed
		"""
		newEventRE = r".+(?= due).+"

		match = re.search(newEventRE, instruction)
		if match:
			event = self.handleNewEvent(match.group())
			if event: 
				self.events.append(event)
				self.writeEventToFile(event)


	def handleNewEvent(self, instruction):
		"""Handles the creation of a new event
		instruction: The instruction detailing the new event
		"""
		gettingName = True
		name = ""
		date = ""
		for word in instruction.split(" "):
			if word.lower() in ["is", "due", "on"]:
				gettingName = False
			elif gettingName:
				#Don't add a space before the first word
				if name == "": name += word
				else: name += " " + word
			else:
				date += word + " "
		try:
			e = Event(name, self.parseDate(date))
		except ValueError:
			e = None
		return e

	def parseDate(self, date):
		"""Parses a user inputted date from an instruction into a valid date object
		date: The date from the instruction
		return: A valid date object based on date
		"""
		longFormPattern = r"\w+ [0-9]{1,2}( [0-9]{2,4})?"
		shortFormPattern = r"\d\d/\d\d/\d\d\d\d"
		match = re.search(longFormPattern, date)
		if match:
			return self.parseLongFormDate(match.group())
		match = re.search(shortFormPattern, date)
		if match:
			return self.parseShortFormDate(match.group())
		#Can't parse date
		#TODO not this
		return None

	def parseLongFormDate(self, date):
		"""Parses a date f the form <Month> <Day> [Year]
		"""
		dates = date.split(" ")
		month, day = dates[0], int(dates[1])
		month = monthAsInt(month)
		currDate = Date.today()
		if len(dates) == 3:
			year = int(dates[2])
		else:
			if month >= currDate.month:
				year = currDate.year
			else:
				year = currDate.year + 1
		return Date(year, month, day)

	def parseShortFormDate(self, date):
		"""Parses a date of the from dd/mm/yyyy
		"""
		dates = date.split("/")
		day, month, year = int(dates[0]), int(dates[1]), int(dates[2])
		return Date(year, month, day)

def monthAsInt(month):
	month = month.lower()
	if month == "january" or month == "jan":
		return 1
	elif month == "february" or month == "feb":
		return 2
	elif month == "march" or month == "mar":
		return 3
	elif month == "april" or month == "apr":
		return 4
	elif month == "may":
		return 5
	elif month == "june" or month == "jun":
		return 6
	elif month == "july" or month == "jul":
		return 7
	elif month == "august" or month == "aug":
		return 8
	elif month == "september" or month == "sep":
		return 9
	elif month == "october" or month == "oct":
		return 10
	elif month == "november" or month == "nov":
		return 11
	elif month == "december" or month == "dec":
		return 12
	else:
		raise ValueError

def Main():
	if len(sys.argv) != 2:
		print "Incorrect number of command line arguments!"
		print "Usage: python duebot.py <name>"
		return 1
	d = Duebot(sys.argv[1])
	d.listen()

if __name__ == '__main__':
	Main()
