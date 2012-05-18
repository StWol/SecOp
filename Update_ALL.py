# -*- coding: iso-8859-1 -*-
"""
Created on Wed Apr 25 21:30:07 2012

@author: Philipp
"""

import urllib2
import sys
import MySQLdb
from valid_dictionaries import *
import urllib2
from bs4 import BeautifulSoup
from datetime import *
import re
import time
import math
import h5py
import numpy as np
import time
from valid_dictionaries import *
from up_Stocks import *
from up_get_predictions import *
from up_prediction_to_database import *


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
update_stocks()
update_indizes()
finish_up_Stocks()
print "Stock Update abgeschlossen"
print "####################"



print
print "####################"
print "Starte Prognosen Update"
#--> Textfiles
main_prediction()
#--> Datenbank
main_to_db()
print "Prognosen Update abgeschlossen"
print "####################"

print
print "####################"

if (kontrolle == 0) and (control==0):
    print "Update Erfolgreich!"
    print
    print "####################"
else:
    print "Update fehlerhaft!"
    print
    print "####################"



