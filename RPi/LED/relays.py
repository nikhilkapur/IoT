#!/usr/bin/python

print "hello world"

import RPi.GPIO as GPIO  
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

pins = [2,3,18,23]
 
def toggle_led(pin, delay=2): 
    print "low"
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay)
    print "high"
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(delay)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

for pin in pins:
    print pin
    toggle_led(pin, delay=2)
    
GPIO.cleanup()
                
