import os
import sys
import time as Time
import re
from event import Event, from_xml
from datetime import date as date, time, datetime, timedelta
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
		whatDueRE = r"what('s|s| is) due"

		match = re.search(newEventRE, instruction)
		if match:
			event = self.handleNewEvent(match.group())
			if event: 
				self.events.append(event)
				self.writeEventToFile(event)
			return
		if re.search(whatDueRE, instruction.lower()):
			s = self.getUpcomingEvents(instruction.lower())


	def handleNewEvent(self, instruction):
		"""Handles the creation of a new event
		instruction: The instruction detailing the new event
		"""
		gettingName = True
		gettingDate = False
		name = ""
		date = ""
		time = ""
		for word in instruction.split(" "):
			if word.lower() in ["is", "due", "on"]:
				gettingName = False
				gettingDate = True
			elif gettingName:
				#Don't add a space before the first word
				if name == "": name += word
				else: name += " " + word
			elif gettingDate:
				if word.lower() == "at":
					gettingDate = False
				else: 
					if date == "": date += word
					else: date += " " + word
			else: #Getting time
				time += word
		try:
			if time == "": time = None #No time supplied
			e = Event(name, self.parseDate(date), self.parseTime(time))
		except ValueError:
			e = None
		return e

	def parseDate(self, date):
		"""Parses a user inputted date from an instruction into a valid date object
		date: The date from the instruction
		return: A valid date object based on date
		"""
		possiblePatterns = ["%d/%m/%y", "%d/%m/%Y", "%B %d %Y",	"%B %d", "%b %d %Y", "%b %d"]
		for pattern in possiblePatterns:
			try:
				return datetime.strptime(date, pattern).date()
			except ValueError:
				pass
		#None of the pattern match	
		raise ValueError

	def parseTime(self, time):
		if time == None: return None
		possiblePatterns = ["%I%p", "%I:%M%p", "%H:%M", "%H%M"]
		for pattern in possiblePatterns:
			try:
				return datetime.strptime(time, pattern).time()
			except ValueError:
				pass
		#None of the patterns match
		raise ValueError

	def cleanEvents(self):
		"""Clears any events whose due date has passed
		"""
		today = datetime.now().date()
		updateXML = False
		for event in self.events:
			if event.due_date < today:
				self.events.remove(event)
				updateXML = True
		if updateXML: self.updateXML()

	def updateXML(self):
		#Delete old file
		os.remove(self.event_xml)
		self.createXMLFile()
		for event in self.events:
			self.writeEventToFile(event)

	def getUpcomingEvents(self, instruction):
		if re.search(r"today(\?)?", instruction):
			collectBy = lambda x: x.due_date == date.today()
		elif re.search(r"week(\?)?", instruction):
			collectBy = lambda x: x.due_date <= date.today() + timedelta(days=7)
		elif re.search(r"month(\?)?", instruction):
			collectBy = lambda x: x.due_date <= date.today() + timedelta(days=30)
		else:
			collectBy = lambda x: True #Get everything
		s = ""
		for event in self.events:
			if collectBy(event):
				s += str(event) + "\n"
		return s if s != "" else "Nothing! :)"

		
def Main():
	if len(sys.argv) != 2:
		print "Incorrect number of command line arguments!"
		print "Usage: python duebot.py <name>"
		return 1
	d = Duebot(sys.argv[1])
	d.listen()

if __name__ == '__main__':
	Main()
