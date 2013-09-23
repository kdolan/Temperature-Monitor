"""
***************************
File: temp_ChartGen.py
***************************
Author: Kevin J Dolan
Project: Live Temp Monitor
Purpose: Generate chart based on data from postgreSQL.
***************************
Imports:
 psycopg2: PostgreSQL framework
 matplotlib: Generates and saves chart.
***************************
"""
import psycopg2
from matplotlib import pyplot as plot, dates

"""
Generates chart based on data from postgeSQL database.
Size of query determiens the how many points will be plotted
on the chart.
"""
def genChart(limit = 1400):
    conn = psycopg2.connect('dbname=tempStats user=user')
    cur = conn.cursor()
    if(limit == 0):
        cur.execute('SELECT * FROM templog ORDER BY datetime DESC')
    else:
        cur.execute('SELECT * FROM templog ORDER BY datetime DESC LIMIT ' + str(limit))
    data = cur.fetchall()
    cur.close()
    conn.close()

    fig, ax = plot.subplots(1)
    fig.autofmt_xdate()
    ax.fmt_xdata = dates.DateFormatter('%H:%M')

    dt, sensor1, sensor2 = zip(*data)
    dt = dates.date2num(dt)
    plot.plot_date(dt, sensor1, linewidth=2.0)
    plot.savefig("temp.png")

