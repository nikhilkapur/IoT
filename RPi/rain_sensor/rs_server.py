#!/usr/bin/python
import os
import bottle
import shelve
import pprint
import time
import rs_checker

@bottle.route('/')
def main():
    data = shelve.open('data.shelve', writeback=True)
    data = sanitize(data)
    zipcode = bottle.request.query.get('zipcode')
    command = bottle.request.query.get('command')
    if command == 'update':
        update(data, zipcode)
    if command == 'dump':
        return dump(data)
    #data.close()
    return index(data)

def index(data):
    tpl = bottle.template('status.tpl' , data=data )
    return tpl
  
def update(data, zipcode):
    if zipcode != None:
        data["config"]['zipcode'] = zipcode
    update_status(data)
    return

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

def dump(data):
    html = '<pre>'
    for key in data.keys():
        html += "<br>" + key + "=> "
        html+= pprint.pformat(data[key])
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

bottle.run(server='cgi')
