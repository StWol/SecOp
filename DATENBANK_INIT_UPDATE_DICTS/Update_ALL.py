# -*- coding: iso-8859-1 -*-
"""
Created on Wed Apr 25 21:30:07 2012

@author: Philipp
"""

import time
import up_Stocks 
import up_get_predictions
import install_db

##################################
#           START
#################################

# control als Kontrollvariable für up_prediction to database
#control = 0
#
#tickers = symbol_dict.keys()
#banks = bankhaus_dict.keys()
#start_time=datetime.now()
#
##aktuelles Datum für abfrage
#now = datetime.now()
#y = now.year
#m = now.month-1
#d = now.day
#
##Kontrollvariable für up_stocks ob Ausführung erfolgreich
#kontrolle = 0                    
#
## datum des letzten updates
#version_string = "Stocks_Version/version.txt"
#fin_version = open(version_string,"r")
#version = (fin_version.readline()).strip()
#fin_version.close() 
#version = version.split("-")


######################################
#   Funtionsaufrufe
######################################

print "Starte kompletten Update Vorgang"
print
print "####################"
##################################################
# UPDATE STOCKS:
##################################################    
 
print
print "####################"
print "Starte Stock Update"
up_Stocks.update_stocks()
up_Stocks.finish_up_Stocks()
print "Stock Update abgeschlossen"
print "####################"



print
print "####################"
print "Starte Prognosen Update"
up_get_predictions.main_prediction()
install_db.updateDB()
print "Prognosen Update abgeschlossen"
print "####################"

print
print "####################"





