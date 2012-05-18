# -*- coding: iso-8859-1 -*-
"""
Created on Thu May 10 11:53:09 2012

@author: Stan
"""
import urllib2, sys, MySQLdb
import read_textfile, valid_dictionaries

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


#####################################################################
##############         Init DB Connection        ####################
#####################################################################
try:
#    conn = MySQLdb.connect (host="141.62.65.151",
#                            user = "stan",
#                            passwd = "money!",
#                            db = "secop")

    conn = MySQLdb.connect (host="localhost",
                            user = "root",
                            passwd = "83jhs52u18s",
                            db = "secop")                        
    print "Mit secop verbunden"
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1) 
    
cursor = conn.cursor ()


now = datetime.now()
y = now.year
m = now.month-1
d = now.day
#####################################################################
#####################################################################
#####################################################################



def einstufungenToDB(einstufungen):
    for i in einstufungen:
        sql = "INSERT INTO `einstuffung` (`wert`) VALUES ('%s')" % i
        try:
            cursor.execute(sql)
            conn.commit()
        except MySQLdb.Error, e:
            conn.rollback()
            print "Error %d: %s" % (e.args[0], e.args[1])
            continue

# alle Indizes in der DB speichern
###############################################
def indexToDB(indizes_list):
    indizes_whit_db_id = {}
    for index in indizes_list:
        sql = "INSERT INTO `index` (`index`) VALUES ('%s')" % index
        try:
            cursor.execute(sql)
            indizes_whit_db_id[index] = cursor.lastrowid
            conn.commit()
        except MySQLdb.Error, e:
            conn.rollback()
            print "Error %d: %s" % (e.args[0], e.args[1])
            continue
    return indizes_whit_db_id

# alle Unternehmen in der DB speichern
###############################################
def companyToDB(company_dict):
    
    company_whit_db_id_dict = {}
    for key, value in company_dict.iteritems():
        sql = "INSERT INTO `unternehmen` (`kuerzel`,`ISIN`,`name`,`index`) VALUES ('%s','%s','%s',(SELECT `id` FROM `index` WHERE `index`='%s'))" % (key, value[0],value[1],value[2])
       
        try:
            cursor.execute(sql)
            conn.commit()
            company_whit_db_id_dict[value[1]] = cursor.lastrowid
            print "unternehmen %s eingefuegt" % key 
        except:
            conn.rollback()
            print "Unexpected error:", sys.exc_info()[1]
    return company_whit_db_id_dict
        
# alle Kursdaten in der DB speichern
###############################################
def kursdatenToDB(company_kuerzel_list):
    for company in company_kuerzel_list:
        try:
            rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=01&c=2006&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(company,m,d,y)).readlines()     
        except:
            print 'Fehler bei Link: %s' % company
            continue            
            
        for row in rows[1:]:
            row = row.split(',')
            datum = str(row[0])
            op = float(row[1])
            cl = float(row[4])
            vl = int(row[5])
            amount_ch = cl - op
            percent_ch = (amount_ch/op)*100
            sql = "INSERT INTO `kursdaten` (`unternehmen`, \
                  `datum`, `open`, `close`, `volume`, `amount_change`, `percent_change`) \
                  VALUES ((SELECT `id` FROM `unternehmen` WHERE `kuerzel`='%s'),'%s','%.2f', '%.2f', '%d', '%.2f', '%.2f' )" % \
                  (company,datum,op,cl,vl,amount_ch,percent_ch)
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                print "Fehler bei insert: %s" % company 
                print sys.exc_info()[1]
                conn.rollback()
                continue

        print "unternehmen %s eingefuegt mit %d zeilen" % (company, len(rows))


