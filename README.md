# Meraki Automated Port Monitoring Prototype
The Prototype solution was built to demonstrate the "Art of Possible" around the following use-cases:
 1) Provide and "Easy-to-Use" Dashboard for first-level staff to configure Meraki Switchports.
 2) Enable an Organization-wide, Automated, Notification system to monitor Switchports that meet the defined criteria.

## Contacts
* Alex Hoecht
* Jason Mah


## Solution Components
* Python3
* SQLite Database
* Flask Web-Application framework
* Cisco UI Kit
* Meraki Dashboard API
* Cisco Webex API


## Dependencies/Environment
Required Packages
 - Flask (pip install Flask)
 - Requests (pip install requests)
 - Click (pip install click)
 - Schedule (pip install schedule)
```
# Create a Virtual Environment
python3 -m venv Virtual_Environment
source Virtual_Environment/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

## Starting the Application
Once Dependencies are installed to Environment:
```
# Setup Flask application
export FLASK_APP=src
export FLASK_ENV=development

# Start Application
flask run
```

# Documentation
### Developer Resources
- Meraki API Reference - [See Docs](https://developer.cisco.com/meraki/api-v1/)
- Flask Application Framework - [See Docs](https://flask.palletsprojects.com/en/1.1.x/)
- Python Job Scheduling - [See Docs](https://schedule.readthedocs.io/en/stable/)
- Webex Messages - [See Docs](https://developer.webex.com/docs/api/v1/messages/create-a-message)
- Webex Message Formatting - [See Docs](https://developer.webex.com/docs/api/basics#formatting-messages)
- Create a Webex Bot - [See Docs](https://developer.webex.com/docs/bots)

### LICENSE

Provided under Cisco Sample Code License, for details see [here](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.