#!/usr/bin/python

import shelve
from pprint import pprint

data = shelve.open('data.shelve', writeback=True)
pprint(data)

data['status'] = {
    'state': 'Unknown',
    'error': None,
    'last_check': 'Jan 1 1970'
}

data['config'] = {
    'zip': 95138
}

data['details'] = {}
for d in ['day0', 'day1']:
  details = dict()
  details['actual']    = 0.3
  details['threshold'] = 0.5
  details['state']     = details['actual']  > details['threshold'] 
   
  data['details'][d] = details

pprint(data)
data.close()