# alle Analystenhaeuser in die DB speichern
###############################################
def analystenhausToDB(haus_list):
    haus_with_db_id_dict ={}
    
    for haus in set(haus_list):
        sql = "INSERT INTO `secop`.`analystenhaus` (`name`) VALUES ('%s')" % haus
        try:
            cursor.execute(sql)
            haus_with_db_id_dict[haus] = cursor.lastrowid
            conn.commit()
        except MySQLdb.Error, e:
            conn.rollback()
            print "Error %d: %s" % (e.args[0], e.args[1])
            continue
    
    return haus_with_db_id_dict      


# alle Analysten in die DB speichern
###############################################
def analystToDB(analyst_dict):
    analyst_with_db_id_dict = {}

    for analyst_row in analyst_dict:
        analyst = analyst_row[0]
        haus = analyst_row[1]
        
        sql = "INSERT INTO `secop`.`analyst` (`name`,`analystenhaus`) VALUES ('%s',(SELECT `id` FROM `analystenhaus` WHERE `name`='%s'))" % (analyst, haus)

        
        try:
            cursor.execute(sql)
            analyst_with_db_id_dict[analyst] = cursor.lastrowid
            conn.commit()
        except MySQLdb.Error, e:
            conn.rollback()
            print "Error %d: %s" % (e.args[0], e.args[1])
    
    return analyst_with_db_id_dict     


# alle Vorhersagen in die DB speichern
###############################################
def allPredictionsToDB(company_list):
    predict_count = 0
    for company in company_list:
        predict_count += __companyPredictionsToDB(company[1])
        print "%d \t %s " % (predict_count,company[1])
        
    return predict_count

# alle Vorhersagen einer Firma in die DB speichern    
###############################################
def __companyPredictionsToDB(company):
    predcit_list = reader.get_companyPredictionsAsList(company)    

    
    for row in predcit_list:
        date = datetime.strptime(row[1],'%Y-%m-%d')
        zieldatum = date + relativedelta( months =+ int(row[2]) )
        
        sql = """INSERT INTO `prognose` (
                `unternehmen`,
                `analyst`,
                `datum`,
                `zieldatum`,
                `zeithorizont`,
                `neues_kursziel`,
                `altes_kursziel`,
                `neue_einstufung`,
                `alte_einstufung`,
                `kurs_bei_veroeffentlichung`) 
            VALUES (
                (SELECT id FROM `unternehmen` WHERE `name`='%s'),
                (SELECT `analyst`.`id` FROM `analyst`, `analystenhaus` WHERE `analyst`.`name`='%s' AND `analystenhaus`.`name` = '%s' AND `analyst`.`analystenhaus`=`analystenhaus`.`id`),
                '%s',
                '%s',
                '%d',
                '%.2f',
                '%.2f',
                (SELECT id FROM einstuffung WHERE wert='%s'),
                (SELECT id FROM einstuffung WHERE wert='%s'),
                '%.2f'                
                )""" % (company, row[8], row[9],row[1],str(zieldatum),row[2],row[3],row[4],row[5],row[6],row[7])
        try:
            cursor.execute(sql)
            conn.commit()
        except MySQLdb.Error, e:
            conn.rollback()
            print "Error %d: %s \t in %s" % (e.args[0], e.args[1], company.replace("_"," "))        
        
    return len (predcit_list)
    


reader = read_textfile.Reader()            


#einstufungenToDB(einstufungen)
#print "Einstuffungen gespeichert"
# 
#inx = indexToDB(indizes_dic.values())   
#print "insert %d indizies" % len( inx )
# 
#haeuser = analystenhausToDB(reader.get_analyseHaeuser())
#print "insert %d analystenhaeuser" % len( haeuser )
#
#ana = analystToDB(reader.get_analystenList())
#print "insert %d analyst" % len( ana )

#
#cp_dict = companyToDB(symbol_dict)
#print "%d Unternehmen eingefügt" % len(cp_dict)
#
#count = allPredictionsToDB(symbol_dict.values())
#print "%d Vorhersagen eingefügt" % count

kursdatenToDB(valid_dictionaries.symbol_dict.keys())