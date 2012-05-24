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

sql = "SELECT AVG( close ) , `datum` FROM kursdaten WHERE unternehmen =1  GROUP BY YEAR( `datum` ) , MONTH( `datum` )"
sql1 = """SELECT `neues_kursziel`,  `zieldatum`
    FROM `prognose`, `analyst`, `analystenhaus`
    WHERE `zeithorizont`>0 AND `neues_kursziel`>0 AND `unternehmen` =1 AND `analyst` = `analyst`.`id` AND `analyst`.`analystenhaus`=`analystenhaus`.`id`"""
sql2 = """SELECT avg,datum FROM unternehmen_avg WHERE unternehmen = 1 ORDER BY datum"""

date1 = datetime.date( 2006, 1, 31 )
date2 = datetime.date( 2012, 5, 21 )

# every monday


# every 3rd month
months    = MonthLocator(range(1,13))
monthsFmt = DateFormatter("%b '%y")


#quotes = quotes_historical_yahoo('INTC', date1, date2)
quotes = get_select(sql)

if len(quotes) == 0:
    print 'Found no quotes'
    raise SystemExit

datesss = [q[1] for q in quotes]
opens = [q[0] for q in quotes]

kurse = get_select(sql1)



n_k = [q[0] for q in kurse]
date1 = [q[1] for q in kurse]

datesss = dates.date2num(datesss)
print opens
print datesss

fig = figure()
ax = fig.add_subplot(111)
ax.plot_date(datesss, opens, '-')
ax.hold(True)
ax = fig.add_subplot(111)
ax.plot_date(date1, n_k, 'o')
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
#ax.xaxis.set_minor_locator(mondays)
ax.autoscale_view()
#ax.xaxis.grid(False, 'major')
#ax.xaxis.grid(True, 'minor')
ax.grid(True)

fig.autofmt_xdate()

show()