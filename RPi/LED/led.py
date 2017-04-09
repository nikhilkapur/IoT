#!/usr/bin/python

print "hello world"

import RPi.GPIO as GPIO  
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)
 
# Set pin 12 to output mode
led_port_list = [24,25,7]
GPIO.setup(12, GPIO.OUT)

def toggle_led(pin, delay=2): 
    print "high"
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(delay)
    print "low"
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay)

for port in led_port_list:
    toggle_led(port, delay=2)
    
GPIO.cleanup()
                