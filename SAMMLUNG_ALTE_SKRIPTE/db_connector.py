# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:16:09 2012

@author: Philipp
"""
import sys, MySQLdb

######################################################################
###############         Init DB Connection        ####################
######################################################################
try:
    conn = MySQLdb.connect (host="141.62.65.151",
                            user = "stan",
                            passwd = "money!",
                            db = "secop")
                      
    print "Mit secop verbunden"
                           
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1) 
    
cursor = conn.cursor ()