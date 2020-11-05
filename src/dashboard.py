from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort
from src.auth import login_required
from src.db import get_db
from src.merakiAPI import *
from src.monitoringSchedular import *
from src.bot import *
import datetime
import threading
import schedule
import time


bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    """
    The Index page (For Testing)
    :return:
    """
    post_Webex_Message('Testing from application')
    return render_template('dashboard/index.html')


@bp.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    """
    The base Application Dashboard page
    :return:
    """
    error = None

    # Ensure User has registered an API Key
    if 'apiKey' not in session:
        error = 'Error: Meraki API Client not properly established!'
        flash(error)
        return render_template('auth/login.html')

    # Load Page
    else:
        session['available_Orgs'] = get_Meraki_Organizations(session['apiKey'])

        if request.method == 'POST':
            # Clear any previous session data
            if 'selectedOrg' in session:
                session.pop('selectedOrg', None)
            session['selectedOrg'] = request.form.get('organization')
            return redirect(url_for('dashboard.dashboardWithNetworks'))

        return render_template('dashboard/dashboard.html', available_Orgs=session['available_Orgs'])


@bp.route('/dashboardWithNetworks', methods=('GET', 'POST'))
@login_required
def dashboardWithNetworks():
    """
    The Application Dashboard page
        - After User selects an Organization
    :return:
    """
    # Ensure Organization is selected
    if 'selectedOrg' not in session:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        # IF a different Organization is selected
        if request.form.get('organization'):
            session.pop('selectedOrg', None)
            session['selectedOrg'] = request.form.get('organization')

        # User selects a Network
        else:
            if 'selectedNetwork' in session:
                session.pop('selectedNetwork', None)
            session['selectedNetwork'] = request.form.get('network')
            return redirect(url_for('dashboard.dashboardComplete'))

    session['org_Networks'] = get_Meraki_Networks(session['apiKey'], session['selectedOrg'])
    return render_template('dashboard/dashboardWithNetworks.html', available_Orgs=session['available_Orgs'],
                           selectedOrg=session['selectedOrg'], org_Networks=session['org_Networks'])


@bp.route('/dashboardComplete', methods=('GET', 'POST'))
@login_required
def dashboardComplete():
    """
    The Complete Application Dashboard page
        - After User selects both a Network and an Organization
    :return:
    """
    # Ensure Network is selected
    if 'selectedNetwork' not in session:
        return redirect(url_for('dashboard.dashboardWithNetworks'))

    # Clear previous Session data
    if 'network_Events' in session:
        session.pop('network_Events', None)
    if 'network_Devices' in session:
        session.pop('network_Devices', None)
    if 'device' in session:
        session.pop('device', None)

    session['network_Events'] = get_Meraki_Network_Events(session['apiKey'], session['selectedNetwork'])
    session['network_Devices'] = get_Meraki_Network_Devices(session['apiKey'], session['selectedNetwork'])

    if request.method == 'POST':
        # IF a new Organization is selected
        if request.form.get('organization'):
            session.pop('selectedOrg', None)
            session.pop('selectedNetwork', None)
            session['selectedOrg'] = request.form.get('organization')
            return redirect(url_for('dashboard.dashboardWithNetworks'))

        # IF a new Network is selected
        elif request.form.get('network'):
            session.pop('selectedNetwork', None)
            session['selectedNetwork'] = request.form.get('network')
            return redirect(url_for('dashboard.dashboardComplete'))

        # IF the Event log is refreshed
        elif request.form.get('refreshEvents'):
            session.pop('network_Events', None)
            session['network_Events'] = get_Meraki_Network_Events(session['apiKey'], session['selectedNetwork'])
            return redirect(url_for('dashboard.dashboardComplete'))

        # IF a Network Device is selected
        elif request.form.get('device'):
            session.pop('device', None)
            session['device'] = request.form.get('device')
            return redirect(url_for('dashboard.networkSwitch'))

        else:
            return redirect(url_for('dashboard.dashboardComplete'))

    return render_template('dashboard/dashboardComplete.html', available_Orgs=session['available_Orgs'],
                           selectedOrg=session['selectedOrg'], org_Networks=session['org_Networks'],
                           selectedNetwork=session['selectedNetwork'], network_Devices=session['network_Devices'],
                           network_Events=session['network_Events'])


@bp.route('/networkSwitch', methods=('GET', 'POST'))
@login_required
def networkSwitch():
    """
    The Network Device Detail page
        - Displays Switchport statuses and other information
    :return:
    """
    # Error check
    error = None
    if 'device' not in session:
        error = 'ERROR: Invalid state entered! Device page accessed without selecting a device.'
        flash(error)
        return redirect(url_for('dashboard.dashboardComplete'))

    org = {'id': session['selectedOrg']}

    deviceDetails = get_Meraki_Network_Device(session['apiKey'], session['device'])
    device_PortList = get_Meraki_Switch_Port(session['apiKey'], session['device'])
    device_PortList_Status = get_Meraki_Switch_Port_Status(session['apiKey'], session['device'])

    if request.method == 'POST':
        port_Enable_List = request.form.getlist('port')
        complete_Action_List = []

        for port in device_PortList:
            # User tries to Enable port
            if port['portId'] in port_Enable_List:
                if not port['enabled']:
                    portUpdate = {"operation": "update"}
                    resource = '/devices/{}/switch/ports/{}'.format(session['device'], port['portId'])
                    portUpdate['resource'] = resource
                    body = {'enabled': True}
                    portUpdate['body'] = body
                    complete_Action_List.append(portUpdate)
            # User tries to Disable port
            else:
                if port['enabled']:
                    portUpdate = {"operation": "update"}
                    resource = '/devices/{}/switch/ports/{}'.format(session['device'], port['portId'])
                    portUpdate['resource'] = resource
                    body = {'enabled': False}
                    portUpdate['body'] = body
                    complete_Action_List.append(portUpdate)
        runActionList(session['apiKey'], org, complete_Action_List)
        return redirect(url_for('dashboard.dashboardComplete'))

    return render_template('dashboard/networkSwitch.html', deviceDetails=deviceDetails, device_PortList=device_PortList,
                           device_PortList_Status=device_PortList_Status)


@bp.route('/automation', methods=('GET', 'POST'))
@login_required
def automation():
    """
    The Automation page that allows the user to start the Automated Reporting process
    :return:
    """
    if request.method == 'POST':
        selectedAutomationOrg = request.form.getlist('organization')
        if len(selectedAutomationOrg) == 1:
            organization = get_Meraki_Organization(session['apiKey'], selectedAutomationOrg[0])
            organization_Networks = get_Meraki_Networks(session['apiKey'], organization['id'])

            # Create and Start Monitoring thread
            x = threading.Thread(target=scheduleTask, args=(session['apiKey'], organization, organization_Networks), daemon=True)
            x.start()
            msg = 'SUCCESS: Automated Port Monitoring started for {}'.format(organization['name'])
            flash(msg)
            return redirect(url_for('dashboard.dashboardComplete'))
        else:
            error = 'WARNING: Please select only 1 organization'
            flash(error)
    return render_template('dashboard/automation.html', available_Orgs=session['available_Orgs'])


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    """
    Simplistic Settings page
    :return:
    """
    if request.method == 'POST':
        stopScheduledTask()
        return redirect(url_for('dashboard.dashboardComplete'))
    return render_template('dashboard/settings.html')