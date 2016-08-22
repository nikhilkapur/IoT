import os

def send_mail(sender, recipients, subject, text):
    message = """From: %s\nTo: %s\nSubject: %s

    %s
    """ % (sender, ", ".join(recipients), subject, text)

    print message

    p = os.popen("/usr/sbin/sendmail -t -i", "w")
    p.write(message)
    status = p.close()
    return status


sender = 'salt-monitor@pizero'
recipients = ['nikhil@kapurs.net']
subject = "Some sub1"
text = "some text"

status = send_mail (sender, recipients, subject, text)
