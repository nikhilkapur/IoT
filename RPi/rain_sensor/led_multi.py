import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BCM)

red = 23
green = 18
blue = 25

GPIO.setup (green, GPIO.OUT)
GPIO.setup (red, GPIO.OUT)
GPIO.setup (blue, GPIO.OUT)
#
#GPIO.output (red, GPIO.LOW)
#GPIO.output (green, GPIO.LOW)
#GPIO.output (blue, GPIO.LOW)
#
#GPIO.output (red, GPIO.HIGH)
#time.sleep (1)
#GPIO.output (red, GPIO.LOW)
#GPIO.output (green, GPIO.HIGH)
#time.sleep (1)
#GPIO.output (green, GPIO.LOW)
#GPIO.output (blue, GPIO.HIGH)
#time.sleep (1)

GPIO.output (red, GPIO.LOW)
GPIO.output (green, GPIO.LOW)
GPIO.output (blue, GPIO.LOW)

red_pwm = GPIO.PWM(red, 100)
green_pwm = GPIO.PWM(green, 100)
blue_pwm = GPIO.PWM(blue, 100)

blue_pwm.start(0)
green_pwm.start(0)
red_pwm.start(0)

def change_colors():
    speed = 0.01
    for i in range(100):
        green_pwm.ChangeDutyCycle(100-i)
        blue_pwm.ChangeDutyCycle(i)
        time.sleep (speed)
    
    blue_pwm.start(0)
    green_pwm.start(0)
    red_pwm.start(0)
    #time.sleep(1)
    
    for i in range(100):
        blue_pwm.ChangeDutyCycle(100-i)
        red_pwm.ChangeDutyCycle(i)
        time.sleep (speed)
    
    blue_pwm.start(0)
    green_pwm.start(0)
    red_pwm.start(0)
    #time.sleep(1)
    
    for i in range(100):
        red_pwm.ChangeDutyCycle(100-i)
        green_pwm.ChangeDutyCycle(i/2)
        time.sleep (speed)

for i in range(5):
    change_colors()

GPIO.cleanup()

