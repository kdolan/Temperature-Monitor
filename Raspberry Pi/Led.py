"""
led.py (for Raspberry pi)
Interface to LED on specified GPIO pin
GPIO mode must be set to BCM
Author: Kevin J Dolan
Created: 7/15/2013
"""
import RPi.GPIO as GPIO
import time

"""
Led class.
Created with GPIO Pin Number
Allows user to toggle the led on and off or
flash the led.
"""
class Led:
    
    """
    Creates instance of Led.
    Parms: 
    gpio_pin: GPIO pin number that the positive
    terminal of the LED is connected to.
    """
    def __init__(self, gpio_pin):
        self.gpio_pin_number = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)
        self.led_on = False

    """
    Led on --> off
    Led off --> on
    (Toggles the state of the led)
    """
    def toggleOutput(self):
        if(self.led_on):
            GPIO.output(self.gpio_pin_number, GPIO.HIGH)
            self.led_on = False
        else:
            GPIO.output(self.gpio_pin_number, GPIO.LOW)
            self.led_on = True
    """
    Flash the led a certain number of times with a given delay.
    Delay in miliseconds
    """
    def flash(self,numberOfFlashes, delay):
        counter = 0
        while(numberOfFlashes > counter):
            counter += 1
            self.toggleOutput()
            time.sleep(delay/1000)
            self.toggleOutput()
            time.sleep(delay/1000)

    """
    Turns the LED ON
    """
    def ledOn(self):
        GPIO.output(self.gpio_pin_number, GPIO.HIGH)
        self.led_on = True
    """
    Turns the LED OFF
    """
    def ledOff(self):
        GPIO.output(self.gpio_pin_number, GPIO.LOW)
        self.led_on = False




    
    
    
