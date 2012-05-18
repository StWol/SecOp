# -*- coding:utf8 -*-
import urllib2
import sys
import MySQLdb
from datetime import *
from valid_dictionaries import *


#############################################
# MYSQL Server Connection
############################################
try:
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "83jhs52u18s",
                            db = "Kursdaten")
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)    
cursor = conn.cursor () 
###############################################  

print "Ausfuehrung gestartet!"
   
#aktuelles Datum für abfrage
now = datetime.now()
y = now.year
m = now.month-1
d = now.day


#Kontrollvariable ob Ausführung erfolgreich
kontrolle = 0                    

####################################
#       Aktien aus Symbo_dict
####################################

tickers=symbol_dict.keys()

for t in tickers:
      # Open the URL
      sql_create = """create table if not exists %s (
                    kurzel CHAR(10) NOT NULL,
                    ISIN CHAR(20) NOT NULL, 
                    date DATE NOT NULL, 
                    open FLOAT NOT NULL, 
                    close FLOAT NOT NULL, 
                    volume INT NOT NULL, 
                    amount_change FLOAT NOT NULL, 
                    percent_change FLOAT NOT NULL,
                    Primary Key(date))""" % (symbol_dict[t][1])
      try:              
          cursor.execute(sql_create)
          conn.commit()
      except:
          print "Fehler bei create: %s" %t
          kontrolle = 1
          conn.rollback()          
      try:
          rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=01&c=2006&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(t,m,d,y)).readlines()     
      except:
          print 'Fehler bei Link: %s'%t
          kontrolle = 1
          
      
      z = len(rows)
      i = 1
      # i=1 weil erste zeile (rows[0]) = Date,Open,High,Low,Close,Volume,Adj Close
      while i<z:
          data = rows[i]
          i = i + 1
          data = data.split(',')
          datum = str(data[0])
          op = float(data[1])
          cl = float(data[4])
          vl = int(data[5])
          amount_ch = cl - op
          percent_ch = (amount_ch/op)*100
          sql = "INSERT INTO %s (kurzel,ISIN, \
                  date,open,close,volume,amount_change,percent_change) \
                  VALUES ('%s','%s','%s','%.2f', '%.2f', '%d', '%.2f', '%.2f' )" % \
                  (symbol_dict[t][1],t,symbol_dict[t][0],datum,op,cl,vl,amount_ch,percent_ch)
          try:
              cursor.execute(sql)
              conn.commit()
          except:
              print "Fehler bei insert: %s" %t
              kontrolle = 1
              conn.rollback()



#######################
#          Indizes
#######################

indizes_dic = {'%5EGDAXI':'DAX',
               '%5EMDAXI':'MDAX',
               '%5ETECDAX':'TECDAX',}    

i_ticker = indizes_dic.keys()

for i in i_ticker:
    sql = """create table if not exists %s (
                    date DATE NOT NULL, 
                    open FLOAT NOT NULL, 
                    close FLOAT NOT NULL, 
                    volume INT NOT NULL, 
                    amount_change FLOAT NOT NULL, 
                    percent_change FLOAT NOT NULL,
                    Primary Key (date))""" % (indizes_dic[i])
    try:
        cursor.execute(sql)
        conn.commit()                
    except:
        print "create: %s" %i
        kontrolle = 1
        conn.rollback()
    try:
        rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=01&c=2006&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(i,m,d,y)).readlines()
    except:
        print 'Fehler bei Link: %s' % i
        kontrolle = 1

    z = len(rows)-1
    x = 1 
    while x<z:
        data = rows[x]
        x = x + 1
        data = data.split(',')
        datum = str(data[0])
        op = float(data[1])
        cl = float(data[4])
        vl = int(data[5])
        amount_ch = cl - op
        percent_ch = (amount_ch/op)*100             
        sql = "INSERT INTO %s(date,open,close,volume,amount_change,percent_change) \
        VALUES ('%s','%.2f', '%.2f', '%d', '%.2f', '%.2f' )" % \
        (indizes_dic[i],datum,op,cl,vl,amount_ch,percent_ch)
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            print "insert: %s" %t
            kontrolle = 1
            conn.rollback()

if kontrolle==0:
    print "Ausfuehrung ERFOLGREICH"
        
        # update datum in file aktualisieren

    upd = datetime.strftime(now,'%Y-%m-%d')
    upd = str(upd)
    version_string = "Stocks_Version/version.txt"
    fin_version = open(version_string,"w")
    version = fin_version.write(upd)
    fin_version.close() 

else:
    print "Ausfuehrung FEHLERHAFT" 
    print "Initialisierung wiederholen!"                     