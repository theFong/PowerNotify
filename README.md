# PowerNotify

Python 3.6.4

Push SMS notifications for critical events on Google Calendar

Create event on google calendar with "#PowerNotify" in title/summary and "xxxxxxxxxxx" (11 digit phone number) in location of event
Can personalize message by specifiying message in description of event

Run python app.py and give permission to access respective google account


Note: Make sure to add .aws folder and set env variables in activate of environment, add client_secret.json in working dir, add ~/.credentials/calendar-powernotify-token.json if no browser

`
export AWS_CONFIG_FILE=/Users/AlecFong/GoogleDrive/WorkStation/PowerNotify/.aws/config

export AWS_SHARED_CREDENTIALS_FILE=/Users/AlecFong/GoogleDrive/WorkStation/PowerNotify/.aws/credentials
`
