#! /bin/python
import RPi.GPIO as GPIO
from time import sleep
testPin = 23
GPIO.setmode (GPIO.BCM)
GPIO.setup (testPin, GPIO.OUT)
while True:
	GPIO.output (testPin, GPIO.HIGH)
	sleep (1)
	GPIO.output (testPin, GPIO.LOW)
	sleep (1)
