import requests
import json

BASE_URL = 'https://api.meraki.com/api/v1'


def get_Meraki_Organization(token, orgId):
	"""
	Return an organization
	:param token: user access token
	:param orgId: Organization
	:return:
	"""
	url = '{}/organizations/{}'.format(BASE_URL, orgId)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	return response.json()


def get_Meraki_Organizations(token):
	"""
	List the organizations that the user has privileges on
	:param token: user access token
	:return:
	"""
	url = '{}/organizations'.format(BASE_URL)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	return response.json()


def get_Meraki_Networks(token, orgID):
	"""
	List the networks that the user has privileges on in an organization
	:param token: user access token
	:param orgID: Selected Organization
	:return:
	"""
	url = '{}/organizations/{}/networks'.format(BASE_URL, orgID)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	return response.json()


def get_Meraki_Organization_Devices(token, orgID):
	"""
	List the devices in an organization
		- Filtering for MS devices
	:param token: user access token
	:param orgID: Selected Organization
	:return:
	"""
	url = '{}/organizations/{}/devices'.format(BASE_URL, orgID)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	switch_List = []
	for device in response.json():
		if 'MS' in device['model']:
			switch_List.append(device)
	return switch_List


def get_Meraki_Network_Devices(token, netID):
	"""
	List the devices in a network
		- Filtering for MS devices
	:param token: user access token
	:param netID: Selected Network
	:return:
	"""
	url = '{}/networks/{}/devices'.format(BASE_URL, netID)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	switch_List = []
	for device in response.json():
		if 'MS' in device['model']:
			switch_List.append(device)
	return switch_List


def get_Meraki_Network_Events(token, netID):
	"""
	List the events for the network
	:param token: user access token
	:param netID: Selected Network
	:return:
	"""
	# Defining Event Type
	eventTypes = 'port_status'
	productType = 'switch'

	url = '{}/networks/{}/events?productType={}&includedEventTypes[]={}'.format(BASE_URL, netID, productType, eventTypes)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)

	if 'events' in response.json():
		event_List = response.json()['events']
		return event_List

	return response.json()


def get_Meraki_Network_Device(token, serial):
	"""
	Return a single device
	:param token: user access token
	:param serial: Device serial
	:return:
	"""
	url = '{}/devices/{}'.format(BASE_URL, serial)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	return response.json()


def get_Meraki_Switch_Port(token, serial):
	"""
	List the switch ports for a switch
	:param token: user access token
	:param serial: Device serial
	:return:
	"""
	url = '{}/devices/{}/switch/ports'.format(BASE_URL, serial)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	return response.json()


def get_Meraki_Switch_Port_Status(token, serial):
	"""
	Return the status for all the ports of a switch
	:param token: user access token
	:param serial: Device serial
	:return:
	"""
	url = '{}/devices/{}/switch/ports/statuses'.format(BASE_URL, serial)
	hdr = {'X-Cisco-Meraki-API-Key': token}

	response = requests.request('GET', url, headers=hdr)
	return response.json()


def update_Meraki_Switch_Port(token, serial, portID, update):
	"""
	Update a switch port
	:param token: user access token
	:param serial: Device serial
	:param portID: Switchport ID
	:param update: Updated Configuration
	:return:
	"""
	url = '{}/devices/{}/switch/ports/{}'.format(BASE_URL, serial, portID)
	hdr = {
		'X-Cisco-Meraki-API-Key': token,
		"Content-Type": "application/json",
		"Accept": "application/json"
	}
	response = requests.request('PUT', url, headers=hdr, data=update)
	return response.json()


def meraki_ActionBatch(token, orgId, actions):
	"""
	Submit batched configuration requests in a single synchronous/asynchronous transaction
	:param token: user access token
	:param orgId: Organization to apply batch command to
	:param actions: Actions to apply
	:return:
	"""
	url = '{}/organizations/{}/actionBatches'.format(BASE_URL, orgId)
	hdr = {
		'X-Cisco-Meraki-API-Key': token,
		"Content-Type": "application/json",
	}
	payload = {
		"confirmed": True,
		"synchronous": True,
		"actions": actions
	}
	response = requests.post(url, json=payload, headers=hdr)
	print(response.json())
