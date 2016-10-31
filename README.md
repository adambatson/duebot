# Duebot

[![build status](http://gitlab.adambatson.com/adambatson/deadline_bot/badges/master/build.svg)](http://gitlab.adambatson.com/adambatson/deadline_bot/builds/)
[![build status](https://travis-ci.org/adambatson/duebot.svg?branch=master)](https://travis-ci.org/adambatson/duebot)

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

You'll also need to set your bots API Token to an environment variable named : DUE_BOT_API_TOKEN

### Commands
Currently Duebot supports the following commands all commands must be prefaced with
@duebot:
- [name] is due one \[date] \(at time)
	- Adds an event named name due on date, time parameter is optional
- What's due \(today | this week | this month)?
	- List all upcoming events, optionally listing events only for the current
	day, week, or month
- help
	- Displays the help message

## TODO
- Ability to set custom reminders for events
- Prevent users from adding duplicate events
- Allow the bot to work accross multiple channels
	- Possibly by linking events to specific channels
- Allow users to delete / modify events

## License
Duebot is licensed under the MIT License.  More info can be found in the LICENSE file.
