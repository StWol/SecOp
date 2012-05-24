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
from sklearn.gaussian_process import GaussianProcess
from matplotlib import pyplot as pl
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
        
        
def get_MSE(new_kurs,avg):
    """The function to predict."""
    MSE = 0
    l = len(datum_ziel)
    print l
    for z,j in zip(new_kurs,avg):
        MSE = MSE + ((z-j)**2)
    MSE = MSE/l
    return MSE

        


sql = "SELECT AVG( close ) , `datum` FROM kursdaten WHERE analyst =1661  GROUP BY YEAR( `datum` ) , MONTH( `datum` )"
sql1 = """SELECT `neues_kursziel`,  `zieldatum`
    FROM `prognose`, `analyst`, `analystenhaus`
    WHERE `zeithorizont`>0 AND `neues_kursziel`>0 AND `analyst` =1661 AND `analyst` = `analyst`.`id` AND `analyst`.`analystenhaus`=`analystenhaus`.`id`"""

#sql2 = """SELECT avg,datum,neues_kursziel,analyst FROM analyst_avg_2 WHERE unternehmen = 1 ORDER BY datum """
sql2 = """SELECT avg,datum,neues_kursziel,analyst FROM analyst_avg_2
         WHERE unternehmen = 1 AND analyst = 779 AND `datum`> '2009-01-01' AND `datum`<(SELECT CURDATE())"""
sql_prog = """SELECT zieldatum,neues_kursziel,analyst FROM prognose
         WHERE unternehmen = 1 AND `zieldatum`>(SELECT CURDATE())"""
"""AND analyst = 779 """

avg_nk = get_select(sql2)
avg = [q[0] for q in avg_nk]
new_kurs = [q[2] for q in avg_nk]
datum_ziel = [q[1] for q in avg_nk]
datum_ziel =dates.date2num(datum_ziel)
analyst = [q[3] for q in avg_nk]
ana_prog = [[q[2] for q in avg_nk],[q[3] for q in avg_nk]]
#print ana_prog
months    = MonthLocator(range(1,13))
monthsFmt = DateFormatter("%b '%y")
analyst_MSE = {}
analyst_dict = {}
analyst_pred = {}
for i in analyst:
    analyst_dict[i] = []
    analyst_MSE[i] = []
    analyst_pred[i] = []
    
for i in analyst_dict:
    analyst_dict[i].append([[q[2] for q in avg_nk if q[3]==i],[q[1] for q in avg_nk if q[3]==i],[q[0] for q in avg_nk if q[3]==i]])
X_pred = ''
y_pred = ''
for i in analyst_dict:
    X = np.atleast_2d(np.arange(0,len(analyst_dict[i][0][0]))).T
    y = np.atleast_2d(analyst_dict[i][0][0]).T
    MSE = get_MSE(new_kurs,avg)
    print "MSE: %f" %(MSE)
    sigma = float(np.sqrt(MSE))
    print "sigma: %f" %(sigma)
    analyst_MSE[i].append([X,y])
    y_werte = get_select(sql_prog)
    for i in analyst_pred:
        analyst_pred[i].append([[q[2] for q in y_werte if q[3]==i],[q[1] for q in y_werte if q[3]==i],[q[0] for q in y_werte if q[3]==i]])
        X_pred = np.atleast_2d(np.arange(len(new_kurs),len(new_kurs)+len(analyst_dict[i][0][0]))).T
        y_pred = np.atleast_2d(analyst_dict[i][0][0]).T
    #x = np.atleast_2d(np.arange(len(new_kurs),len(new_kurs)+len(analyst_dict[i][0][0]))).T
    x = np.atleast_2d(np.arange(0,len(new_kurs))).T
    x_pred = np.atleast_2d(np.arange(len(new_kurs),len(new_kurs)+len(analyst_dict[i][0][0]))).T
    x_gesamt = np.atleast_2d(np.arange(0,len(new_kurs)+len(analyst_dict[i][0][0]))).T
    y_gesamt = np.concatenate((y,y_pred))

# Instanciate a Gaussian Process model
gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1)

# Fit to data using Maximum Likelihood Estimation of the parameters
#gp.fit(X, y)

# Make the prediction on the meshed x-axis (ask for MSE as well)
#y_pred, MSE = gp.predict(x, eval_MSE=True)
#sigma = np.sqrt(MSE)
#print sigma
# Plot the function, the prediction and the 95% confidence interval based on
# the MSE

ui = range (len(avg))

pl.plot(ui,avg, 'b-', markersize=10, label=u'tatsaechlicher kurs')

pl.plot(X, y, 'r.', markersize=10, label=u'prognosen')
pl.plot(X_pred, y_pred, 'g.', label=u'Zukunftsprog')
pl.fill(np.concatenate([x_gesamt, x_gesamt[::-1]]), \
        np.concatenate([y_gesamt - 1.9600 * sigma,
                       (y_gesamt + 1.9600 * sigma)[::-1]]), \
        alpha=.5, fc='b', ec='None', label='95% confidence interval')
pl.xlabel('$x$')
pl.ylabel('$f(x)$')
pl.ylim(-10, 20)
pl.legend(loc='upper left')

pl.show()