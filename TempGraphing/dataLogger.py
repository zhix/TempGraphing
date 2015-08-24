#!/usr/bin/python

'''
This program reads data from the serial port (Arduino) and saves it to a text file. 
Format of the data file:
"Time, Temperature in Celcius"

Assumption: Arduino shows up in /dev/ttyACM0 on the RaspPi when using Debian
'''

import serial 
from time import strftime
from datetime import datetime, time

ser = serial.Serial('/dev/ttyACM0',9600)

startTime = datetime.now()

try: 
	while 1: 
		temp = ser.readline().rstrip()
		now = datetime.now()
		elapsedTime = now-startTime
		elapsedSeconds = (elapsedTime.microseconds + (elapsedTime.days * 24 * 3600 + elapsedTime.seconds)*10**6)/10**6
		print("%s,%s,%s" %(now.strftime("%Y-%m-%d %H:%M:%S"), elapsedSeconds, temp))
		f = open("tempLog.dat",'a')
		print >>f, ("%s,%s,%s" %(now.strftime("%Y-%m-%d %H:%M:%S"), elapsedSeconds, temp))
		f.close()

except KeyboardInterrupt:
	print "\ndone"
