import os
from slackclient import SlackClient

BOT_NAME = "duebot"
READ_SOCKET_DELAY = 1

class duebot(object):

	def __init__(self):
		self.slack_client = SlackClient(os.environ.get('DUE_BOT_API_TOKEN'))
		self.bot_id = self.get_bot_id()

	def get_bot_id(self):
		api_call = self.slack_client.api_call("users.list")
		if api_call.get('ok'):
			users = api_call.get('members')
			for user in users:
				if 'name' in user and user.get('name') == BOT_NAME:
					return user.get('id')
			print "Could not get bot id!"
			return -1	

	def print_all_messages(self):
		if self.slack_client.rtm_connect():
			print "Duebot up and running!"
			while True:
				output_list = self.slack_client.rtm_read()
				if output_list and len(output_list) > 0:
					for output in output_list:
						if 'channel' in output and 'text' in output:
							print output['channel']
							print output['text']

if __name__ == '__main__':
	d = duebot()
	d.print_all_messages()