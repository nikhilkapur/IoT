#!/usr/bin/python

print "hello world"

import RPi.GPIO as GPIO  
import time

class recliner:
    def init(self
def up(percent=100):
    print "low"
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay)
    print "high"
    GPIO.output(pin, GPIO.HIGH)
    #time.sleep(delay)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

for pin in pins:
    print pin
    toggle_led(pin, delay=8)
    
GPIO.cleanup()

if __name__ == "__main__":
    # Use BCM numbering
    GPIO.setmode(GPIO.BCM)
    
    #pins = [2,3,18,23]
    pins = [17,27]
     
                
