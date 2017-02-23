#! /bin/python

#  Written By:  Blair Edwards
#  Modified:  2017-04-13
#  Programme to act as main communications between Pi and PC,
#    for the communications hub part of the system
#  This system should set up comms with the PC, wait for an initialisation
#    and then enter the cyclic communications cycle
#  The 'demux.py' programme could then be easily implemented to
#    control the GPIO pins
#  This system...  Doesn't work!  We're not sure if it's this programme, the
#    PC programme, or something else entirely

import serial
from time import sleep as sleep
import signal

##  Data
#  0 Shutdown
#  1 Init
#  2 NOP (Nothing to Send)

bankCount = 7  #  How many battery banks to charge (no more than 7 without updating the PC)
currChain = 3  #  Which chain we're charging (indexing from 1)
sendFunc = 4  #  Which function to send next

theVoltages = []  #  Voltages for banks read from PC
theCurrents = []  #  Currents for banks read from PC
theSoC = [72, 73, 74, 78, 76, 77, 78]  #  State of Charge received from Coulomb Count

def init ():
	#  Check bank count is sensible
	if (bankCount <= 0) | (bankCount > 7):
		print ("Invalid bank count!  Must be less than 7 without updating the PC.")
		cleanup ()
	#  Populate lists
	for i in range (1, bankCount):
		theVoltages.append (0)
		theCurrents.append (0)
		#theSoC.append (0)
	
	#  Wait for handshake
	#  Timeout?
	timeout = 40
	#  Wait for PC handshake
	print ("Waiting for PC handshake...")
	while recvOnce () != "1":
		#  Decrementes 'timeout' once per loop, resulting in a handshake
		#    timeout if nothing received in time
		timeout -= 1
		if timeout <= 0:
			print ("Connection timed out!  No handshake received from PC.")
			cleanup ()
		sleep (1)
	print ("Handshake received!")
	return
	
def captureCC (signal, frame):
	print ("\nCtrl-C received!  Shutting down...")
	cleanup ()

def cleanup ():
	port.close ()
	exit (0)
	return


def sendPCData (send):
	#  Function to send data to PC
	print ("Sending:  " + str (send))
	send = str (send) + "\r\n"
#	sleep (1)
	port.write (send .encode ('ASCII'))
	return

def recvPCData ():
	recv = ""
	#  Function to wait for data from PC
	#  Programme timeout
	while recv == "":
		recv = port.read (10) .decode ("ASCII") [:-4]
#		print (recv)
		sleep (0.1)
	print ("Received:  " + recv)
	return recv
def recvOnce ():
	#  Receive one line from the PC, regardless of message content
	data = port.read (10) .decode ("ASCII") [:-4]
#	print (data)
	return data


def sendPC ():
	#  Send the 'dataType' to the PC, then the relevant line
	#  Then loop to next 'dataType' to send
	global sendFunc
	sendPCData (sendFunc)
	#sleep (1)
	if sendFunc == 0:
		sendSDown ()
	elif sendFunc == 2:
		sendNOP ()
	elif sendFunc == 4:
		sendChain ()
		sendFunc = 5
	elif sendFunc == 5:
		sendSoC ()
		sendFunc = 4
	else:
		print ("Not a valid function to send!")
	return
		
def recvPC ():
	#  Receive the 'dataType' from the PC, then handle the subsequent
	#    line accordingly
	recvFunc = recvPCData ()
#	sleep (1)
	if recvFunc == 0:
		recvSDown ()
	elif recvFunc == "2":
		recvNOP ()
	elif recvFunc == "3":
		recvStartStop ()
	elif recvFunc == "6":
		recvVoltage ()
	elif recvFunc == "7":
		recvCurrent ()
	else:
		print ("Did not receive a valid function!")
	return


#  F0 - Shutdown
def sendSDown ():
	sendPCData (0)
def recvSDown ():
	print ("Received shutdown from PC.  Shutting down...")
	cleanup ()
	return

#  F1 - Initialisation
#  F2 - NOP
def sendNOP ():
	sendPCData (2)
	return
def recvNOP ():
	return
	
#  F3 - PC -> Start/Stop
def recvStartStop ():
	#  Handle Later
	return
	
#  F4 - Pi -> Presently Charging Chain
def sendChain ():
	sendPCData (currChain)
	return
	
#  F5 - Pi -> SoC (Percentage Charged)
def sendSoC ():
	sendPCData (theSoC [currChain])
	return
	
#  F6 - PC -> Voltage
def recvVoltage ():
	global theVoltages
	theVoltages [currChain] = recvPCData ()
	return
	
#  F7 - PC -> Current
def recvCurrent ():
	global theCurrents
	theCurrents [currChain] = recvPCData ()
	return

#  Setup ctrl-c catching
signal.signal (signal.SIGINT, captureCC)

#  Initialise serial port
port = serial.Serial ("/dev/ttyAMA0", baudrate=9600, timeout=0.1)

init ()

while True:
	#  This should simply parform the cyclic part of the cyclic model
	sendPC ()
	sleep (1)
	recvPC ()
	sleep (1)

#  Kev.py
