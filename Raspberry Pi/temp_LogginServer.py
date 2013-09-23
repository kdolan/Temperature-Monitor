"""
***************************
File: temp_LoggingServer.py
***************************

IMPORTANT: Designed to run on raspberrypi

Author: Kevin J Dolan
Project: Live Temp Monitor
Purpose: The LogginServer is designed to be run on a raspberry  pi 
conected to Ds18b20 temperature sensors. The server can be configured to
take a specific number of reads at an interval or an infinate number of 
reads at an interval. 
***************************
Imports: 
 Led: Custom LED class to easily interface with an LED conected to the 
 raspberry pi.
 Ds18b20: Custom class designed to interface with the Ds18b20 temperature sensor.
 time: Used for time logging
 datetime: Used for time logging
 urllib2: Used to load webpage that records the results of the read.
 **************************
"""
from Led import *
from Ds18b20 import *
import time
import datetime
import urllib2

"""
#####***CONSTANTS SECTION***#####
 *Defines Constants used at runtime
"""
#Declare sensors. Note Serial numbers found /sys/bus/w1/devices/
sensor1 = Ds18b20("serialNumberOfSensor")
sensor2 = Ds18b20("serialNumberOfSensor")

#Number of readings to take. If set to 0 then an infinite number of reeds will be taken
readsToTake = 0
#Delay between reads (seconds)
delay = 60

#get time spamp
timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

#open log file for writing
#logFile = open("templog-"+timeStamp, "w")
logFileName = "templog-continuous"
#Live Log Path is the ip address and port where the temp_WebServer.py is running.
#Live Log Path is in the format http://127.0.0.1:8000/tempMonitor?"
liveLogPath = "http://server.host.com:8080/tempMonitor?"

redLed = Led(23)
redLed.ledOff()
#####***END CONSTANTS SECTION***#####

"""
Function used to load webpage that records data.
Uses liveLogPath and appends data read in from the sensors.
"""
def writeLiveData(liveLogPath, sensor1, sensor2):
    data = "sensor1=" + sensor1 + "&sensor2=" + sensor2
    try:
        urllib2.urlopen(liveLogPath + data)
    except Exception:
        return

#####***BEGIN PROGRAM***#####
        
readsTaken = 0
while (readsToTake > readsTaken or readsToTake == 0 ):
    print ("\nRead " + str(readsTaken + 1) + " of " + str(readsToTake) + ".")
    print ("    Poling sensors...")
    redLed.ledOn()
    sensor1_data = str(sensor1.read_temp()[1])
    sensor2_data = str(sensor2.read_temp()[1])
    redLed.ledOff()
    print ("    Information Logged: " + sensor1_data + ", " + sensor2_data)
    writeString = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ", " + sensor1_data + ", " + sensor2_data +"\n"
    with open(logFileName, "a") as logFile:
        logFile.write(writeString)
    readsTaken += 1
    writeLiveData(liveLogPath, sensor1_data, sensor2_data)
    #if loop condition still true then wait before next reading
    if(readsToTake > readsTaken or readsToTake == 0):
        print ("    Delay for " + str(delay) + " seconds.")
        time.sleep(delay)

print("\n#####  Operation complete  #####")
logFile.close()
