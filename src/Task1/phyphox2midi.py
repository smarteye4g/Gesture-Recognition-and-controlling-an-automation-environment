#phyphox configuration
PP_ADDRESS = "http://192.168.178.20"
PP_CHANNELS = ["accX", "accY", "accZ"] #If using different CC channels, define multiple phyphox buffers

import urllib, json
import requests
import time

def start_stop_point():
	start_time = time.time()
	count = 1;
	while(time.time()<(start_time.seconds+3)):
		a = data["buffer"]["accZ"]["buffer"]
		if((a>9.6 and a<9.9)==True):
			count = 0
			print count
	return count


while True:
	url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
	data = requests.get(url=url).json()
	ax = data["buffer"]["accX"]["buffer"]
	ay = data["buffer"]["accY"]["buffer"]
	az = data["buffer"]["accZ"]["buffer"]
	print az
	if((az>9.6 and az<9.9) == True):
		print az
		valid = start_stop_point()
		print valid
