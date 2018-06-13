# PowerNotify

* Python 3.6.4
* AWS SNS
* AWS S3
* Google Calendar API

Push SMS notifications for critical events on Google Calendar

### How

Create event on Google calendar with "#PowerNotify" in title/summary and "1xxxxxxxxxx" (11 digit phone number) in location of event. Send a personalized message instead of title/summary by adding a description to the Google event.

### Build Server

Install Dependencies
`pip install -r requirements.txt`

Configure AWS CLI making sure AWS_CONFIG_FILE and AWS_SHARED_CREDENTIALS_FILE is set.

Add Google API client client_secret.json file in working dir.

Run python app.py with a browser and give permissions to access respective google account
`python app.py`

Note: Make sure to add .aws folder and set env variables in activate of environment, add ~/.credentials/calendar-powernotify-token.json manually if no browser exists. Make sure AWS config file's region is set to region=us-east-1, or one which supportes AWS SNS.

`export AWS_CONFIG_FILE=/Users/AlecFong/GoogleDrive/WorkStation/PowerNotify/.aws/config`

`export AWS_SHARED_CREDENTIALS_FILE=/Users/AlecFong/GoogleDrive/WorkStation/PowerNotify/.aws/credentials`

### Build Serverless
Run this on AWS Lambda

Install Dependencies:

`python3 -m venv env`
`source env/bin/activate`
`pip install -r requirements.txt`

Run locally once to generate .credentials/calendar-powernotify-token.json.
Put calendar-powernotify-token.json in S3 bucket in region the same as your planned Lambda function.
Make sure you create a user, lambda role, and update lambda_deploy.sh.

Build:

`bash lambda_make.sh`

Deploy:

`cd lambda_zip/`

`bash ../lambda_deploy.sh`

Configure Trigger:

On aws console/lambda, setup a CloudWatch event with rule
`cron(* * * * ? *)`

![screen shot](https://raw.githubusercontent.com/theFong/PowerNotify/master/Screen%20Shot%202018-03-17%20at%203.40.12%20PM.png)




