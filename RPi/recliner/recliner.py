#!/usr/bin/python

from __future__ import division

#import RPi.GPIO as GPIO
import gpio as GPIO
  
import time

class recliner:
    def init(self, up_pin=17, down_pin=27, on_level=GPIO.LOW, gpio_mode=GPIO.BCM, recline_time=10):
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
        self.reset()
    
    def reset(self):
        GPIO.output(self.up_pin, self.off_level) 
        GPIO.output(self.down_pin, self.off_level) 
    
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
             
    
if __name__ == "__main__":
    r = recliner (up_pin=17, down_pin=27)
    r.up()
    time.sleep(2)
    r.down()
    time.sleep(2)

    r.up(50)
    time.sleep(2)
    r.down(50)
    time.sleep(2)

    GPIO.cleanup()

     
                
