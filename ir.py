import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
pin=37
GPIO.setup(pin,GPIO.IN)
def detection():
	if GPIO.input(pin):
		a=1
	else:
		a=0
	return a	

