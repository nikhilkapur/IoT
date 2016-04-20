
import ultra_sonic
import datetime
#import time
import MySQLdb
import random
import os

def check_level():
    trig_pin = 18                                 #Associate pin 23 to trig_pin
    echo_pin = 23                                  #Associate pin 24 to echo_pin
    dm = ultra_sonic.DistanceMeasurer(trig_pin, echo_pin)
    dist = dm.get_dist()
    return dist
    #return random.randrange(2,400)

def send_notification(level):

    sender = 'salt-monitor@pizero'
    recipients = ['nikhil@kapurs.net']
    subject = "Salt Level Low [%d]" % level
    text = "http://home.kapurs.net:11680/cgi-bin/salt-monitor/salt_chart.py?days=60&show_raw=0"
        
    status = send_mail (sender, recipients, subject, text)


def send_mail(sender, recipients, subject, text):
    message = """From: %s\nTo: %s\nSubject: %s

    %s 
    """ % (sender, ", ".join(recipients), subject, text)

    p = os.popen("/usr/sbin/sendmail -t -i", "w")
    p.write(message)
    status = p.close()
    return status



def save_data(level):
    db = MySQLdb.connect(host="localhost", user="salt_monitor", passwd="salt_monitor123", db="salt_monitor")
    cur = db.cursor()
    cur.execute("INSERT INTO salt_level (sl_level, sl_date) VALUES (%s, %s)", (level, datetime.datetime.today()))
    db.commit()
    db.close()


##############################################################

if __name__ == "__main__":
    level = check_level()
    if level > 60:
        send_notification (level)
    save_data(level)
    print level
    
