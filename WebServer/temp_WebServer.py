"""
***************************
File: temp_WebServer.py
***************************
Author: Kevin J Dolan
Project: Live Temp Monitor
Purpose: Bottle web server to manage loggin data from sensors to postgreSQL and
to output data to webpage when requested. 
***************************
Imports: 
 bottle: WebFramework
 psycopg2: PostgreSQL framework
 sys
 chartGen: Generates chart of temperature data and saves as PNG for webpage.
 **************************
"""
from bottle import route, run, template, get, post, request
import psycopg2
import sys
import tempChartGen

"""
GET: sensor1 and sensor2 
Store this data in postgeSQL database
"""
@get('/tempMonitor')
def logData():
    sensor1 = request.GET.get('sensor1')
    sensor2 = request.GET.get('sensor2')
    print(sensor1 + ' ' + sensor2)
    con = psycopg2.connect(database='tempStats', user='user')
    cur = con.cursor()
    SQL ='INSERT INTO templog (sensor1, sensor2) VALUES(' + sensor1 + ', ' + sensor2 + ');'
    print(SQL)
    cur.execute(SQL)
    con.commit()
    con.close()
@route('/liveTemp')
"""
Loads webpage with list of temperatures and chart of temperatures.
"""
def viewData():
    chartGen.genChart()
    try:
        con = psycopg2.connect(database='tempStats', user='user')
        cur = con.cursor()
        cur.execute('SELECT * FROM templog ORDER BY datetime DESC LIMIT 720')
        #ver = cur.fetchone()
        result = "<table><tr><td><b>"
        row = cur.fetchone()
        counter = 1
        while(row!=None):
            result +=  row[0].strftime("%m-%d-%y %H:%M:%S") + ': ' + str(row[1]) + ', ' + str(row[2]) + "<br>"
            if(counter == 1):
                result += "</b><br><br>"
            counter += 1
            row = cur.fetchone()
        result += '</td><td valign="top"><img src="http://media.kevinjdolan.com/LiveTemp/chart.png" valign="top" alt="chart"></td></tr></table>'
        return result
    except:
        print( 'Error %s')
        #sys.exit(1)
    finally:
        if con:
            con.close()



run(host='sever.host.com', port=8080)

