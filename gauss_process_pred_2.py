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
sql_prog ="""SELECT zieldatum,neues_kursziel,analyst FROM prognose
         WHERE unternehmen = 1 AND analyst = 779 AND `zieldatum`>(SELECT CURDATE())"""
"""AND analyst = 779"""

sql_date = "SELECT AVG( close ) , `datum` FROM kursdaten GROUP BY YEAR( `datum` ) , MONTH( `datum` )"

global_d = get_select(sql_date)
global_avg = [q[0] for q in global_d]
global_dates = [q[1] for q in global_d]
global_dates =dates.date2num(global_dates)
global_dates_dict = {}
global_list = []
i = 0
for z,j in zip(global_dates,global_avg):
    global_dates_dict[z] = [i,j]
    i = i+1  
    global_list.append([i,j])
global_x = [z[0] for z in global_list]
global_y = [z[1] for z in global_list]
#print global_dates_dict

avg_nk = get_select(sql2)
avg = [q[0] for q in avg_nk]
new_kurs = [q[2] for q in avg_nk]
datum_ziel = [q[1] for q in avg_nk]
datum_ziel =dates.date2num(datum_ziel)
analyst = [q[3] for q in avg_nk]
#print ana_prog
#months    = MonthLocator(range(1,13))
#monthsFmt = DateFormatter("%b '%y")

analyst_MSE = {}
analyst_dict = {}
analyst_pred = {}
analyst_result = {}
for i in analyst:
    analyst_dict[i] = []
    analyst_MSE[i] = []
    analyst_pred[i] = []
    analyst_result[i] = []
    
for i in analyst_dict:
    analyst_dict[i].append([[q[2] for q in avg_nk if q[3]==i],[dates.date2num(q[1]) for q in avg_nk if q[3]==i],[q[0] for q in avg_nk if q[3]==i]])

for i in analyst_dict:
    days_for_prog = []
    progs = []
    
    key = analyst_dict[i][0][1]
    prog = analyst_dict[i][0][0]
    print prog
    for k in key:       
        days_for_prog.append(global_dates_dict[k][0])
    for p in prog:
        progs.append(p)
        
    X = np.atleast_2d(np.array(days_for_prog)).T
    y = np.atleast_2d(progs).T
    MSE = get_MSE(progs,analyst_dict[i][0][2])
    print "Analyst: %d" %(i)
    print "MSE: %f" %(MSE)
    sigma = float(np.sqrt(MSE))
    print "sigma: %f" %(sigma)
    analyst_MSE[i].append([X,y])
    
    
    
    
    y_werte = get_select(sql_prog)
    
    new_kurs_prog = [q[1] for q in y_werte]
    datum_ziel_prog = [q[0] for q in y_werte]
    datum_ziel_prog =dates.date2num(datum_ziel_prog)
    analyst_prog = [q[2] for q in y_werte]
    
    for i in analyst_pred:
        analyst_pred[i].append([[q[1] for q in y_werte if q[2]==i],[q[0] for q in y_werte if q[2]==i],[q[2] for q in y_werte if q[2]==i]])

        days_for_prog_pred = []
        progs_pred = []
    
        key_pred = analyst_dict[i][0][1]
        prog_pred = analyst_dict[i][0][0]
        for k in key_pred:       
            days_for_prog_pred.append(global_dates_dict[k][0])
        for p in prog:
            progs_pred.append(p)
            
        X_pred = np.atleast_2d(days_for_prog_pred).T
        y_pred = np.atleast_2d(progs_pred).T
    #x = np.atleast_2d(np.arange(len(new_kurs),len(new_kurs)+len(analyst_dict[i][0][0]))).T
    x = np.atleast_2d(global_x).T
    x_pred = np.atleast_2d(np.arange(len(global_x),len(days_for_prog_pred)+len(global_x))).T
    x_gesamt = np.atleast_2d(np.arange(0,len(global_x)+len(days_for_prog_pred))).T
    y_gesamt = np.concatenate((y[:],y_pred[:]))
    analyst_result[i] = ([X,y,MSE,X_pred,y_pred,x,x_pred,x_gesamt,y_gesamt,sigma])
  
# Instanciate a Gaussian Process model
#gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1)

# Fit to data using Maximum Likelihood Estimation of the parameters
#gp.fit(X, y)

# Make the prediction on the meshed x-axis (ask for MSE as well)
#y_pred, MSE = gp.predict(x, eval_MSE=True)
#sigma = np.sqrt(MSE)
#print sigma
# Plot the function, the prediction and the 95% confidence interval based on
# the MSE

pl.plot(global_x,global_y, 'b-', markersize=10, label=u'tatsaechlicher kurs')
pl.hold(True)
#for i in analyst_result:
    
    #pl.plot(analyst_result[i][0][0], analyst_result[i][1][0], 'r.', markersize=10, label=u'prognosen')
    #pl.hold(True)
    #pl.plot(analyst_result[i][3][0], analyst_result[i][4][0], 'g.', label=u'Zukunftsprog')
    #pl.hold(True)
    #pl.fill(np.concatenate([analyst_result[i][7][0], analyst_result[i][7][0][::-1]]), \
    #    np.concatenate([analyst_result[i][8][0] - 1.9600 * analyst_result[i][9][0],
    #                   (analyst_result[i][8][0] + 1.9600 * analyst_result[i][9][0])[::-1]]), \
    #    alpha=.5, fc='b', ec='None', label='95% confidence interval')
    #pl.hold(True)


pl.plot(X, y, 'r.', markersize=10, label=u'prognosen')
pl.hold(True)
pl.plot(X_pred, y_pred, 'g.', label=u'Zukunftsprog')
pl.hold(True)
#pl.fill(np.concatenate([x_gesamt, x_gesamt[::-1]]), \
#    np.concatenate([y_gesamt - 1.9600 * sigma,
#                   (y_gesamt + 1.9600 * sigma)[::-1]]), \
#    alpha=.5, fc='b', ec='None', label='95% confidence interval')
pl.hold(True)

pl.xlabel('$x$')
pl.ylabel('$f(x)$')
#pl.ylim(-10, 20)
pl.legend(loc='upper left')

pl.show()