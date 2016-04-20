#!/usr/bin/python

import fusionCharts
import MySQLdb
import cgi
from pprint import pprint
#import salt_monitor
import os

MAX  = 70                              # Max distance i.e. lowest salt level. % is calculated based on this
WARN = 15                              # Level below which notifications start (%)

def create_chart(data):
    chart = fusionCharts.fusionChart (chart_type = 'multi_stacked_area',
                                      width = 800, height = 450)
    # Let fusionchart decide color instead of the list in our library
    chart.color_array = []
 
    # Keep only about 10 x-axis labels
    labelstep = len(data) /10
    if labelstep < 1:
        labelstep = 1

    chart.setChartTagAttributes ( {
            'caption': 'Water Softener Salt Level',
            'yAxisName': 'Level (%)',
            'yAxisMaxValue': 100,
            'numberSuffix': '%',
            'decimals': 1,
            'labelStep': labelstep
    })
    chart.addDataSeries('Salt Level', data,
                        series_attributes= { 'renderAs' : 'column', 'showValues' : '0', 'alpha': 70},
                        )
    hline = { 'Warning': 
                  {'startValue':WARN, 'color':'fbaa01', 'thickness':2, 'alpha': 100}
            }
    chart.addHlines(hline)
    #html = chart.getHTMLheader()
    html = chart.getHTML('chart_div_name')
    return html

def get_data(ndays):
    data = {}
    db = MySQLdb.connect(host="localhost", user="salt_monitor", passwd="salt_monitor123", db="salt_monitor")
    cur = db.cursor()
    cur.execute('''SELECT sl_level, sl_date FROM salt_level 
                   WHERE sl_date > (DATE_SUB(CURDATE(), INTERVAL %s DAY))
                ''', (ndays,))
    for row in cur.fetchall():
        day = row[1]
        #date = "%d-%02d-%02d %02d:%02d:%02d" % (day.year, day.month, day.day, day.hour, day.minute, day.second)
        date = "%d-%02d-%02d %02d:%02d" % (day.year, day.month, day.day, day.hour, day.minute)
        data[date] = row[0]
    return data

def sanitize_chart_data(data):
    new_data = {}
    prev_level = None
    for date, level in sorted(data.items()):
        if prev_level != None and abs(prev_level-level)*1.0/level > 0.1 :
            #print '<pre>Skipping:', date, level, prev_level, abs(prev_level-level)*1.0/level
            prev_level = level
            continue
        # Convert to percentage
        new_data[date] = (MAX - level) *100.0 / MAX 
        prev_level = level

    return new_data

def raw_data_html(data):
    html = "<table border=1>"
    for date, level in sorted(data.items()):
        html += '''<tr><td>%s</td>
                       <td>%d</td>
                   </tr>''' % (date, level)
    html += '</html>'
    return html

def update_data():
    os.system("./wrapper > /dev/null")

def get_form(ndays, show_raw, update_now):
    if show_raw == 1:
        show_raw_chk = 'checked'
    else:
        show_raw_chk = ''
    if update_now == 1:
        update_now_chk = 'checked'
    else:
        update_now_chk = ''

    form = ''' <form method=GET action='%s'>
               <label>Days:<input type=text name=days value=%s size=4></label>
               <label>Show Numbers<input type=checkbox name=show_raw value=1 %s></label>
               <label>Update Now<input type=checkbox name=update_now value=1 %s></label>
               <input type=Submit Value='Update'>
               </form>
           ''' % (os.environ['SCRIPT_NAME'], ndays, show_raw_chk, update_now_chk)
    return form

if __name__ == "__main__":
    print "Content-type: text/html\n\n"
    print "<script type=text/JavaScript src=/fusioncharts/js/fusioncharts.js></script>"
    print "<html>"
    form = cgi.FieldStorage()
    ndays = form.getfirst('days', 7)
    update_now = int(form.getfirst('update_now', 0))
    show_raw = int(form.getfirst('show_raw', 0))

    if update_now == 1:
        update_data()

    data = get_data(ndays)
    data_chart = sanitize_chart_data(data)
    print create_chart(data_chart)
    print get_form(ndays, show_raw, update_now)
    if show_raw == 1:
        print raw_data_html(data)
    #print "<pre>"
    #pprint (data)
    print "</html>"

