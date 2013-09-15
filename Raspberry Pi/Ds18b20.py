"""
Represents DS18B20 temperature sensors using
a raspberry pi.
Author: Kevin J Dolan
"""

import os
import glob
import time

class Ds18b20:
    
    __slots__ = ( "serialNumber", "temperaturePath" )
    
    PATH_TO_DEVICES = "/sys/bus/w1/devices/" 
    TEMP_FILE_NAME = "/w1_slave"
    
    
    
    def __init__( self, serialNumber ):
        self.serialNumber = serialNumber
        self.temperaturePath = self.PATH_TO_DEVICES + serialNumber + self.TEMP_FILE_NAME
    
    def read_temp_raw(self):
        f = open(self.temperaturePath, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    """
    Returns temperature in celsius and fahrenheit.
    Returns list of two elements (celsius, fahrenheit)
    """
    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f