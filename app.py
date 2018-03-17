
from __future__ import print_function
import httplib2
import os
import boto3

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import dateutil.parser
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Power Notify'
LOG_FILE = 'log.txt'
MINUTE = 60.0


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-powernotify-token.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def send_sms_message(number,msg):
    client = boto3.client('sns')
    response = client.publish(
        PhoneNumber=number,
        Message=msg,
        MessageStructure='',
        MessageAttributes={}
    )
    # log text sent
    fh = open(LOG_FILE, "a")
    fh.writelines([ 'number: '+number, ', message: '+msg ,', response: '+str(response),', time: '+str(datetime.datetime.now(datetime.timezone.utc)),"\n"])
    fh.close

def send_text_notificaton(event_dict):
    """
    takes in calendar event
    sends text message
    PhoneNumber = location
    Message = description
    """
    if('#powernotify' in event_dict['summary'].lower() and 'location' in event_dict and event_dict['location']):
        number = form_phone_number(event_dict['location'])
        send_sms_message(number, event_dict['description']) if event_dict['description'] else send_sms_message(number, event_dict['summary'])

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def form_phone_number(num_str):
    if '+' in num_str:
        return num_str
    else:
        return '+'+num_str

def event_loop(actions):
    """
    checks every minute for event at current time
    calls 
    """
    while(True):

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
        events = eventsResult.get('items', []) 

        # if an upcoming events exist
        if events:
            eventTime = dateutil.parser.parse(events[0]['start']['dateTime'])
            # if current time in range
            if time_in_range(eventTime - datetime.timedelta(seconds=30), eventTime + datetime.timedelta(seconds=30), datetime.datetime.now(datetime.timezone.utc)):
                # loop over all actions passing event in
                for action in actions:
                    action(events[0])
        time.sleep(MINUTE)       

def main():
    """
    register actions
    call event loop
    """
    actions = [send_text_notificaton]
    event_loop(actions)


if __name__ == '__main__':
    main()
