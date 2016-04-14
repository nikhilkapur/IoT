
#import ultra_sonic
import datetime
#import time
import MySQLdb
import random

def check_level():
    trig_pin = 20                                 #Associate pin 23 to trig_pin
    echo_pin = 21                                  #Associate pin 24 to echo_pin
    #dm = ultra_sonic.DistanceMeasurer(trig_pin, echo_pin)
    #dist = dm.get_dist()
    #return dist
    return random.randrange(2,400)

def send_notification(level):
    pass

def save_data(level):
    db = MySQLdb.connect(host="localhost", user="root", passwd="nkapur", db="salt_monitor")
    cur = db.cursor()
    cur.execute("INSERT INTO salt_level (sl_level, sl_date) VALUES (%s, %s)", (level, datetime.datetime.today()))
    db.commit()
    db.close()


##############################################################

if __name__ == "__main__":
    level = check_level()
    if level < 300:
        send_notification (level)
    save_data(level)
    