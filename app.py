import boto3
import time
import cPickle as pickle

min = 60
filename = "log.txt"

class Message(object):
	"""docstring for Message"""
	def __init__(self, phoneNumber, message, timeObj):
		self.phoneNumber = phoneNumber
		self.message = message
		self.timeObj = timeObj

def checkSend(msgs):
	timeObj = time.localtime(time.time())
	for x in msgs:
		if getattr(timeObj,"tm_hour") == x.timeObj["tm_hour"] and getattr(timeObj,"tm_min") == x.timeObj["tm_min"]:
			client = boto3.client('sns')
			response = client.publish(
			    PhoneNumber=x.phoneNumber,
			    Message=x.message,
			    MessageStructure='',
			    MessageAttributes={}
			)
			fh = open(filename, "a")
			fh.writelines([str(response),str(timeObj),str(vars(x)),"\n"])
			fh.close	

messageList = pickle.load( open( "save.p", "rb" ))

while True:
	checkSend(messageList)
	time.sleep(min)