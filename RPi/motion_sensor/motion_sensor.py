import RPi.GPIO as GPIO
import time

class Motion:
    '''Check library that interfaces with the HC-SR501
        Reference https://electrosome.com/pir-motion-sensor-hc-sr501-raspberry-pi/
    '''
    
    def __init__(self, trig_pin, settle_time=1):
        self.trig_pin = trig_pin
        self.settle_time = settle_time
        
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(trig_pin, GPIO.IN)
        time.sleep(self.settle_time)

    def is_motion(self):
        '''Check if there is motion right now
            Ensure that if True, dont check for another 2 seconds (avoid multiple positives)
                        if False, dont check for 0.1 seconds (hardware limitation)
        '''
        if GPIO.input(self.trig_pin):
            return True
        return False

    def wait_for_motion(self, max_delay=300):
        '''Wait for motion
           Wait for max_delay seconds (default 300)
        '''
        start = time.time()
        time.sleep(self.settle_time)
        
        while start+max_delay > time.time():
            if self.is_motion():
                return True, time.time() - start
        return False, time.time() - start

##############################################################################################################

if __name__ == "__main__":
    trig_pin = 23
    mot = Motion(trig_pin)
    print "Waiting for motion for 10 seconds"
    (found, tm) = mot.wait_for_motion(10)
    if found:
        print "Found motion in %f seconds" % tm
        time.sleep(2)
    else:
        print "No motion found in %f seconds" % tm
        time.sleep(0.1)

    print "Waiting for motion for 3 seconds"
    (found, tm) = mot.wait_for_motion(3)
    if found:
        print "Found motion in %f seconds" % tm
    else:
        print "No motion found in %f seconds" % tm
            
        


    