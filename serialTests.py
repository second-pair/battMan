import serial

port = serial.Serial ("/dev/ttyAMA0", baudrate=9600, timeout=5.0)

while True:
	port.write ("\r\n12345".encode ('ASCII'))
	rcv = port.read (10)
	print ("Received:" + repr (rcv))


