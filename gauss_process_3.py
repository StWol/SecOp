# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import datetime
import MySQLdb
import numpy as np
from pylab import figure, show
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib import dates
from random import randrange

try:
    conn = MySQLdb.connect (host="141.62.65.151",
                            user = "stan",
                            passwd = "money!",
                            db = "secop")
                      
    print "Mit secop verbunden"
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])

    
cursor = conn.cursor ()


################################################################################
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
        
################################################################################        
def get_sigma(new_kurs,avg,datum_list):
    """The function to predict."""
    MSE = 0
    l = len(datum_list)
    for z,j in zip(new_kurs,avg):
        MSE = MSE + ((z-j)**2)
    MSE = MSE/l
    return np.sqrt(MSE)
    
    
################################################################################    
def plot_analyst(kurse, avg, daten):
    
    color ='#%02X%02X%02X' % (randrange(0, 255), randrange(0, 255),randrange(0, 255))
     
    ax = fig.add_subplot(111)
    ax.plot_date(daten, kurse, 'o-', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    sigma = get_sigma(kurse,avg,daten)
    ax.fill_between(daten, kurse + 1.9600 * sigma, kurse - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)
    
   
   
   
sql2 = """SELECT avg, datum FROM analyst_avg_2 WHERE unternehmen = 1  AND `datum`> '2009-01-01' AND `datum`<(SELECT CURDATE()) ORDER BY datum """
sql3 = """SELECT neues_kursziel, zieldatum, analyst, avg FROM analyst_avg_2 WHERE analyst in (779,373, 1661,2125) AND unternehmen = 1  AND `datum`> '2009-01-01' AND `datum`<(SELECT CURDATE()) ORDER BY datum, zieldatum """


avg_kurse = get_select(sql2)
ziel_kurse = get_select(sql3)

avg = [q[0] for q in avg_kurse]

datum_avg = [q[1] for q in avg_kurse]
datum_avg =dates.date2num(datum_avg)


datum_ziel = [q[1] for q in ziel_kurse]
datum_ziel =dates.date2num(datum_ziel)

analysten_list = [q[2] for q in ziel_kurse]
avg_2 = [q[3] for q in ziel_kurse]


analysten_dict ={}

for row in ziel_kurse:
    analysten_dict[row[2]] = []
    
for row in ziel_kurse:  
    value = analysten_dict[row[2]]
    value.append([row[0],row[3] ,dates.date2num(row[1])])
    
 
    
date1 = datetime.date( 2006, 1, 31 )
date2 = datetime.date( 2012, 5, 21 )

months    = MonthLocator(range(1,13))
monthsFmt = DateFormatter("%b '%y")


fig = figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)


################################################################################
### Die Schleife läuft jeden Analysten durch und ruft die methode zum zeichnen auf
for k,v in analysten_dict.iteritems():
    kurse = [q[0] for q in v]
    avgs = [q[1] for q in v]
    daten = [q[2] for q in v]
    
    plot_analyst(kurse, avgs, daten)
    
    
ax.hold(True)
ax = fig.add_subplot(111)
ax.plot_date(datum_avg, avg, 'o-')
ax.autoscale_view()    
ax.grid(True)

fig.autofmt_xdate()

show()
