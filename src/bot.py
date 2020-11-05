import requests

# TODO: MUST SANITIZE THIS FILE BEFORE PUBLISHING!!!!!!
# WebEx API Bot Setup
BASE_URL = 'https://webexapis.com/v1'
BOT_NAME = ''
BOT_USERNAME = '@webex.bot'
BOT_ID = ''
BOT_ACCESS_TOKEN = ''

# Webex Person ID used for Direct reporting
PERSON_ID = ''


def post_Webex_Message(message):
	"""
	Cisco Webex API call to have the defined Bot POST a Message
	:param message:
	:return:
	"""
	url = '{}/messages'.format(BASE_URL)
	hdr = {
		'Authorization': 'Bearer {}'.format(BOT_ACCESS_TOKEN),
		'Content-Type': 'application/json'
	}
	# Defining Message characteristics
	payload = {
		'markdown': message,
		'toPersonId': PERSON_ID
	}

	response = requests.request('POST', url, headers=hdr, json=payload)
	return response.json()
