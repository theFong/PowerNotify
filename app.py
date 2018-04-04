
from __future__ import print_function
import httplib2
import os
import sys
import boto3

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.errors import HttpError
from retrying import retry

import datetime
import dateutil.parser
import time
import email_creds

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-powernotify-token.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Power Notify'
LOG_FILE = 'log.txt'
MINUTE = 60.0

# action decorator
def action(tag):
    """
    decorator that checks if tag exists before calling action
    """
    def action_decorator(func):
        def check_tag_wrapper(event_dict):
            if event_dict and event_dict['summary']:
                if tag.lower() in event_dict['summary'].lower():
                    return func(event_dict)
        return check_tag_wrapper
    return action_decorator

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(sys.path[len(sys.path)-1], '.credentials')
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

@action('#powernotify')
def send_text_notificaton(event_dict):
    """
    takes in calendar event
    sends text message
    PhoneNumber = location
    Message = description
    """
    if('location' in event_dict and event_dict['location']):
        number = form_phone_number(event_dict['location'])
        send_sms_message(number, event_dict['description']) if event_dict['description'] else send_sms_message(number, event_dict['summary'])

def time_in_range(start, end, x):
    """
    Return true if x is in the range [start, end]
    """
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def form_phone_number(num_str):
    if '+' in num_str:
        return num_str
    else:
        return '+'+num_str

def is_retriable_error(exception):
    """
    Check if certain http error
    """
    if isinstance(exception, HttpError):
        return exception.resp.status in [403, 500, 503]
    else:
        return False

@retry(retry_on_exception=is_retriable_error, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_google_cal_events():
    """
    gets most recent google cal event
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    eventsResult = service.events().list(
    calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
    orderBy='startTime').execute()
    events = eventsResult.get('items', []) 
    return events

def event_loop(actions):
    """
    checks every minute for event at current time
    calls. limit to one event at the same time
    """
    while(True):

        events = get_google_cal_events()
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
    try:
        actions = [ send_text_notificaton ]
        event_loop(actions)
    except Exception as e:
        send_email(email_creds.email, email_creds.password, email_creds.email, 'POWERNOTIFY FAILURE', str(datetime.datetime.now(datetime.timezone.utc))+' UTC')
        raise e

# deprecated for gmail, must turn on unsecure apps in gmail if you want to use
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


if __name__ == '__main__':
    main()
