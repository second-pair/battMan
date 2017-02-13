#! /bin/python

#  Written by Blair Edwards
#  Created 2017-02-11
#  Modified 2017-02-11
#  Simple python script for a software 1:4 demux
#  This uses a RPi's GPIO pins

#  Import Modules
import RPi.GPIO as GPIO
import time

#  GPIO Setup
GPIO.setmode (GPIO.BCM)  #  Pins use Broadcom's numbering
gpioBtn = 17
gpioPin0 = 27
gpioPin1 = 22
gpioPin2 = 23
gpioPin3 = 24
GPIO.setup (gpioBtn, gpio.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup (gpioPin0, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin3, GPIO.OUT, initial = GPIO.LOW)

def selWithKbd ():
#  Asks for user to select a specific output of the demux
	while True:
		selOut = input ("Which pin would you like to output on?  [0-3, q to quit]  ")
		if selOut == "q":
			print ("Quitting")
			break
		try:
			setOutput (str (selOut))
			print ("Keyboard Entry")

def selWithBtn ():
#  Cycles demux output on button press (polled)
	currOut = 0
	while True:
		if (GPIO.input (gpioBtn)):
			print ("Button Entry")
			setOutput (currOut)
			currOut ++
		else:
			time.sleep (0.01)

def setOutput (outVal):
#  Sets demux ouytput to a specific value
	#  Check Pin 0
	if outVal == "0":
		print ("Writing to Pin 0")
		GPIO.output (gpioPin0, GPIO.HIGH)
	else:
		GPIO.output (gpioPin0, GPIO.LOW)
	#  Check Pin 1
	if outVal == "1":
		print ("Writing to Pin 1")
		GPIO.output (gpioPin1, GPIO.HIGH)
	else:
		GPIO.output (gpioPin1, GPIO.LOW)
	#  Check Pin 2
	if outVal == "2":
		print ("Writing to Pin 2")
		GPIO.output (gpioPin2, GPIO.HIGH)
	else:
		GPIO.output (gpioPin2, GPIO.LOW)
	#  Check Pin 3
	if outVal == "3":
		print ("Writing to Pin 3")
		GPIO.output (gpioPin3, GPIO.HIGH)
	else:
		GPIO.output (gpioPin3, GPIO.LOW)


#def cleanup ():
#  Clean up the bound GPIO channels
GPIO.cleanup ()
