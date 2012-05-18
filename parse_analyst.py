# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:59:38 2012

@author: Stan
"""
import MySQLdb, sys
from nltk.metrics import edit_distance

#####################################################################
##############         Init DB Connection        ####################
#####################################################################
try:
    conn = MySQLdb.connect (host="141.62.65.151",
                            user = "stan",
                            passwd = "money!",
                            db = "secop")

#    conn = MySQLdb.connect (host="localhost",
#                            user = "root",
#                            passwd = "83jhs52u18s",
#                            db = "secop")                        
    print "Mit secop verbunden"
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1) 
    
cursor = conn.cursor ()

def get_analyst():
    
    analys_dict = {}
    sql = "select `name`,`id` from `analyst` GROUP BY `name`"
    #"""select AVG(`close`),`unternehmen`.name from `kursdaten`,`unternehmen` where `datum` between '2012-01-01'and'2012-01-31' AND `unternehmen`=1 AND `unternehmen`.id=`kursdaten`.`unternehmen`"""
    try:
        cursor.execute(sql)
        conn.commit()
        for row in cursor: 
            analys_dict[row[0]]= row[1]    
    except MySQLdb.Error, e:
            conn.rollback()
            print "Error %d: %s \t " % (e.args[0], e.args[1])   
    return analys_dict


def get_sim(analys_dict):
    
    sim_dict = {}
    name_list = analys_dict.keys()
    
    for name1 in name_list:
        for name2 in name_list:
            dist = edit_distance(name1,name2)
            if(dist < 3 and dist > 0):
                sim_dict[analys_dict[name1]]= analys_dict[name2]
                name_list.remove(name2)
                print "%d %s : %d %s" % (analys_dict[name1], name1, analys_dict[name2], name2)
    return sim_dict

print "================================="
print len(get_sim(get_analyst()) )
            