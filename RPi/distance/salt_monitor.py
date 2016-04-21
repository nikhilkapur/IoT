
import ultra_sonic
import datetime
#import time
import MySQLdb
#import random
import os
import ConfigParser

def check_level():
    trig_pin = 18                                 #Associate pin 23 to trig_pin
    echo_pin = 23                                  #Associate pin 24 to echo_pin
    dm = ultra_sonic.DistanceMeasurer(trig_pin, echo_pin)
    dist = dm.get_dist()
    return dist
    #return random.randrange(2,400)

def send_notification(level, config):

    sender = config.get('general', 'sender')
    recipients = [config.get('general', 'recipient')]
    text = config.get('general', 'chart_url')
    subject = "Salt Level Low [%d]" % level
        
    status = send_mail (sender, recipients, subject, text)
    return status


def send_mail(sender, recipients, subject, text):
    message = """From: %s\nTo: %s\nSubject: %s

    %s 
    """ % (sender, ", ".join(recipients), subject, text)

    p = os.popen("/usr/sbin/sendmail -t -i", "w")
    p.write(message)
    status = p.close()
    return status



def save_data(level, config):
    db_host = config.get('database', 'db_host')
    db_name = config.get('database', 'db_name')
    db_user = config.get('database', 'db_user')
    db_password = config.get('database', 'db_password')
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
    cur = db.cursor()
    cur.execute("INSERT INTO salt_level (sl_level, sl_date) VALUES (%s, %s)", (level, datetime.datetime.today()))
    db.commit()
    db.close()


##############################################################

if __name__ == "__main__":

    config = ConfigParser.ConfigParser()
    config.read('salt_monitor.cfg')
    
    level = check_level()
    if level > 60:
        send_notification (level, config)
    save_data(level, config)
    print level
    
