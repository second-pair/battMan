#! /bin/python

#  Written by Blair Edwards
#  Created 2017-02-11
#  Modified 2017-02-14
#  Simple python script for a software 1:4 demux
#  This uses a RPi's GPIO pins

#  Import Modules
import RPi.GPIO as GPIO
import time
import signal
import sys

#  GPIO Setup
GPIO.setmode (GPIO.BOARD)  #  Pins use Broadcom's numbering
gpioBtn = 11
gpioPin0 = 13
gpioPin1 = 15
gpioPin2 = 16
gpioPin3 = 18
GPIO.setup (gpioBtn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup (gpioPin0, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin3, GPIO.OUT, initial = GPIO.LOW)

GPIO.output (gpioPin2, GPIO.HIGH)
input ("...")
sys.exit (0)

def selWithKbd ():
	#  Asks for user to select a specific output of the demux
	while True:
		selOutRaw = input ("Which pin would you like to output on?  [0-3]  ")
		try:
			selOut = int (selOutRaw)
		except:
			print ("Please enter a valid integer.")
		#  Check for suitable number
		if selOut >= 0 and selOut < 4:
			setOutput (selOut)
		else:
			print ("Please enter a number between 1 and 4.")
	return


def selWithBtn ():
	#  Cycles demux output on button press (polled)
	print ("Please press the button to cycle the output.")
	currOut = 0
	while True:
		if (GPIO.input (gpioBtn)):
			setOutput (currOut)
			currOut += 1
			if currOut > 3:
				currOut = 0
			time.sleep (0.01)
			while (GPIO.input (gpioBtn)):
 				pass
		else:
			time.sleep (0.01)
	return


def setOutput (outVal):
	#  Sets demux ouytput to a specific value
	#  Check Pin 0
	if outVal == 0:
		print ("Writing to Pin 0")
		GPIO.output (gpioPin0, GPIO.HIGH)
	else:
		GPIO.output (gpioPin0, GPIO.LOW)
	#  Check Pin 1
	if outVal == 1:
		print ("Writing to Pin 1")
		GPIO.output (gpioPin1, GPIO.HIGH)
	else:
		GPIO.output (gpioPin1, GPIO.LOW)
	#  Check Pin 2
	if outVal == 2:
		print ("Writing to Pin 2")
		GPIO.output (gpioPin2, GPIO.HIGH)
	else:
		GPIO.output (gpioPin2, GPIO.LOW)
	#  Check Pin 3
	if outVal == 3:
		print ("Writing to Pin 3")
		GPIO.output (gpioPin3, GPIO.HIGH)
	else:
		GPIO.output (gpioPin3, GPIO.LOW)
	return


def cleanup (signal, frame):
	#  Cleanup function to exit gracefully
	print ("\n\nctrl-c captured!  Cleaning up...")
	#  Clean up the bound GPIO channels
	GPIO.output (gpioPin0, GPIO.LOW)
	GPIO.output (gpioPin1, GPIO.LOW)
	GPIO.output (gpioPin2, GPIO.LOW)
	GPIO.output (gpioPin3, GPIO.LOW)
	GPIO.cleanup ()
	print ("Cleanup complete!  Exiting...")
	sys.exit (0)


#  Setup ctrl-c capturing
signal.signal (signal.SIGINT, cleanup)

while True:
	modeSel = input ('Run in Keyboard ("k") or Button ("b") mode?  ')
	if modeSel == "k":
		selWithKbd ()
	elif modeSel == "b":
		selWithBtn ()
	else:
		print ("That was not a valid selection.")

#  Shouldn't get here
cleanup ()
