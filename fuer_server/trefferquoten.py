# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import datetime
import MySQLdb
import numpy as np
from pylab import figure, show
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib import dates
from random import randrange


################################################################################
def get_select(sql,cursor,conn):
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



def get_Analyst_quote(treffer,gesamt):
    analysten_dict_gesamt ={}
    
    for row_gesamt in gesamt:
        analysten_dict_gesamt[row_gesamt[0]] = [row_gesamt[1],0]
    
    for row_treffer in treffer:
        if row_treffer[0] in analysten_dict_gesamt:
            analysten_dict_gesamt[row_treffer[0]][1] = row_treffer[1]
            #analysten_dict_gesamt[row_treffer[0]].append(row_treffer[1])
        else:
            print row_treffer[0]
    
    for r in analysten_dict_gesamt:
        gesamtzahl_prognosen =  analysten_dict_gesamt[r][0] 
        treffer_anzahl = float(analysten_dict_gesamt[r][1])
        quote = treffer_anzahl/gesamtzahl_prognosen
        analysten_dict_gesamt[r].append(quote)
    return analysten_dict_gesamt
        

def get_Company_quotes(treffer,gesamt,unternehmen_dict):
    unternehmen_id = unternehmen_dict.keys()
    unternehmen_dict_result = {}    
    for key in unternehmen_id:
        t = []
        g =[]
        for row in gesamt:
            if key == row[2]:
                g.append(row)
        for row_treffer in treffer:
            if key == row_treffer[2]:
                t.append(row_treffer)
        result = get_Analyst_quote(t,g) 
        unternehmen_dict_result[key] = result
    return unternehmen_dict_result
    



def start_analyst():
    ####################################################
    # Gesamt Trefferquoute der Analysten ermitteln
    ####################################################
    treffer = get_select(sql)
    gesamt = get_select(sql2)

    # trefferquote_nach_analyst_dict auf folgende form bringen:
    # {id_des_Analysten: [gesamtanzahl_an_Prognosen, treffer, trefferquote]}
    trefferquote_nach_analyst_dict = get_Analyst_quote(treffer,gesamt)
    return trefferquote_nach_analyst_dict
    #################################################################################
    ##################################################################################

def start_company(cp,conn,cursor):
    ####################################################
    # Trefferquouten nach Unternehmen
    ####################################################
    treffer = get_select(sql4,cursor,conn)
    gesamt = get_select(sql3,cursor,conn)
    unternehmen = get_select(sql5,cursor,conn)

    unternehmen_dict ={}
    
    for row in unternehmen:
        unternehmen_dict[row[0]] = {}

    # trefferquote_nach_unternehmen_dict auf folgende form bringen:
    # {id_des_Unternehmens: {id_des_Analysten:[gesamtanzahl_an_Prognosen, treffer, trefferquote]}}
    trefferquote_nach_unternehmen_dict = get_Company_quotes(treffer,gesamt,unternehmen_dict)
    return trefferquote_nach_unternehmen_dict
    


### Analyst <-> anzahl richtiger Prognosen
sql="""SELECT `analyst_avg_2`.`analyst`,
COUNT(`analyst_avg_2`.`analyst`) 
FROM `analyst_avg_2`
WHERE  `analyst_avg_2`.`kurs_bei_veroeffentlichung`>0 AND `analyst_avg_2`.`zieldatum` > '2010-01-01'
AND((`analyst_avg_2`.`neue_einstufung`=1 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) > 2)
OR (`analyst_avg_2`.`neue_einstufung`=2 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) < -2)
OR (`analyst_avg_2`.`neue_einstufung`=3 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) > -2 
	AND (((`analyst_avg_2`.avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) < 2)) GROUP BY `analyst_avg_2`.`analyst`
 """


#### Analyst <-> anzahl der Prognosen   
sql2 = """
SELECT `analyst`,COUNT(*), unternehmen FROM analyst_avg_2 WHERE `zieldatum` > '2010-01-01' AND `analyst_avg_2`.`kurs_bei_veroeffentlichung`>0 GROUP BY analyst 
"""

sql3 ="""
SELECT `analyst`,COUNT(*), unternehmen FROM analyst_avg_2 WHERE `zieldatum` > '2010-01-01' AND `analyst_avg_2`.`kurs_bei_veroeffentlichung`>0 GROUP BY analyst,unternehmen 
"""
sql4="""SELECT `analyst_avg_2`.`analyst`,
COUNT(`analyst_avg_2`.`analyst`) , unternehmen
FROM `analyst_avg_2`
WHERE  `analyst_avg_2`.`kurs_bei_veroeffentlichung`>0 AND `analyst_avg_2`.`zieldatum` > '2010-01-01'
AND((`analyst_avg_2`.`neue_einstufung`=1 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) > 2)
OR (`analyst_avg_2`.`neue_einstufung`=2 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) < -2)
OR (`analyst_avg_2`.`neue_einstufung`=3 AND (((avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) > -2 
	AND (((`analyst_avg_2`.avg - `analyst_avg_2`.`kurs_bei_veroeffentlichung`)/ `analyst_avg_2`.`kurs_bei_veroeffentlichung` )*100) < 2)) GROUP BY `analyst_avg_2`.`analyst`,`analyst_avg_2`.`unternehmen`
 """
sql5 ="""
SELECT unternehmen FROM analyst_avg_2 WHERE `zieldatum` > '2010-01-01' AND `analyst_avg_2`.`kurs_bei_veroeffentlichung`>0 GROUP BY unternehmen 
"""


####################################################
# Gesamt Trefferquoute der Analysten ermitteln
####################################################
#start_analyst()



####################################################
# Trefferquouten nach Unternehmen
####################################################
#erg = start_company()
