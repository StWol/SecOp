# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:10:44 2012

@author: Philipp
"""

import numpy as np
from matplotlib import pyplot as plt
#from scikits.learn.gaussian_process import GaussianProcess
from sklearn import gaussian_process
import datetime
import MySQLdb
import numpy as np
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



print "---------------------Read Data----------------------------"

sql = "SELECT AVG( close ) , `datum` FROM kursdaten WHERE unternehmen =1  GROUP BY YEAR( `datum` ) , MONTH( `datum` )"
sql1 = """SELECT `neues_kursziel`,  `zieldatum`
    FROM `prognose`, `analyst`, `analystenhaus`
    WHERE `zeithorizont`>0 AND `neues_kursziel`>0 AND `unternehmen` =1 AND `analyst` = `analyst`.`id` AND `analyst`.`analystenhaus`=`analystenhaus`.`id`"""
kurse = get_select(sql1)
n_k = [q[0] for q in kurse]
date1 = [q[1] for q in kurse]
quotes = get_select(sql)
datesss = [q[1] for q in quotes]
opens = [q[0] for q in quotes]
#rawdata=[]
##File contains 3 Columns: Year, Month, Price
#fobj=open('Oilreal_pricesReduced.txt','r')
#for el in fobj:
#    rawdata.append(el.split())
NumEl=len(n_k) #get number of instances
print NumEl
test = NumEl-20
trainIdx = []
testIdx = []
for i in range(NumEl):
    trainIdx.append(i)
    testIdx.append(i)
trainIdx=trainIdx[:test]
print trainIdx
testIdx = testIdx[test:NumEl]
print testIdx
#print type(NumEl)
#PriceList=[float(a[2]) for a in rawdata]
print "------------Partition into train- and testset------------"
#np.random.seed(32314567)
#trainIdx=list(set(np.random.random_integers((0,NumEl-20,30))))
#trainIdx = 
trainSamp=[n_k[i] for i in trainIdx]
print trainSamp
#testIdx=[i for i in trainIdx]
testSamp=[n_k[i] for i in testIdx]
print testSamp
#Transform into format required by Scikits.learn
Xtrain = np.atleast_2d(trainIdx).T
Xtest = np.atleast_2d(testIdx).T



print "------------Create GP object and train--------------------"
gp = gaussian_process.GaussianProcess(corr='squared_exponential', theta0=[5e-1] * Xtrain.shape[1], \
thetaL=[1e-3] * Xtrain.shape[1],thetaU=[1e+2] * Xtrain.shape[1], \
verbose=True, normalize=False, regr='quadratic', nugget=0.05)
gp.fit(Xtrain, trainSamp)
print "------------Output of GP parameters----------------------"
print "Horizontal length scales (one per feature) = ",gp.theta
print "Vertical length scale = ",gp.sigma2
print "Relative Noise (nugget) = ",gp.nugget
print "Coefficients of quadratic mean:"
print gp.beta
print "------------------------Prediction ---------------------"
y_pred, variance = gp.predict(Xtest, eval_MSE=True)
sigma = np.sqrt(variance)
print "-----------Compute MAE on test data---------------------"
mae=0
numTest=len(Xtest)
print numTest
for el in range(numTest):
    diff=np.abs(y_pred[el]-n_k[Xtest[el]])
    mae+=diff
mae=mae/numTest
print "MAE on test data: ",mae

print Xtest
#print [Xtest, Xtest[::-1]]
print Xtest[::-1]


print "---------------------Plotting--------------------------"
#plt.plot_date(datesss, opens, '-')
#plt.plot(range(NumEl), n_k, 'b:', label=u'real values')
plt.plot(Xtrain, trainSamp, 'r.', markersize=10, label=u'Observations')
plt.plot(Xtest, y_pred, 'b-', label=u'Prediction')
plt.fill(np.concatenate([Xtest, Xtest[::-1]]), \
    np.concatenate([y_pred + 1.9600 * sigma,
                    (y_pred - 1.9600 * sigma)[::-1]]), \
    alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('month')
plt.ylabel('Oil price')
plt.grid(True)
#pl.ylim(-10, 20)
plt.legend(loc='upper left')
#pl.title("GP with quadratic mean and trained hyperparameters (Scikits)")
plt.text(60,0,"Theta = "+str(gp.theta))
plt.text(60,-0.4,"$\sigma_f^2 = $"+str(gp.sigma2))
plt.text(60,-0.8,"nugget = "+str(gp.nugget))
plt.text(10,-1,"prior coeff. = \n"+str(gp.beta.round(decimals=2)))
plt.text(60,-1.2,"MAE = "+str(mae))
plt.title('Oil price in USD/gallon from Jan 2000 to Nov. 2010')
plt.show()