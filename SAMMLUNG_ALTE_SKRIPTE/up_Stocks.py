# -*- coding:utf8 -*-
import urllib2
import sys
import MySQLdb
from datetime import *
from valid_dictionaries import *
from db_connector import *

# MYSQL Server Connection Kursdaten
#try:
#    conn = MySQLdb.connect (host="141.62.65.151",
#                            user = "stan",
#                            passwd = "money!",
#                            db = "secop")
#    print "Mit Kursdaten verbunden"
#                            
#except MySQLdb.Error, e:
#    print "Error %d: %s" % (e.args[0], e.args[1])
#    sys.exit (1)    
#cursor = conn.cursor ()


####################################
#   Aktien aus Symbol_dict downloaden
####################################

def update_stocks():
    version_string = "Stocks_Version/version.txt"
    fin_version = open(version_string,"r")
    version = (fin_version.readline()).strip()
    fin_version.close() 
    version = version.split("-")   
    n_m = str(int(version[1]) -1) 
    tickers=symbol_dict.keys()
    
    for t in tickers:
               
          #try:
              #rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=01&c=2006&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(t,m,d,y)).readlines()
          rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(t,n_m,version[2],version[0],m,d,y)).readlines()
          #except:
           #   print "Update und Initialisierung am selben Tag! Kein Update möglich"
           #   kontrolle = 1
              
          
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
#              sql = "INSERT INTO %s (kurzel,ISIN, \
#                      date,open,close,volume,amount_change,percent_change) \
#                      VALUES ('%s','%s','%s','%.2f', '%.2f', '%d', '%.2f', '%.2f' )" % \
#                      (symbol_dict[t][1],t,symbol_dict[t][0],datum,op,cl,vl,amount_ch,percent_ch)
              sql = "INSERT INTO `kursdaten` (`unternehmen`, \
                  `datum`, `open`, `close`, `volume`, `amount_change`, `percent_change`) \
                  VALUES ((SELECT `id` FROM `unternehmen` WHERE `kuerzel`='%s'),'%s','%.2f', '%.2f', '%d', '%.2f', '%.2f' )" % \
                  (t,datum,op,cl,vl,amount_ch,percent_ch)        
                      
              try:
                  cursor.execute(sql)
                  conn.commit()
              except:
                  #print "Fehler bei insert: %s" %t
                  kontrolle = 1
                  conn.rollback()
                  
                  
#######################
#          Indizes
#######################

def update_indizes():  
    indizes_dic = {'%5EGDAXI':'DAX',
                   '%5EMDAXI':'MDAX',
                   '%5ETECDAX':'TECDAX',}    
    
    i_ticker = indizes_dic.keys()
    
    for i in i_ticker:
        try:
            #rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=01&c=2006&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(i,m,d,y)).readlines()
            rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(i,n_m,version[2],version[0],m,d,y)).readlines()
        except:
            print "Update und Initialisierung am selben Tag! Kein Update möglich"
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
                #print "insert: %s" %t
                kontrolle = 1
                conn.rollback()
#####################################################


def finish_up_Stocks():
    if kontrolle==0:
            print "Stock Update ERFOLGREICH"
            
             # update datum in file aktualisieren            
            upd = datetime.strftime(now,'%Y-%m-%d')
            upd = str(upd)
    
            version_string = "Stocks_Version/version.txt"
            fin_version = open(version_string,"w")
            fin_version.write(upd)
            fin_version.close() 
    
    else:
            print "Stock Update FEHLERHAFT"



#      
#aktuelles Datum für abfrage
now = datetime.now()
y = now.year
m = now.month-1
d = now.day

#Kontrollvariable ob Ausführung erfolgreich
kontrolle = 0                    

# datum des letzten updates
  
          