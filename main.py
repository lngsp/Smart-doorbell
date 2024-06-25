import smtplib
import RPi.GPIO as GPIO
import time

from picamera import PiCamera
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Camera Settings
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server
SMTP_PORT = 587 #Server Port
GMAIL_USERNAME = 'proiectsm1310a@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'proiectsm1310a' #change this to match your gmail password

#Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)

#Set digital pin 27(BCM) to an input
GPIO.setup(27, GPIO.IN)

#Set digital pin 27(BCM) to an input and enable the pullup
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Event to detect button press
GPIO.add_event_detect(27, GPIO.FALLING,bouncetime=200)

class Emailer :
	def sendmail(self, recipient, subject, content, image):
	
		# Create Headers
		emailData = MIMEMultipart()
		emailData['Subject'] = subject
		emailData['To'] = recipient
		emailData['From'] = GMAIL_USERNAME
		
		# Attach our text data
		emailData.attach(MIMEText(content))
		
		# Create our Image Data from the defined image
		imageData = MIMEImage(open(image, 'rb').read(), 'jpg')
		imageData.add_header('Content-Disposition', 'attachment;filename="image.jpg"')
		emailData.attach(imageData)
		
		# Connect to Gmail Server
		session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		session.ehlo()
		session.starttls()
		session.ehlo()
		
		# Login to Gmail
		session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
		
		# Send Email & Exit
		session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
		session.quit
		
sender = Emailer()

while True:
	if GPIO.event_detected(27):
		image = '/home/pi/image.jpg'
		camera.capture(image)
		sendTo = 'emiliachelariu28@gmail.com'
		emailSubject = "Someone is at the door!"
		emailContent = "The button has been pressed at: " + time.ctime()
		sender.sendmail(sendTo, emailSubject, emailContent, image)
		print("Email Sent")