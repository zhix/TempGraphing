#!/usr/bin/python

#########################################################
# This program does the following:
# 1) reads data from the serial port (Arduino) 
# 2) saves data to a text file
# 3) posts data to a phant server (data.sparkfun.com)
#
# Format of the data file:
# "Time, Temperature in Celcius"
#
# Format of the data to phant server:
# "time, temp"
#
# Assumption: Arduino shows up in /dev/ttyACM0 on the RaspPi when using Debian
#
# **modified from: 
# 1) https://learn.sparkfun.com/tutorials/pushing-data-to-datasparkfuncom/raspberry-pi-python
# 2) www.benk.ca/node/10
###########################################################

import serial 		#serial programs arduino with python
import httplib, urllib 	#http and url libs used for HTTP POSTs
from time import strftime
from datetime import datetime, time
import time

ser = serial.Serial('/dev/ttyACM0',9600)

startTime = datetime.now()

## Phant server
server = "data.sparkfun.com" 	#base url of your feed
publickey = "yAV5DK5jxbuGaDxNwOQO"
privatekey = "4WADKnDbXRhPqdypejAj"
fields = ["time","temp"]

try: 
	while 1: 
		print("Sending an update!")
		temp = ser.readline().rstrip()
		now = datetime.now()
#		elapsedTime = now-startTime
#		elapsedSeconds = (elapsedTime.microseconds + (elapsedTime.days * 24 * 3600 + elapsedTime.seconds)*10**6)/10**6
#		print("%s,%s,%s" %(now.strftime("%Y-%m-%d %H:%M:%S"), elapsedSeconds, temp))
#		f = open("tempLog_try_delete.dat",'a')
#		print >>f, ("%s,%s,%s" %(now.strftime("%Y-%m-%d %H:%M:%S"), elapsedSeconds, temp))
#		f.close()

		## Creating data set
		data = {}
#		data[fields[0]] = str(now.strftime("%Y-%m-%d %H:%M:%S"))
		data[fields[0]] = now.strftime("%c")
		data[fields[1]] = temp
		params = urllib.urlencode(data)
#		print data
#		print params

		## Setting up headers - these are static, should be here everytime:
		headers={}
		headers["Content-Type"]= "application/x-www-form-urlencoded"
		headers["Connection"] = "close"
		headers["Content-Length"] = len(params)
		headers["Phant-Private-Key"] = privatekey
#		print headers

		## Initiate connection and post the data
		c = httplib.HTTPConnection(server)
		# Here's the magic, our request format is POST, we want to send data to data.sparkfun.com/input/PUBLIC_KEY.txt
		# and include both our data (i.e. params) and headers
		c.request("POST", "/input/" + publickey + ".txt", params, headers)
		r = c.getresponse()
		print r.status, r.reason
		
		time.sleep(300)

except KeyboardInterrupt:
	print "\ndone"
