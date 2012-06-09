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
        
def get_varianz(mittel,prognosen):
    """The function to predict."""
    Varianz = 0
    for z in prognosen:
        Varianz = Varianz + ((z-mittel)**2)
    Varianz = Varianz/len(prognosen)
    return Varianz


def plot_future(prognose_kurs, prognose_datum,color):
    
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)

def plot_own_forecast_points(predictions_mittel_dict,predictions_varianz_dict):
    color = 'green'    
    ax = fig.add_subplot(111)    
    for k in predictions_mittel_dict.keys():
        ax.plot_date(k, predictions_mittel_dict[k], 'o', color=color,linewidth=2)
        ax.hold(True)
        ax = fig.add_subplot(111)
        #ax.fill_between(k, predictions_mittel_dict[k] + 1.9600 * predictions_varianz_dict[k][1], predictions_mittel_dict[k] - 1.9600 * predictions_varianz_dict[k][1], alpha=0.35, linestyle='dashed' , color=color)
        ax.hold(True)
        ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #ax.fill_between(datum, prognosen + 1.9600 * std, prognosen - 1.9600 * std, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)

def plot_own_forecast_line(predictions, prognose_datum,sigma):
    color = 'green'
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, predictions, '-', color=color,linewidth=1)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    ax.fill_between(prognose_datum, predictions + 1.9600 * sigma, predictions - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)



def get_prediction_dictionary(analysten_dict):
    ################################################################################
    ### Die Schleife läuft jeden Analysten durch und ruft die methode zum zeichnen auf
    predictions_dict = {}
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
                if i[1] in predictions_dict:
                    predictions = svm.SVR.predict(clf,i[0])
                    predictions_dict[i[1]].append(predictions) 
                else:
                    predictions_dict[i[1]] = []
                    predictions = svm.SVR.predict(clf,i[0])
                    predictions_dict[i[1]].append(predictions)
            plot_future(prognose_kurs, prognose_datum,'yellow')
    return predictions_dict



def get_analysten_dict(ziel_kurse):
    analysten_dict ={}    
    for row in ziel_kurse:
        analysten_dict[row[2]] = []
    
    for row in ziel_kurse:  
        value = analysten_dict[row[2]]
        value.append([row[0],row[3] ,dates.date2num(row[1])])
    return analysten_dict
    

def get_analysten_prognosen_dict(prognose):
    analysten_prognosen_dict ={} 
    for row in prognose:
        analysten_prognosen_dict[row[2]] = []
    for row in prognose:  
        value = analysten_prognosen_dict[row[2]]
        value.append([row[0],dates.date2num(row[1])])
    return analysten_prognosen_dict
    
def get_predictions_and_dates(predictions_dict):
    global predictions_mittel_dict
    global predictions_varianz_dict
    predictions_and_dates_list = []
    for k in predictions_dict.keys():
        mittel = 0
        count = 0
        prognosen = []
        predictions_varianz_dict[k] = []
        for i in predictions_dict[k]:
            mittel=mittel+i[0]
            count = count +1
            prognosen.append(i[0])
        mittel = mittel/count
        Varianz = get_varianz(mittel,prognosen)
        predictions_mittel_dict[k] = mittel
        std = math.sqrt(Varianz)
        predictions_varianz_dict[k] = [Varianz,std]
        predictions_and_dates_list.append([k,mittel])
    predictions_and_dates_list.sort()
    return predictions_and_dates_list
    
def get_mittelwert(liste):
    mittelwert = 0
    count = 0 
    for z in liste:
        mittelwert = mittelwert+z[1]
        count = count +1
    mittelwert = mittelwert/count
    return mittelwert



cp=input("Für welches Unternehmen?\n")
sql2 = """SELECT avg, zieldatum FROM analyst_avg_2 WHERE unternehmen = %d  """%(cp)
sql3 = """SELECT neues_kursziel, zieldatum, analyst, avg FROM analyst_avg_2 WHERE unternehmen = %d AND neues_kursziel >0 AND avg_datum<(SELECT CURDATE()) ORDER BY avg_datum, zieldatum """%(cp)

sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d "%(cp)

sql4 = """SELECT neues_kursziel, zieldatum, analyst FROM prognose
 WHERE unternehmen = %d
 AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
 ORDER BY zieldatum"""%(cp)

predictions_mittel_dict = {}
predictions_varianz_dict={}
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



analysten_dict = get_analysten_dict(ziel_kurse)

analysten_prognosen_dict = get_analysten_prognosen_dict(prognose)



############################################# plot tatsächlichen kurs
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



predictions_dict = get_prediction_dictionary(analysten_dict)
predictions_and_dates_list = get_predictions_and_dates(predictions_dict)
mittelwert = get_mittelwert(predictions_and_dates_list)
Varianz = get_varianz(mittelwert,[q[1] for q in predictions_and_dates_list])
sigma = np.sqrt(Varianz)

print "standardabweichung: %s" %(str(sigma))

plot_own_forecast_line([q[1] for q in predictions_and_dates_list], [q[0] for q in predictions_and_dates_list],sigma) 
plot_own_forecast_points(predictions_mittel_dict,predictions_varianz_dict)   
    


ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.autoscale_view()    
ax.grid(True)
ax.legend(loc='upper left')
fig.autofmt_xdate()

show()
