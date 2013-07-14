#External library.
#http://docs.python-requests.org/en/latest/
import requests

#Internal libraries.
import sys
import smtplib
import datetime
import time
import threading

#Email Login Settings
smtpLoginId = 'login'
smtpPassword = 'password'

#Default settings
timeOutVal = 60 #time out after the site has not responded for one minute.
webSites = {'SiteName1': 'WebsiteUrl1', 'SiteName2': 'WebsiteUrl2'}
sender = 'sender@email.com'
receiver = 'receiver@gmail.com'
message = """\
From: {0}
To: {1}
Subject: {2} Website Down

The website {3} is reported down at {4}.

Details: {5}

"""

class checkWebsiteThread(threading.Thread):

	#Constructor...
	def __init__(self, websiteName, websiteUrl, sleepTime=None):
		threading.Thread.__init__(self)
		self.websiteUrl = websiteUrl
		self.websiteName = websiteName
		self.isAlive = True
		if sleepTime is None:
			self.sleepTime = 300
		else:
			self.sleepTime = sleepTime

	#Run method invoked when the thread starts.
	def run(self):
		print('>>Beginning site checking for site {0}\n').format(self.websiteUrl)
		while self.isAlive:
			if self.checkWebsite(self.websiteName, self.websiteUrl):
				time.sleep(self.sleepTime)
			else:
				self.isAlive = False
		print('>>Site checking for site {0} has stopped.\n').format(self.websiteUrl)

	#Stops the threads internal loop.
	def stop(self):
		self.isAlive = False

	#Perform the actual check website logic.
	def checkWebsite(self, websiteName, websiteUrl):
		#Default to no error message.
		errorMessage = None

		#Attempt to perform a head request on the website with time-out
		#in seconds based on the timeOutVal
		try:
			#r = requests.head(websiteUrl, timeout=timeOutVal)
			#r.raise_for_status()
			print('rquest')
		except:
			e = sys.exc_info()
			errorMessage = str(e[0]) + '\r\n' + str(e[1])

		timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		#An error has occured, attempt to email the issue to receiver.
		if errorMessage != None:
			try:
				compiledMessage = message.format(sender, receiver, websiteName, websiteUrl, timeStamp, errorMessage)
				smptObj = smtplib.SMTP('smtp.gmail.com:587')
				smptObj.starttls()
				smptObj.login(smtpLoginId, smtpPassword)
				smptObj.sendmail(sender, receiver, compiledMessage)
				smptObj.quit()
				print('>>The site {0} was reported down at {1} with the error {2}.\n').format(websiteName, timeStamp, errorMessage)
			except:
				print(sys.exc_info())
				return False
		#Write to the console that everything is okay.
		else:
			print('>>The site {0} was reported good at {1}.\n').format(websiteUrl, timeStamp)

		return True

#Main execution.
threads = []
for key in webSites.keys():
	thread = checkWebsiteThread(key, webSites[key])
	threads.append(thread)
	thread.start()

isAlive = True

#Control loop.
while isAlive:

	#Get the user input.
	input = raw_input('').lower()
	#Stop the control loop and shutdown the script.
	if input == 'stop':
		isAlive = False

#Clean-up
print('>>Stopping the script.\n')

for thread in threads:
	thread.stop()