import RPi.GPIO as GPIO
import time


class RGBled:
    def __init__(self, red, green, blue, hz=100):
        self.red = red
        self.green = green
        self.blue = blue
        self.hz = hz
        
        GPIO.setup (red, GPIO.OUT)
        GPIO.setup (green, GPIO.OUT)
        GPIO.setup (blue, GPIO.OUT)

        GPIO.output (red, GPIO.LOW)
        GPIO.output (green, GPIO.LOW)
        GPIO.output (blue, GPIO.LOW)

        self.red_pwm   = GPIO.PWM (red,   hz)
        self.green_pwm = GPIO.PWM (green, hz)
        self.blue_pwm  = GPIO.PWM (blue,  hz)

    def change_colors(self, speed = 0.01):
        # Start PWM with duty cycle 0 and then change DC in a loop to get the effect
        self.blue_pwm.start(0)
        self.green_pwm.start(0)
        self.red_pwm.start(0)
        
        for i in range(100):
            self.green_pwm.ChangeDutyCycle(100-i)
            self.blue_pwm.ChangeDutyCycle(i)
            time.sleep (speed)

        self.blue_pwm.start(0)
        self.green_pwm.start(0)
        self.red_pwm.start(0)
        #time.sleep(1)

        for i in range(100):
            self.blue_pwm.ChangeDutyCycle(100-i)
            self.red_pwm.ChangeDutyCycle(i)
            time.sleep (speed)

        self.blue_pwm.start(0)
        self.green_pwm.start(0)
        self.red_pwm.start(0)
        #time.sleep(1)

        for i in range(100):
            self.red_pwm.ChangeDutyCycle(100-i)
            self.green_pwm.ChangeDutyCycle(i/2)
            time.sleep (speed)

        self.blue_pwm.stop()
        self.green_pwm.stop()
        self.red_pwm.stop()

if __name__ == "__main__":
    GPIO.setmode (GPIO.BCM)
    led = RGBled(23, 18, 25)
    for i in range(5):
        led.change_colors()

    GPIO.cleanup()