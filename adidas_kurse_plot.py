# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:37:04 2012

@author: sw128
"""
import MySQLdb
import numpy as np
import h5py
from matplotlib import pyplot as plt
#####################################################################
##############         Init DB Connection        ####################
#####################################################################
try:
    conn = MySQLdb.connect (host="141.62.65.151",
                            user = "stan",
                            passwd = "money!",
                            db = "secop")
                      
    print "Mit secop verbunden"
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])

    
cursor = conn.cursor ()


def get_closeAVG():
    #sql = "SELECT AVG( close ) , `datum` FROM kursdaten WHERE unternehmen =96 GROUP BY YEAR( `datum` ) , MONTH( `datum` )"
    sql =  "SELECT close , `datum` FROM kursdaten WHERE unternehmen =96 GROUP BY YEAR( `datum` ) , MONTH( `datum` )"    
    result = []
    try:
        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchall()
        result = np.array(result)
        result = np.transpose(result)
        return result
        
    except MySQLdb.Error, e:
        conn.rollback()
        print "Error %d: %s" % (e.args[0], e.args[1])


sql = """SELECT `neues_kursziel`, `analyst`.`name`, `analystenhaus`.`name`, `zieldatum`
    FROM `prognose`, `analyst`, `analystenhaus`
    WHERE `unternehmen` =96 AND `analyst` = `analyst`.`id` AND `analyst`.`analystenhaus`=`analystenhaus`.`id`"""

def get_select(sql):
    result = []
    try:
        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchall()
        result = np.array(result)
        result = np.transpose(result)
        return result
        
    except MySQLdb.Error, e:
        conn.rollback()
        print "Error %d: %s" % (e.args[0], e.args[1])


sql9 = """SELECT `zieldatum`
    FROM `prognose`
    WHERE `unternehmen` =96 AND"""


#sql2 = "SELECT `datum` FROM kursdaten WHERE unternehmen =96"
ps = get_select(sql)
datey = get_select(sql9)

n_k = ps[0,:]
name = ps[1,:]
haus = ps[2,:]
zieldatum =ps[3,:] 



figure = plt.figure()

subplot = figure.add_subplot(111,axisbg='#cccccc')

#sql2 = "SELECT `datum` FROM kursdaten WHERE unternehmen =96"

#ole = get_select(sql2)

result = get_closeAVG()

kurse = result[0,:]
datum = result[1,:]

#uiuiui = get_select(sql3)
#subplot.plot(kurse,linewidth=2.0)

#plt.hold(True)
#subplot.scatter(zieldatum,n_k)
#subplot.grid(True)
#subplot.set_xticklabels(datum)
plt.hold(True)
plt.plot(kurse, c='black', label='Kursverlauf')
plt.hold(True)
plt.scatter(datey, n_k, c='black', label='Kursverlauf')
plt.hold(True)
plt.legend(loc=3)
#subplot.set_xticklabels(datum)
plt.xlabel('days')
plt.ylabel('Euro')
plt.show()










