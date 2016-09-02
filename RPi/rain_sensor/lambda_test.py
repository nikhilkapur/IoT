import json
import urllib
import urllib2

url = "https://x1z8egdmi2.execute-api.us-east-1.amazonaws.com/prod/zip2coord"
values = {'zipcode' : 95133}

req = urllib2.Request(url, json.dumps(values), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
response = urllib2.urlopen(req)
the_page = response.read()
print the_page