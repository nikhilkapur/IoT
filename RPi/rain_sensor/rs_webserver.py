#!/usr/bin/python

import bottle
import shelve
import time
import pprint
import rs_checker

@bottle.route('/')
@bottle.route('/status')
def index():
  data = shelve.open('data.shelve', writeback=True)
  data = sanitize(data)
  tpl = bottle.template('status.tpl' , data=data )
  data.close()
  return tpl
  
@bottle.route('/update')
def update_zip():
  data = shelve.open('data.shelve', writeback=True)
  zipcode = bottle.request.query.get('zipcode')
  data["config"]['zipcode'] = zipcode
  update_status(data)
  data.close()
  return index()

def update_status(data):
    rs = rs_checker.RainSensor(data['config']['zipcode'])
    daily_stats = rs.get_weather()
    sensor = rs.get_status(daily_stats)
    data['daily_stats'] = daily_stats
    data['status'] = {
        'state': sensor,
        'last_check': time.ctime(),
        'error': ''
        }

@bottle.route('/dump')
def dump():
  data = shelve.open('data.shelve', writeback=True)
  html = '<pre>'
  for key in data.keys():
    html += "<br>" + key + "=> "
    html+= pprint.pformat(data[key])
  data.close()
  return html
  
def sanitize(data):
  if not data.has_key('status'):
    data['status'] = {
        'state': 'Unknown',
        'error': None,
        'last_check': 'Jan 1 1970'
    }

  if not data.has_key('config'):
    data['config'] = {
          'zipcode': 95138
    }

  if not data.has_key('daily_stats'):
    data['daily_stats'] = {}
  return data

bottle.run(host='', port=8080)