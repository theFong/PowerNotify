import boto3
import time
import cPickle as pickle

class Message(object):
	"""docstring for Message"""
	def __init__(self, phoneNumber, message, timeObj):
		self.phoneNumber = phoneNumber
		self.message = message
		self.timeObj = timeObj

m = Message("+***********","*message here*", {"tm_hour":18,"tm_min":55})

mList = [m]

pickle.dump( mList, open( "save.p", "wb" ) )

# client = boto3.client('sns')
# response = client.publish(
#     PhoneNumber='+19494859948',
#     Message='Test Py',
#     MessageStructure='',
#     MessageAttributes={}
# )


