import ephem

sj = ephem.Observer()

#Location of San Jose, CA
sj.lat  = str(37.279518)   #Note that lat/lon should be in string format
sj.lon  = str(-121.867905)

# Get sunset
sunset = sj.next_setting(ephem.Sun())
# Convert to local datetime object
ss = ephem.localtime(sunset)
print ss