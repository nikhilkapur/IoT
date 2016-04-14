#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
#!/usr/bin/python
import urllib
import json
import datetime
import shelve
import time
from pprint import pprint

class RainSensor:
    def __init__(self, zipcode, days_before=-3, days_after=3):
        self.zipcode = zipcode
        (lat, lng) = self.zip2coord(zipcode)
        self.lat = lat
        self.lng = lng
        self.days_before = days_before
        self.days_after = days_after
        pass
      
    def zip2coord (self, zipcode) :
        'Convert a zipcode code to cordinates. Returns a (lat, long) tuple'
        
        fh = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s" % (self.zipcode))
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
        for i in range(self.days_before, self.days_after):
            day = datetime.datetime.today() + datetime.timedelta(days=i)
            daily_stats[day] = {}
            daily_stats[day]["precip"], daily_stats[day]["temp"] = self.daily_weather (day)
        return daily_stats
    
    def get_status(self, daily_stats):
        'Check if sensor should be on or off'
            
        sensor = "On"
        for i in sorted(daily_stats.iterkeys()):
            # get offset in days from today for this entry
            diff = datetime.datetime.today() - i
            diff_days = diff.days

            # Rain threshold is .1 inches for each incremental
            daily_stats[i]['precip_threshold'] = abs(diff_days) * .1 + .1
            
            # Adjust Rain Threshold for temperature for that day ??? TBD
            if (daily_stats[i]["precip"] > daily_stats[i]['precip_threshold']):
                sensor = "Off"
                daily_stats[i]['state'] = "Off"
            else:
                daily_stats[i]['state'] = "On"
        return sensor
    
    def print_history (self, ndays, lat, lng):
        total = 0.0
        for i in range(-2, ndays):
            day = datetime.datetime.today() - datetime.timedelta(days=i)
            rain, temp = self.daily_weather (day)
            day_formatted=day.strftime("%Y-%m-%dT%H:%M:%S")
            print day_formatted, "=>", rain, temp
            total = total + rain
        return total
    

if __name__ == "__main__":        
    data = shelve.open('data.shelve', writeback=True)
    pprint(data)
    if data.has_key('config') and data['config'].has_key('zipcode'):
      zipcode = data['config']['zipcode']
    else:
      zipcode = 95138
      data['config'] = {
        'zipcode': zipcode
      }
    
    rs = RainSensor(zipcode)
    daily_stats = rs.get_weather ()
    sensor = rs.get_status(daily_stats)
    print sensor
    pprint (daily_stats)
    data['daily_stats'] = daily_stats
    data['status'] = {
        'state': sensor,
        'last_check': time.ctime(),
        'error': 'foobar'
        }
    pprint (data)

#                 print i, daily_stats[i]["precip"] , daily_stats[i]['precip_threshold'], "Off"
#     
#     data['status'] = {
#         'state': sensor,
#         'error': '',
#         'last_check': time.ctime()
#     }

