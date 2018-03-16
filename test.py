import boto3

"""
Test boto3 auth and text message
"""

phone_number = '+1xxxxxxxxxx'

# change to real number
if phone_number == '+1xxxxxxxxxx':
	raise NotImplementedError

client = boto3.client('sns')
response = client.publish(
    PhoneNumber=phone_number,
    Message='Testing auth and message. APPEARS VALID',
    MessageStructure='',
    MessageAttributes={}
)


