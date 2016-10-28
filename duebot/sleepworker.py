from threading import Thread, Timer
from datetime import datetime, timedelta

WAKE_HOUR = 11 #11AM

class SleepWorker(Thread):
	"""
	The SleepWorkder sleeps most of the time.  Ocassionaly waking to
	perform regular tasks such as sending out reminders about events
	and cleaning the xml file
	"""

	def __init__(self, bot):
		Thread.__init__(self)
		self.setDaemon(True)
		self.bot = bot
		self.timer = None

	def run(self):
		self.setUpTimer()

	def setUpTimer(self):
		"""
		Sets up a timer that will activate the sleepworker at the next
		occurence of WAKE_HOUR
		"""
		timeNow = datetime.today()
		day = timeNow.day
		if timeNow.hour >= WAKE_HOUR: day += 1
		wakeUpTime = timeNow.replace(day=day, hour=WAKE_HOUR, minute=0, second=0, microsecond=0)
		delta_t = wakeUpTime - timeNow
		self.timer = Timer(delta_t.seconds + 1, self.onWakeUp)
		self.timer.start()

	def onWakeUp(self):
		self.bot.cleanEvents()
		self.bot.sendReminders()
		#Start the timer again
		self.setUpTimer()