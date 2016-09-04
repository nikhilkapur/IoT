#!/usr/bin/python

import fusionCharts
import MySQLdb
import cgi
import os
import ConfigParser

def create_chart(data, div_id='chart_div_id'):
    chart = fusionCharts.fusionChart (chart_type = 'multi_stacked_area',
                                      width = 800, height = 450)
    # Let fusionchart decide color instead of the list in our library
    chart.color_array = []
 
    # Keep only about 10 x-axis labels
    labelstep = len(data) /10
    if labelstep < 1:
        labelstep = 1

    chart.setChartTagAttributes ( {
            'caption': 'Temp History',
            #'yAxisName': 'Temp',
            #'yAxisMaxValue': 100,
            #'numberSuffix': '%',
            #'decimals': 1,
            'labelStep': labelstep
    })
    chart.addDataSeries('Temperature', data,
                        series_attributes= { 'renderAs' : 'column', 'showValues' : '0', 'alpha': 70},
                        )
    html = chart.getHTML(div_id)
    return html

def get_data(ndays, config):
    data = {}

    db_host = config.get('database', 'db_host')
    db_name = config.get('database', 'db_name')
    db_user = config.get('database', 'db_user')
    db_password = config.get('database', 'db_password')
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
    
    cur = db.cursor()
    cur.execute('''SELECT temperature, time FROM temperatures 
                   WHERE time > (DATE_SUB(CURDATE(), INTERVAL %s DAY))
                ''', (ndays,))
    for row in cur.fetchall():
        day = row[1]
        #date = "%d-%02d-%02d %02d:%02d:%02d" % (day.year, day.month, day.day, day.hour, day.minute, day.second)
        date = "%d-%02d-%02d %02d:%02d" % (day.year, day.month, day.day, day.hour, day.minute)
        data[date] = row[0]
    return data

def raw_data_html(data):
    html = "<table border=1>"
    for date, temperature in sorted(data.items()):
        html += '''<tr><td>%s</td>
                       <td>%.2f</td>
                   </tr>''' % (date, temperature)
    html += '</html>'
    return html

def get_form(ndays, show_raw):
    if show_raw == 1:
        show_raw_chk = 'checked'
    else:
        show_raw_chk = ''

    form = ''' <form method=GET action='%s'>
               <label>Days:<input type=text name=days value=%s size=4></label>
               <label>Show Numbers<input type=checkbox name=show_raw value=1 %s></label>
               <input type=Submit Value='Update'>
               </form>
           ''' % (os.environ['SCRIPT_NAME'], ndays, show_raw_chk)
    return form

if __name__ == "__main__":
    print "Content-type: text/html\n\n"
    print "<script type=text/JavaScript src=/fusioncharts/js/fusioncharts.js></script>"
    print "<html>"
    form = cgi.FieldStorage()
    ndays = form.getfirst('days', 2)
    show_raw = int(form.getfirst('show_raw', 0))

    config = ConfigParser.ConfigParser()
    config.read('temp.cfg')

    data = get_data(ndays, config)
    print create_chart(data)
    print get_form(ndays, show_raw)
    if show_raw == 1:
        print raw_data_html(data)
    #print "<pre>"
    #pprint (data)
    print "</html>"

