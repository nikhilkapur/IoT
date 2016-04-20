#!/usr/bin/python
<<<<<<< HEAD
import os
=======

#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

>>>>>>> 7f143dc0e500bb3c0b116b56961d355fbf8358bf
print "Content-type: text/html\n\n"

print "<pre>"
for k, v in os.environ.items():
    print k, v
