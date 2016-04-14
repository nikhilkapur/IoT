#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import fusionCharts
import MySQLdb
from pprint import pprint

def create_chart(data):
    chart = fusionCharts.fusionChart (chart_type = 'multi_stacked_area',
                                      width = 800, height = 450)
    # Let fusionchart decide color instead of the list in our library
    chart.color_array = []
    chart.setChartTagAttributes ( {
            'caption': 'Water Softener Salt Level',
            'yAxisName': 'Amount'})
    chart.addDataSeries('Salt Level', data,
                        series_attributes= { 'renderAs' : 'area', 'showValues' : '0'},
                        )
    html = chart.getHTMLheader()
    html += chart.getHTML('chart_div_name')
    return html

def get_data():
    data = {}
    db = MySQLdb.connect(host="localhost", user="root", passwd="nkapur", db="salt_monitor")
    cur = db.cursor()
    cur.execute("SELECT sl_level, sl_date FROM salt_level")
    for row in cur.fetchall():
        day = row[1]
        date = "%d-%02d-%02d %02d:%02d" % (day.year, day.month, day.day, day.hour, day.second)
        data[date] = row[0]
    return data

if __name__ == "__main__":
    print "Content-type: text/html\n\n"
    print "<html>"
    data = get_data()
    print create_chart(data)
    print "</html>"

