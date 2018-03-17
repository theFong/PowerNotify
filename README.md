# PowerNotify

* Python 3.6.4
* AWS SNS
* Google Calendar API

Push SMS notifications for critical events on Google Calendar

Create event on Google calendar with "#PowerNotify" in title/summary and "xxxxxxxxxxx" (11 digit phone number) in location of event. Send personalized messages by adding a description to the Google event.

### Deploy

Install Dependencies
`pip install -r requirements.txt`

Configure AWS CLI making sure AWS_CONFIG_FILE and AWS_SHARED_CREDENTIALS_FILE is set.

Add Google API client client_secret.json file is in working dir.

Run python app.py with a browser and give permissions to access respective google account
`python app.py`

Note: Make sure to add .aws folder and set env variables in activate of environment, add ~/.credentials/calendar-powernotify-token.json manually if no browser exists. Make sure AWS config file's region is set to region=us-east-1, or one which supportes AWS SNS.

`export AWS_CONFIG_FILE=/Users/AlecFong/GoogleDrive/WorkStation/PowerNotify/.aws/config`

`export AWS_SHARED_CREDENTIALS_FILE=/Users/AlecFong/GoogleDrive/WorkStation/PowerNotify/.aws/credentials`
