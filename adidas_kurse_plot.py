# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:37:04 2012

@author: sw128
"""
import MySQLdb

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
    sql = "SELECT AVG( close ) , `datum` FROM kursdaten WHERE unternehmen =96 GROUP BY YEAR( `datum` ) , MONTH( `datum` )"
    result = []
    try:
        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchall()
        print result
    except MySQLdb.Error, e:
        conn.rollback()
        print "Error %d: %s" % (e.args[0], e.args[1])
