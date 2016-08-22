# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
#fp = open(textfile, 'rb')
#msg = MIMEText(fp.read())
#fp.close()

sender = 'salt-monitor@pizero'
recipient = 'nikhil@kapurs.net'

msg = MIMEText('Some text')
msg['Subject'] = 'mail from python'
msg['From'] = sender
msg['To'] = recipient

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail(sender, [recipient], msg.as_string())
s.quit()
