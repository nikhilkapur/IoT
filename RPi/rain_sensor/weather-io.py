#!/usr/bin/python
import urllib
import json
import datetime
import pprint
import math
import shelve
import time
from pprint import pprint

class RainSensor:
    def __init__(self, zip):
        (lat, lng) = self.zip2coord(zip)
        self.lat = lat
        self.lng = lng
        self.zip = zip
        pass
      
    def zip2coord (self) :
        'Convert a zip code to cordinates. Returns a (lat, long) tuple'
        
        fh = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%d" % (self.zip))
        url_data = fh.read()
        json_data = json.loads(url_data)
        lat = json_data["results"][0]["geometry"]["location"]["lat"]
        lng = json_data["results"][0]["geometry"]["location"]["lng"]
        self.lat = lat
        self.lng = lng
        return (lat, lng)
    
    def daily_weather (self, date):
        'Returns rain in inches for the gives coordinates and a date'
        
        date_formatted=date.strftime("%Y-%m-%dT%H:%M:%S")
        #fh = urllib.urlopen("http://api.wunderground.com/api/da389028587d3649/history_%s/q/CA/San_Jose.json" % (date_formatted))
        #print ("https://api.forecast.io/forecast/62f906de6ac7384fcf980197047d64f0/%s,%s,%s" % (lat,lng,date_formatted))
        fh = urllib.urlopen("https://api.forecast.io/forecast/62f906de6ac7384fcf980197047d64f0/%s,%s,%s" % (self.lat,self.lng,date_formatted))
        url_data = fh.read()
        json_data = json.loads(url_data)
        precip_per_hour = json_data["daily"]["data"][0]["precipIntensity"]
        temp_max = json_data["daily"]["data"][0]["temperatureMax"]
        try:
            pi = float(precip_per_hour) * 24
        except :
            pi = 0.0
        if pi == None:
            pi = 0.0
        return pi, temp_max
    
    def get_weather (self):
        'Get weather and temp for a few days. Returns a dict keyed by datetime dates'
        
        daily_stats = {}
        for i in range(-3, 3):
            day = datetime.datetime.today() + datetime.timedelta(days=i)
            daily_stats[day] = {}
            daily_stats[day]["precip"], daily_stats[day]["temp"] = daily_weather (day)
        return daily_stats
    
    def get_status(self, daily_stats, data):
        'Check if sensor should be on or off'
            
        data['details'] = {}
        sensor = "On"
        for i in sorted(daily_stats.iterkeys()):
            # get offset in days from today for this entry
            diff = datetime.datetime.today() - i
            diff_days = diff.days
            # Rain threshold is .1 inches for each incremental
            day_rain_threshold = abs(diff_days) * .1 + .1
            
            data['details'][i] = {}
            data['details'][i]['actual'] = daily_stats[i]["precip"]
            data['details'][i]['threshold'] = day_rain_threshold
            
            # Adjust Rain Threshold for temperature for that day ??? TBD
            if (daily_stats[i]["precip"] > day_rain_threshold):
                sensor = "Off"
                print i, daily_stats[i]["precip"] , day_rain_threshold, "Off"
                data['details'][i]['state'] = "Off"
            else:
                print i, daily_stats[i]["precip"] , day_rain_threshold, "On"
                data['details'][i]['state'] = "On"
        return sensor
    
    def print_history (self, ndays, lat, lng):
        total = 0.0
        for i in range(-2, ndays):
            day = datetime.datetime.today() - datetime.timedelta(days=i)
            rain, temp = daily_weather (lat, lng, day)
            day_formatted=day.strftime("%Y-%m-%dT%H:%M:%S")
            print day_formatted, "=>", rain
            total = total + rain
        return total
    

if __name__ == "__main__":        
    data = shelve.open('data.shelve', writeback=True)
    pprint(data)
    if data.has_key('config') and data['config'].has_key('zip'):
      zip = data['config']['zip']
    else:
      zip = 95138
      data['config'] = {
        'zip': zip
      }
    
    lat, lng = zip2coord (zip)
    
    #r = print_history(5, lat, lng)
    #print r
    daily_stats = get_weather (lat, lng)
    sensor = get_status(daily_stats, data)
    print sensor
    
    data['status'] = {
        'state': sensor,
        'error': '',
        'last_check': time.ctime()
    }

