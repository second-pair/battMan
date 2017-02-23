#! /bin/python

#  Written by Blair Edwards
#  Created 2017-02-11
#  Modified 2017-04-13
#  Simple python script for a software 1:4 demux (can be expanded)
#  This uses a RPi's GPIO pins
#  The programme should exit cleanly at any time by sending a ^C interrupt

#  Import Modules
import RPi.GPIO as GPIO
import time
import signal
import sys
import serial

#  GPIO Setup
relayCount = 2
GPIO.setmode (GPIO.BOARD)  #  Pins use Broadcom's numbering
gpioPin0 = 13
gpioPin1 = 15
gpioPin2 = 16
gpioPin3 = 18
GPIO.setup (gpioPin0, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup (gpioPin3, GPIO.OUT, initial = GPIO.LOW)
prevOutVal = -1  #  No initial value!
#  Note about potential future assignments:
#  The Pi has plenty of available output pins, most of which can be used for
#    controlling the relay-controlling transistors
#  Pins 13, 15, 16, 18 were chosen as they're pure IO pins (don't have any
#    other functions such as the mini-UART), are 4 pins grouped closely and
#    are protected by the Custard Pi board
#  If more pins are required, these can be chaged to whatever, but the hardware
#    circuitry will need to be re-wired to use these pins (should be easy)


def selWithKbd ():
	#  Asks for user to select a specific output of the demux
	while True:
		selOutRaw = input ("Which pin would you like to output on?  [0-" + str (relayCount - 1) + "]  ")
		try:
			#  Try to capture non-integer input
			selOut = int (selOutRaw)
		except:
			print ("Please enter a valid integer.")
		#  Check for suitable number
		if selOut >= 0 and selOut < relayCount:
			setOutput (selOut)
		else:
			print ("Please enter a number between 0 and " + str (relayCount - 1) + ".")
	return


def cycleWithSerial ():
	#  Cycles demux output when serial signal received
	#  Set initial GPIO state
	setOutput (0)
	currOut = 1
	
	while True:
		#  Loop until serial input received
		while (port.read (10) .decode ("ASCII")) == "":
			pass
		#  Cycle GPIO output
		setOutput (currOut)
		#  Pre-set next GPIO state
		if currOut >= (relayCount - 1):
			currOut = 0
		else:
			currOut = currOut + 1
		
		time.sleep (1)
	return


def setOutput (outVal):
	#  Sets demux ouytput to a specific value
	#  Declare the global variable 'prevOutVal'
	global prevOutVal

	#  Check if realy value is out of range (calling functions should handle this)
	if outVal < 0:
		print ("\nsetOutput:  outVal < 0")
	elif outVal >= relayCount:
		print ("\nsetOutput:  outVal >= relayCount")
	
	#  Relay value in range, let's proceed
	else:
		if outVal == prevOutVal:
			#  Nothing to do here
			print ("Previous output of " + str (prevOutVal) + " the same, not changing anything")
		else:
			#  Set previously stored pin LOW
			print ("Setting previous pin " + str (prevOutVal) + " LOW")
			if prevOutVal == 0:
				GPIO.output (gpioPin0, GPIO.LOW)
			if prevOutVal == 1:
				GPIO.output (gpioPin1, GPIO.LOW)
			if prevOutVal == 2:
				GPIO.output (gpioPin2, GPIO.LOW)
			if prevOutVal == 3:
				GPIO.output (gpioPin3, GPIO.LOW)
			
			#  Set the new pin HIGH
			print ("Setting new pin " + str (outVal) + " HIGH")
			if outVal == 0:
				GPIO.output (gpioPin0, GPIO.HIGH)
			if outVal == 1:
				GPIO.output (gpioPin1, GPIO.HIGH)
			if outVal == 2:
				GPIO.output (gpioPin2, GPIO.HIGH)
			if outVal == 3:
				GPIO.output (gpioPin3, GPIO.HIGH)
			
			prevOutVal = outVal
			
	return


def captureCC (signal, frame):
	#  Cleanup function to exit gracefully
	print ("\n\nctrl-c captured!  Cleaning up...")
	cleanup ()


def cleanup ():
	#  Clean up the bound GPIO channels
	GPIO.output (gpioPin0, GPIO.LOW)
	GPIO.output (gpioPin1, GPIO.LOW)
	GPIO.output (gpioPin2, GPIO.LOW)
	GPIO.output (gpioPin3, GPIO.LOW)
	GPIO.cleanup ()
	print ("Cleanup complete!  Exiting...")
	sys.exit (0)


#  Only 4 relay positions programmed for now
if relayCount < 1:
	print ("\n\nYou can't have less than 1 output!\nPlease set 'relayCount' to a number greater than 0.")
	cleanup ()
elif relayCount > 4:
	print ("\n\nToo many relays!\nIf you want to use more than 4, you will need to hard-code the GPIO addresses, add them to 'setOutput' and then edit here to squelch this code.")
	cleanup ()

#  Setup ctrl-c capturing
signal.signal (signal.SIGINT, captureCC)

#  Setup Serial with PC
port = serial.Serial ("/dev/ttyAMA0", baudrate=9600, timeout=0.1)

while True:
	#  Check which control method the user wants
	modeSel = input ('Run in Keyboard ("k") or Serial ("s") mode?  ')
	if modeSel == "k":
		selWithKbd ()
	elif modeSel == "s":
		cycleWithSerial ()
	else:
		print ("That was not a valid selection.")

#  Shouldn't get here
cleanup ()
