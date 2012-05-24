# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import datetime
import MySQLdb
import numpy as np
from pylab import figure, show
from matplotlib.dates import MONDAY, SATURDAY
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib import dates

try:
    conn = MySQLdb.connect (host="141.62.65.151",
                            user = "stan",
                            passwd = "money!",
                            db = "secop")
                      
    print "Mit secop verbunden"
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])

    
cursor = conn.cursor ()



def get_select(sql):
    result = []
    try:
        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchall()
        result = np.array(result)
        #result = np.transpose(result)
        return result
        
    except MySQLdb.Error, e:
        conn.rollback()
        print "Error %d: %s" % (e.args[0], e.args[1])

sql1 = """SELECT avg, datum FROM analyst_avg WHERE unternehmen = 1 ORDER BY datum"""
sql2 = """SELECT analyst, avg, datum FROM analyst_avg_2 WHERE unternehmen = 1  AND `datum`> '2009-01-01' AND `datum`<(SELECT CURDATE()) ORDER BY datum """
sql3 = """SELECT neues_kursziel, zieldatum FROM analyst_avg_2 WHERE unternehmen = 1  AND `datum`> '2009-01-01' AND `datum`<(SELECT CURDATE()) ORDER BY zieldatum """


avg_kurse = get_select(sql2)
ziel_kurse = get_select(sql3)

analysten_keys = [q[0] for q in avg_kurse]

avg = [q[1] for q in avg_kurse]

datum_avg = [q[2] for q in avg_kurse]
datum_avg =dates.date2num(datum_avg)

new_kurs = [q[0] for q in ziel_kurse]



datum_ziel = [q[1] for q in ziel_kurse]
datum_ziel =dates.date2num(datum_ziel)
#print avg
date1 = datetime.date( 2006, 1, 31 )
date2 = datetime.date( 2012, 5, 21 )


MSE = 0
l = len(datum_avg)

for z,j in zip(new_kurs,avg):
    MSE = MSE + ((z-j)**2)
    
MSE = MSE/l


sigma = np.sqrt(MSE)
# every monday


# every 3rd month
months    = MonthLocator(range(1,13))
monthsFmt = DateFormatter("%b '%y")



#quotes = quotes_historical_yahoo('INTC', date1, date2)

fig = figure()
ax = fig.add_subplot(111)
ax.hold(True)
ax = fig.add_subplot(111)
ax.plot_date(datum_ziel, new_kurs, 'go')
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)

ax.hold(True)
ax = fig.add_subplot(111)
#ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
#ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
ax.fill_between(datum_ziel, new_kurs + 1.9600 * sigma, new_kurs - 1.9600 * sigma, alpha=.5, linestyle='dashed', edgecolor="blue" )
ax.hold(True)
ax = fig.add_subplot(111)
ax.plot_date(datum_avg, avg, 'o-')
#ax.xaxis.set_minor_locator(mondays)
ax.autoscale_view()
#ax.xaxis.grid(False, 'major')
#ax.xaxis.grid(True, 'minor')
ax.grid(True)

fig.autofmt_xdate()

show()


# every monday