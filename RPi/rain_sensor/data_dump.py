#!/usr/bin/python

import shelve
from pprint import pprint

data = shelve.open('data.shelve', writeback=True)

for key in data.keys():
    print key
    pprint (data[key])
