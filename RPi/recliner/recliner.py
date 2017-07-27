DONT USE !!!! Moved to separate respository on gitlab


#!/usr/bin/python

from __future__ import division

import RPi.GPIO as GPIO
#import gpio as GPIO
  
import time
import os
import cgi
import cgitb
cgitb.enable()


class recliner:
    def __init__(self, up_pin=27, down_pin=17, on_level=GPIO.LOW, gpio_mode=GPIO.BCM, recline_time=9):
        GPIO.setmode(gpio_mode)
        self.recline_time = recline_time
        self.up_pin = up_pin
        self.down_pin = down_pin
        if on_level == GPIO.LOW:
            self.on_level  = GPIO.LOW
            self.off_level = GPIO.HIGH
        else:
            self.on_level  = GPIO.HIGH
            self.off_level = GPIO.LOW

        self.init()
    
    def init(self):
        GPIO.setup(self.up_pin, GPIO.OUT, initial=self.off_level)
        GPIO.setup(self.down_pin, GPIO.OUT, initial=self.off_level)
    
    def up(self, percent=100):
        duration = int(self.recline_time * percent/100 +0.5)
        GPIO.output(self.up_pin, self.on_level)
        time.sleep(duration)
        GPIO.output(self.up_pin, self.off_level)

    def down(self, percent=100):
        duration = int(self.recline_time * percent/100 +0.5)
        GPIO.output(self.down_pin, self.on_level)
        time.sleep(duration)
        GPIO.output(self.down_pin, self.off_level)
             
    
if os.environ.get('SCRIPT_NAME') != None:
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    command = form.getvalue('command', '')
    percent = int(form.getvalue('percent', 100))
    r = recliner ()
    if command == 'up':
        r.up(percent)
    if command == 'down':
        r.down(percent)

    print "Done"

elif __name__ == "__main__":
    r = recliner ()
    #r.up()
    #time.sleep(2)
    #r.down()
    #time.sleep(2)

    r.up(20)
    time.sleep(2)
    r.down(20)
    time.sleep(2)

    GPIO.cleanup()

