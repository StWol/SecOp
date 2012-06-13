# -*- coding: utf-8 -*-
"""
Created on Tue May 22 16:17:09 2012

@author: Philipp
"""
import install_db
import INITIAL_get_predictions

print "Parsen gestartet! Erstelle txtfiles!"
INITIAL_get_predictions.main_prediction()
print "Parsen beendet"

print

print "Initialisiere Datenbank"
install_db.installDB()
print "BEENDET"