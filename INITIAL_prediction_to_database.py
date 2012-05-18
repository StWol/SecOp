# -*- coding: iso-8859-1 -*-
"""
Created on Sun Apr 22 14:53:37 2012

@author: Philipp
"""
import sys
import MySQLdb
from datetime import datetime
import time
from valid_dictionaries import *


def create_table(t):        
    sql_create = """create table if not exists %s_Prog (
                    ISIN CHAR(20), 
                    date DATE, 
                    Zeithorizont INT,                    
                    Neues_Kursziel FLOAT, 
                    Altes_Kursziel FLOAT, 
                    Neue_Einstufung CHAR(15), 
                    Alte_Einstufung CHAR(15), 
                    Kurs_bei_Veroeffentlichung FLOAT,
                    Analyst CHAR(50),
                    Analysehaus CHAR(30),
                    Primary Key(ISIN,date,Zeithorizont,Neues_Kursziel,Altes_Kursziel,Neue_Einstufung,Alte_Einstufung,Kurs_bei_Veroeffentlichung,Analyst,Analysehaus))""" % (symbol_dict[t][1])    
    try:
        cursor.execute(sql_create)
        conn.commit()
    except:
        conn.rollback()
        print "Create Fehler: %s" %t
        set_control_to_one()
        
        



def insert_in_table(cp_list,t):
    sql = "INSERT INTO %s_Prog (ISIN,date,Zeithorizont,Neues_Kursziel,Altes_Kursziel,Neue_Einstufung,Alte_Einstufung,Kurs_bei_Veroeffentlichung,Analyst,Analysehaus) \
            VALUES ('%s','%s','%d','%.2f', '%.2f','%s','%s','%.2f', '%s','%s' )" % \
            (symbol_dict[t][1], cp_list[0],cp_list[1],cp_list[2],cp_list[3],cp_list[4],cp_list[5],cp_list[6],cp_list[7],cp_list[8],cp_list[9])
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()

def convert_data(cp_raw,t):
    for i in range(1,len(cp_raw)):       
            cp_list = cp_raw[i].split(",",9)
            try:
                cp_list[2] = int(cp_list[2].strip())
            except:
                cp_list[2] = -1
            
            try:
                cp_list[3] = float(cp_list[3].strip())
            except:
                cp_list[3]= -1
                
            try:
                cp_list[4] = float(cp_list[4].strip())
            except:
                cp_list[4]= -1
                
            try:
                cp_list[7] = float(cp_list[7].strip())
            except:
                cp_list[7]= -1
            
            cp_list[8] = (cp_list[8].replace(' ',"_")).strip()
            
            cp_list[9] = (cp_list[9].replace(',\n',"")).strip()            
            
            insert_in_table(cp_list,t)


def main_to_db():        
    for t in tickers:
        #print "In Bearbeitung: %s" %t        
        cp_file = "txtfiles/%s.txt" % symbol_dict[t][1]
        try:
            fin = open(cp_file,"r")
            cp_raw = fin.readlines()
            fin.close()
            create_table(t)
            # nach erfolgreichem convert ruft convert_data für jede zeile direkt insert_in_table auf      
            convert_data(cp_raw,t)
        except:
            print "FILE nicht da: %s" % (symbol_dict[t][1])
            set_control_to_one()


def set_control_to_one():
    global control
    control = 1
    
def finish():
    global control
    date_tmp = datetime.now()
    date = str(date_tmp.strftime('%Y-%m-%d')).strip()  
    update_file = "txtfiles/AAA_Initialisierung_Prognosen_DB.txt"
    fout_update_file = open(update_file,"w")
    fout_update_file.write("Initialisierung der DB 'Prognosen' am: \n")
    fout_update_file.write(date)    
    if control==0:
        fout_update_file.write("\nInitialisierung ERFOLGREICH! Tabellen aller Unternehmen erstellt und initial befüllt!")
    else:
        fout_update_file.write("\nInitialisierung FEHLERHAFT!!! Vergleiche Konsolenausgaben!")
    fout_update_file.close()
    print "Update File geschrieben!"
    print "Ausführung abgeschlossen! Bitte Update-File 'AAA_Initialisierung_Prognosen_DB.txt' lesen!!"    



#############################################
# MYSQL Server Connection
############################################
try:
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "83jhs52u18s",
                            db = "Prognosen")
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)    
cursor = conn.cursor ()
###############################################   


##############################################
# Setzen Kontrollvariable für Fehlererkennung, 
# keys für tickers und banks holen, 
# funktionsablauf starten
##############################################
control = 0
tickers = symbol_dict.keys()
banks = bankhaus_dict.keys()   
print "Starte Bearbeitung!"
main_to_db()
finish()
