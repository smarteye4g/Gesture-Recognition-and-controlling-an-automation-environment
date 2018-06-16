#phyphox configuration
PP_ADDRESS = "http://192.168.178.20" #IP Address of the local pc
PP_CHANNELS = ["accX", "accY", "accZ"] #currently not used in the code. To be used at the time of optimization

import requests
import time

while True:
	url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
	data = requests.get(url=url).json()
        ax = data["buffer"]["accX"]["buffer"]
	ay = data["buffer"]["accY"]["buffer"]
	az = data["buffer"]["accZ"]["buffer"]
        print("Ax = " + str(ax) + "Ay = " + str(ay) + "Az = " + str(az))
