#!/usr/bin/python
import os
print "Content-type: text/html\n\n"

print "<pre>"
for k, v in os.environ.items():
    print k, v
