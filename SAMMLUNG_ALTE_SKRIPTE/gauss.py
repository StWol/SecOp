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
from matplotlib import pyplot as plt
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

sql = "SELECT AVG( close ) , `datum` FROM kursdaten WHERE analyst =1661  GROUP BY YEAR( `datum` ) , MONTH( `datum` )"
sql1 = """SELECT `neues_kursziel`,  `zieldatum`
    FROM `prognose`, `analyst`, `analystenhaus`
    WHERE `zeithorizont`>0 AND `neues_kursziel`>0 AND `analyst` =1661 AND `analyst` = `analyst`.`id` AND `analyst`.`analystenhaus`=`analystenhaus`.`id`"""
sql2 = """SELECT avg,datum,neues_kursziel FROM analyst_avg WHERE unternehmen = 1 ORDER BY datum """



avg_nk = get_select(sql2)
avg = [q[0] for q in avg_nk]
print avg
new_kurs = [q[2] for q in avg_nk]
print new_kurs
datum_ziel = [q[1] for q in avg_nk]
datum_ziel =dates.date2num(datum_ziel)
print datum_ziel
months    = MonthLocator(range(1,13))
monthsFmt = DateFormatter("%b '%y")


#quotes = quotes_historical_yahoo('INTC', date1, date2)
#quotes = get_select(sql)
#
#if len(quotes) == 0:
#    print 'Found no quotes'
#    raise SystemExit
#
#datesss = [q[1] for q in quotes]
#opens = [q[0] for q in quotes]




#kurse = get_select(sql1)
#n_k = [q[0] for q in kurse]
#date1 = [q[1] for q in kurse]

#datesss = dates.date2num(datesss)
#print opens
#print datesss

MSE = 0
l = len(datum_ziel)
print l
for z,j in zip(new_kurs,avg):
    MSE = MSE + ((z-j)**2)
MSE = MSE/l
print MSE
sigma = np.sqrt(MSE)
#
#fig = figure()
#ax = fig.add_subplot(111)
#ax.plot_date(datum_ziel, avg, '-')
#ax.hold(True)
#ax = fig.add_subplot(111)
#ax.plot_date(datum_ziel, new_kurs, 'o')
#ax.fill(np.concatenate([avg, avg[::-1]]), \
#    np.concatenate([new_kurs + 1.9600 * sigma,
#                    (new_kurs - 1.9600 * sigma)[::-1]]), \
#    alpha=.5, fc='b', ec='None', label='95% confidence interval')
#ax.xaxis.set_major_locator(months)
#ax.xaxis.set_major_formatter(monthsFmt)
##ax.xaxis.set_minor_locator(mondays)
#ax.autoscale_view()
##ax.xaxis.grid(False, 'major')
##ax.xaxis.grid(True, 'minor')
#ax.grid(True)
#
#fig.autofmt_xdate()
#
#show()
ui = range (len(avg))

plt.plot(ui,avg, 'b-', markersize=10, label=u'tatsaechlicher kurs')
plt.plot(ui,new_kurs, 'r.', label=u'Vorhersage')
plt.fill(np.concatenate([ui, ui[::-1]]), \
    np.concatenate([new_kurs + 1.9600 * sigma,
                    (new_kurs - 1.9600 * sigma)[::-1]]), \
    alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('zeit')
plt.ylabel('preis')
plt.grid(True)
#pl.ylim(-10, 20)
#plt.legend(loc='upper left')
#pl.title("GP with quadratic mean and trained hyperparameters (Scikits)")
plt.show()


# every monday
