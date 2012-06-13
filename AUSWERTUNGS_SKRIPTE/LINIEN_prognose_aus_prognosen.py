# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import math
import h5py as h5
from sklearn import *
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
        



def plot_future_unbekannt(prognose_kurs, prognose_datum,color):
    
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)
    


################################################################################    
def plot_future(prognose_kurs, prognose_datum,color):
    
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)
    
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
    print sigma
    print len(kurse)
    ax.fill_between(daten, kurse + 1.9600 * sigma, kurse - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)
    ax.hold(True)
    return [color,sigma]


def plot_prediction(predictions, prognose_datum,color):
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, predictions, '-', color=color,linewidth=1)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)
   
def plot_mittel(prognose_datum,last_kurs,color,label):
    trend = []
    for i in range(0,len(prognose_datum)):
        trend.append(last_kurs)
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, trend, '--', color=color,linewidth=4,label=label)
    ax.hold(True)
    ax = fig.add_subplot(111)
    
    
cp=input("Für welches Unternehmen?\n")
sql2 = """SELECT avg, zieldatum FROM analyst_avg_2 WHERE unternehmen = %d  """%(cp)
sql3 = """SELECT neues_kursziel, zieldatum, analyst, avg FROM analyst_avg_2 WHERE unternehmen = %d  AND avg_datum<(SELECT CURDATE()) ORDER BY avg_datum, zieldatum """%(cp)

sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d ORDER BY `datum`"%(cp)

sql4 = """SELECT neues_kursziel, zieldatum, analyst FROM prognose
 WHERE unternehmen = %d
 AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
 ORDER BY zieldatum"""%(cp)


c = 100.
eps = 0.5


avg_kurse = get_select(sql)
ziel_kurse = get_select(sql3)
prognose = get_select(sql4)

avg = [q[0] for q in avg_kurse]

datum_avg = [q[1] for q in avg_kurse]
datum_avg =dates.date2num(datum_avg)

datum_ziel = [q[1] for q in ziel_kurse]
datum_ziel =dates.date2num(datum_ziel)

datum_prognose = [q[1] for q in prognose]
datum_prognose = dates.date2num(datum_prognose)

analysten_list = [q[2] for q in ziel_kurse]
#avg_2 = [q[3] for q in ziel_kurse]



analysten_dict ={}

for row in ziel_kurse:
    analysten_dict[row[2]] = []
    
for row in ziel_kurse:  
    value = analysten_dict[row[2]]
    value.append([row[0],row[3] ,dates.date2num(row[1])])

analysten_prognosen_dict ={} 

for row in prognose:
    analysten_prognosen_dict[row[2]] = []
for row in prognose:  
    value = analysten_prognosen_dict[row[2]]
    value.append([row[0],dates.date2num(row[1])])
    
#date1 = datetime.date( 2006, 1, 31 )
#date2 = datetime.date( 2012, 5, 21 )

months    = MonthLocator(range(1,13),interval = 3)
monthsFmt = DateFormatter("%b '%y")


fig = figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.hold(True)
ax = fig.add_subplot(111)
ax.plot_date(datum_avg, avg,'-',color='black',label='tats. Kurs',linewidth=2)
ax.hold(True)
################################################################################
### Die Schleife läuft jeden Analysten durch und ruft die methode zum zeichnen auf
preds = []
for k,v in analysten_dict.iteritems():
    kurse = [q[0] for q in v]
    avgs = [q[1] for q in v]
    daten = [q[2] for q in v]
    training_prognosen = np.array(kurse)
    training_prognosen=np.resize(training_prognosen,(len(training_prognosen),1))
    training_tats_kurse = np.array(avgs)
    ################################# SVR mit Parametern belegen und antrainieren
    clf = svm.SVR(C=c, epsilon=eps,kernel='rbf')
    clf = svm.SVR.fit(clf,training_prognosen,training_tats_kurse)

    if k in analysten_prognosen_dict.keys():    
        val = analysten_prognosen_dict[k]
        prognose_kurs=[] 
        prognose_datum = []
        for i in val:
            prognose_kurs.append(i[0])
            prognose_datum.append(i[1])
        color ='#%02X%02X%02X' % (randrange(0, 255), randrange(0, 255),randrange(0, 255))
        prognose_kurs=np.array(prognose_kurs)
        prognose_kurs=np.resize(prognose_kurs,(len(prognose_kurs),1))
        predictions = svm.SVR.predict(clf,prognose_kurs)
        plot_prediction(predictions, prognose_datum,color)
        #plot_future(prognose_kurs, prognose_datum,color)
        preds.append(predictions)


mittel_pred = 0
mittel_count = 0
maxi=[]
mini=[]

for i in preds:
    maxi.append(max(i))
    mini.append(min(i))
    for z in i:
        mittel_pred = mittel_pred+z
        mittel_count = mittel_count+1

mittel_pred = mittel_pred/mittel_count
plot_mittel(datum_prognose,mittel_pred,'#7B3F00','mittel_prognosen')

t = 'Mittel Prognose: %s (%s prozentiger Anstieg)' %(str(mittel_pred),str(((mittel_pred-avg[-1])/avg[-1])*100))
print t
print


maximum = max(maxi)
plot_mittel(datum_prognose,maximum,'#76EE00','maximum')
minimum = min (mini)
plot_mittel(datum_prognose,minimum,'#FF0000','minimum')
t = 'Maximum: %s (%s prozentiger Anstieg)' %(str(maximum),str(((maximum-avg[-1])/avg[-1])*100))
print t
print
t = 'Minimum: %s (%s prozentiger Anstieg)' %(str(minimum),str(((minimum-avg[-1])/avg[-1])*100))
print t




#maximum_mittel = 0
#max_count = 0
#minimum_mittel = 0
#min_count = 0
#
#for i in maxi:
#    maximum_mittel= maximum_mittel+i
#    max_count = max_count+1
#for i in mini:
#    minimum_mittel = minimum_mittel+i
#    min_count = min_count +1
#
#maximum_mittel = maximum_mittel/max_count
#minimum_mittel = minimum_mittel/min_count

#t = 'Mittel Max: %s (%s prozentiger Anstieg)' %(str(maximum_mittel),str(((maximum_mittel-avg[-1])/avg[-1])*100))
#print t
#print
#t = 'Mittel Min: %s (%s prozentiger Anstieg)' %(str(minimum_mittel),str(((minimum_mittel-avg[-1])/avg[-1])*100))
#print t






#for k in analysten_prognosen_dict.keys():
#    if k not in analysten_dict.keys():
#        val = analysten_prognosen_dict[k]
#        prognose_kurs=[] 
#        prognose_datum = []
#        color ='#%02X%02X%02X' % (randrange(0, 255), randrange(0, 255),randrange(0, 255))
#        #sigma_prog = []
#        for i in val:
#            
#            prognose_kurs.append(i[0])
#            prognose_datum.append(i[1])
#         #   sigma_prog.append(1.)
#        #print sigma_prog
#        plot_future_unbekannt(prognose_kurs, prognose_datum,color)
    
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.autoscale_view()    
ax.grid(True)
ax.legend(loc='upper left')
fig.autofmt_xdate()

show()
