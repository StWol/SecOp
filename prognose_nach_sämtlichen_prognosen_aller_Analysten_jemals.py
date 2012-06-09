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

def get_varianz(mittel,prognosen):
    """The function to predict."""
    Varianz = 0
    for z in prognosen:
        Varianz = Varianz + ((z-mittel)**2)
    Varianz = Varianz/len(prognosen)
    return Varianz
    

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

def plot_endlich(predictions, prognose_datum,sigma,color):
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, predictions, '-', color=color,linewidth=1)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    ax.fill_between(prognose_datum, predictions + 1.9600 * sigma, predictions - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)

def get_sigma(new_kurs,avg):
    """The function to predict."""
    MSE = 0
    l = len(new_kurs)
    for z,j in zip(new_kurs,avg):
        MSE = MSE + ((z-j)**2)
    MSE = MSE/l
    return np.sqrt(MSE)

cp=input("Für welches Unternehmen?\n")
sql2 = """SELECT avg, zieldatum FROM analyst_avg_2 WHERE unternehmen = %d  """%(cp)
sql_training = """SELECT neues_kursziel, zieldatum,avg FROM analyst_avg_2 WHERE unternehmen = %d AND avg_datum<'2012-03-01'"""%(cp)
sql_testing = """SELECT neues_kursziel, zieldatum, analyst, avg FROM analyst_avg_2 WHERE unternehmen = %d  AND avg_datum>'2012-03-01' AND avg_datum<(SELECT CURDATE())"""%(cp)
sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d "%(cp)

sql_prognose = """SELECT neues_kursziel, zieldatum FROM prognose
 WHERE unternehmen = %d
 AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
 """%(cp)


months    = MonthLocator(range(1,13),interval = 3)
monthsFmt = DateFormatter("%b '%y")
fig = figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
c = 100.
eps = 0.5

avg_kurse = get_select(sql)
kurse_training = get_select(sql_training)
kurse_testing = get_select(sql_testing)
prognose = get_select(sql_prognose)

avg = [q[0] for q in avg_kurse]

datum_avg = [q[1] for q in avg_kurse]
datum_avg =dates.date2num(datum_avg)
datum_kurse_training=[]
tats_kurs_training=[]
prognose_training=[]
training_predictions_and_dates_list = []
testing_predictions_and_dates_list = []
forecast_predictions_and_dates_list = []
for i in kurse_training:
    training_predictions_and_dates_list.append([dates.date2num(i[1]),i[2],i[0]])

training_predictions_and_dates_list.sort()


trainya = np.array([q[2] for q in training_predictions_and_dates_list])
trainya=np.resize(trainya,(len(trainya),1))
training_tats_kurse = np.array([q[1] for q in training_predictions_and_dates_list])
################################# SVR mit Parametern belegen und antrainieren
clf = svm.SVR(C=c, epsilon=eps,kernel='rbf')
clf = svm.SVR.fit(clf,trainya,training_tats_kurse)


for i in kurse_testing:
    testing_predictions_and_dates_list.append([dates.date2num(i[1]),i[3],i[0]])

testing_predictions_and_dates_list.sort()



testinya = np.array([q[2] for q in testing_predictions_and_dates_list])
testinya=np.resize(testinya,(len(testinya),1))
################################# predict training and testing
consistency = svm.SVR.predict(clf,trainya )
testing_check = svm.SVR.predict(clf,testinya)


sigma_training = get_sigma(consistency,[q[1] for q in training_predictions_and_dates_list])
print sigma_training
plot_endlich(consistency, [q[0] for q in training_predictions_and_dates_list],sigma_training,'green') 


sigma_testing = get_sigma(testing_check,[q[1] for q in testing_predictions_and_dates_list])
print sigma_testing
plot_endlich(testing_check, [q[0] for q in testing_predictions_and_dates_list],sigma_testing,'orange')


################################# predict training and testing

for i in prognose:
    forecast_predictions_and_dates_list.append([dates.date2num(i[1]),i[0]])

forecast_predictions_and_dates_list.sort()

prognose_kurs=np.array(forecast_predictions_and_dates_list)
prognose_kurs=np.resize(prognose_kurs,(len(prognose_kurs),1))
predictions = svm.SVR.predict(clf,prognose_kurs)

mittelwert_prog = 0
count_prog = 0 
for z in predictions:
    mittelwert_prog = mittelwert_prog+z
    count_prog = count_prog +1
mittelwert_prog = mittelwert_prog/count_prog
Varianz_prog = get_varianz(mittelwert_prog,[q[1] for q in forecast_predictions_and_dates_list])
sigma_prog = np.sqrt(Varianz_prog)
print sigma_prog
plot_endlich(predictions, [q[0] for q in forecast_predictions_and_dates_list],sigma_prog,'red')




#plotting


ax.hold(True)
ax = fig.add_subplot(111)
ax.plot_date(datum_avg, avg,'-',color='black',label='tats. Kurs',linewidth=2)
ax.hold(True)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.autoscale_view()    
ax.grid(True)
ax.legend(loc='upper left')
#fig.autofmt_xdate()

show()
