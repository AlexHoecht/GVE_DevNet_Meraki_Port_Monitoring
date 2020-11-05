from src.merakiAPI import *
from src.bot import *
import schedule
import datetime
import time


def monitoringTask(apiKey, org, networks):
	"""
	The Automated Monitoring Task to be Scheduled
		TODO: This is where the Monitoring Task is defined!
		- Current Flag Criteria = Enabled and 0 Port usage in past 1 day
	:param apiKey: user access token
	:param org: Organization to apply task
	:param networks: Networks of Organization
	:return:
	"""
	# Starting Action
	currentDateAndTime = datetime.datetime.now()
	print('Starting Monitoring Action @ {}'.format(currentDateAndTime))

	# Automated Report message (Written in Markdown)
	bot_Message = '**{}** \n'.format(org['name'])

	for network in networks:
		bot_Message += "* Network: **{}** \n".format(network['name'])
		network_Devices = get_Meraki_Network_Devices(apiKey, network['id'])

		for device in network_Devices:
			if 'name' in device:
				bot_Message += "   * Device: **{}** \n".format(device['name'])
			else:
				bot_Message += "   * Device: **{}** \n".format(device['model'])

			device_Ports = get_Meraki_Switch_Port_Status(apiKey, device['serial'])
			device_Flagged_Ports = []

			for port in device_Ports:
				# TODO - This is where you can define the Flagging Criteria
				# If port is enabled, check usage in the past day
				if 'enabled':
					port_Usage = port['usageInKb']['total']
					if port_Usage == 0:
						# If no usage, Flag port
						device_Flagged_Ports.append(port['portId'])

			bot_Message += "      * Flagged Ports: **{}** \n".format(device_Flagged_Ports)
		bot_Message += " \n"
	# Post Report to Webex
	post_Webex_Message(bot_Message)
	print('Action Completed @ {}'.format(datetime.datetime.now()))


def scheduleTask(apiKey, org, networks):
	"""
	Create a new Schedule Task
	:param apiKey: user access token
	:param org: Organization to apply task
	:param networks: Networks of Organization
	:return:
	"""
	print('Clearing Previous Jobs')
	schedule.clear()
	# TODO - This is where you edit the Reporting Schedule
	print('Creating Job to execute every X minute(s)')
	schedule.every(5).minutes.do(monitoringTask, apiKey=apiKey, org=org, networks=networks)
	print('Job Scheduled!')

	while True:
		schedule.run_pending()
		time.sleep(10)


def stopScheduledTask():
	"""
	Clear any Scheduled Tasks
	:return:
	"""
	print('Stopping Jobs')
	schedule.clear()


def runActionList(apiKey, org, action_List):
	"""
	Helper function for the Meraki Action batch functionality
		- NOTE: Action Batches can run 20 Actions per Batch!
	:param apiKey: user access token
	:param org: Organization to apply batch command to
	:param action_List: Actions to apply
	:return:
	"""
	if len(action_List) > 20:
		part_action_List = action_List[:20]
		meraki_ActionBatch(apiKey, org['id'], part_action_List)
		runActionList(apiKey, org, action_List[:20])
	else:
		meraki_ActionBatch(apiKey, org['id'], action_List)
