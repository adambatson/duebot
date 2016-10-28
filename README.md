# Deadline Bot
[![build status](http://gitlab.adambatson.com/adambatson/deadline_bot/badges/master/build.svg)](http://gitlab.adambatson.com/adambatson/deadline_bot/builds/)

A Slack bot to track due dates

## Dependencies

[slackclient](https://github.com/slackhq/python-slackclient) is required to run.  Install it using

```
pip install slackclient
```

## Usage
First you must [set up a bot user on slack](https://api.slack.com/bot-users).  Once your bot user
is set up launch duebot by running

```
python duebot/duebot.py "name"
```
where "name" is the name of the bot on your slack team.

## TODO
- Ability to set custom reminders for events
- Prevent users from adding duplicate events
- Allow the bot to work accross multiple channels
	- Possibly by linking events to specific channels
- Allow users to delete / modify events

## License
Duebot is licensed under the MIT License.  More info can be found in the LICENSE file.