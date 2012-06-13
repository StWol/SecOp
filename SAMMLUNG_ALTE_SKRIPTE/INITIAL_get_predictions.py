# -*- coding: iso-8859-1 -*-
"""
Created on Sun Apr 22 14:53:37 2012

@author: Philipp
"""
#############################################
# INITIAL AUSZUFÜHREN!!!!
#############################################

import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import math
import h5py
import numpy as np
from valid_dictionaries import *

start_time=datetime.now()
            


####################################
# besorgt die prognosedaten
###################################
def get_prediction(soup):
    analysis_result = []    
    #print soup.prettify()
    
    tabelle = soup.find_all("table",{"id":"show_artikel"})[0]
    tr_raw = tabelle.find_all("tr")
     #############################################
    # tr tags müssen gefiltert werden !!!
    #############################################
    tr_filtered = filter_data(tr_raw)
    ############################################
    # nach dem filtern wird für jedes (relevante) tr tag 
    # der link geholt mit hilfe dessen die daten schließlich ausgelesen werden
    # #################################################
    for tr_z in tr_filtered:
        javascript_get = tr_z['onclick']
        reg_exp_js = r"(makeHttpRequest\('\.\.)([\S]*)(',)"
        reg_search_js = re.search(reg_exp_js,javascript_get)
        get_analysis_link = reg_search_js.group(2)
        complete_link = "http://www.boersen-zeitung.de%s" % (get_analysis_link)
        try:
            html_analysis = urllib2.urlopen(complete_link).read()
            time.sleep(2)
        except:
            print "Fehler in get_prediction!"
            print "Link!!!"
            print complete_link
        
        try:
            soup_analysis = BeautifulSoup(html_analysis)
        except:
            print "Fehler in get_prediction!"
            print "Soup!!"
            print soup_analysis
        ################################################################
        # nachdem die seite geparsed wurde werden aus der tabelle (vgl. seite)
        #ISIN, Datum,Zeithorizont, Neues_Kursziel, Altes_Kursziel, Neue_Einstufung, Alte_Einstufung, Kurs_bei_Veroeffentlichung,
        # ausgelesen und entsprechend angepasst hinsichtlich der speicherung im txtfile
        #anschließend werden sie in dieser reihenfolge an die liste analysis_list zugewiesen
        # analyst und analysehaus müssen aus dem text gefiltert werden
        #######################################################################
        try:
            td_table = soup_analysis.find_all("table")[1].find_all("td")[1::2]
        except:
            print "Fehler in get_prediction!"            
            print "td_table"
            print td_table
            #
            # ISIN, Datum,Zeithorizont, Neues_Kursziel, Altes_Kursziel, Neue_Einstufung, Alte_Einstufung, Kurs_bei_Veroeffentlichung, 
            #            
        date_tmp = datetime.strptime(td_table[1].get_text(), '%d.%m.%Y %X')
        date = date_tmp.strftime('%Y-%m-%d')
        date.strip()
        
        zeithorizont = str(td_table[2].get_text())
        zeithorizont = zeithorizont.replace("Monate","")
        zeithorizont.strip()
        
        n_kz = str(td_table[3].get_text())
        n_kz = n_kz.replace("EUR","")
        n_kz = n_kz.replace(",",".")
        n_kz.strip()
        
        a_kz = str(td_table[4].get_text())
        a_kz = a_kz.replace("EUR","")
        a_kz = a_kz.replace(",",".")
        a_kz.strip()
        
        v_k = str(td_table[7].get_text())
        v_k = v_k.replace("EUR","")
        v_k = v_k.replace(",",".")
        v_k.strip()
        
        
        try:             
            analysis_list = [str(td_table[0].get_text()),date, zeithorizont, n_kz, a_kz,str(td_table[5].get_text()),str(td_table[6].get_text()), v_k]
        except:
            print "Fehler in get_prediction!"            
            print "analysis_list"
            print analysis_list
         #
        # Analyst abholen
        #  
        analysis_list = get_analyst_name(html_analysis, analysis_list)
       #
        # Analysehaus abholen
        #
        analysis_list = get_bank_name(html_analysis, analysis_list)
        #
        #die ergebnisse dieser einen seite werden nun an die lsite für das gesamte unternehmen analysis_result gehängt
        # im anschluss daran wird analysis_result an zurückgegeben (aufruf kam von parse_company)
        try:        
            analysis_result.append(analysis_list)
        except:
            print "Fehler in get_prediction!"            
            print "analysis_result"
            print analysis_result
    return analysis_result


###########################################
# ermittelt aus html_analysis den namen des analysten
# mittels regulärem ausdruck
# # hängt das ergebnis an die übergebene liste an und gibt die neue wieder zurück
#############################################
def get_analyst_name(html_analysis, analysis_list):
    try:
        reg_exp_analyst = r"Analyst(in)?\s[(\w)|(ä|ö|ü|Ä|Ö|Ü|ß]*(-[(\w)|(ä|ö|ü|Ä|Ö|Ü|ß]*)?\s(?:von|zu|van|de|di|d`|d'|v.|z.|O`|O'|[\w\.])?.[(\w)|(ä|ö|ü|Ä|Ö|Ü|ß]*(-([(\w)|(ä|ö|ü|Ä|Ö|Ü|ß]*))?"
        reg_search_analyst = re.search(reg_exp_analyst,html_analysis)
        analyst_name = reg_search_analyst.group()
        reg_exp_cut = r"Analyst(in)?"
        analyst_name = re.sub(reg_exp_cut,"",analyst_name)      
        analyst_name = analyst_name.strip()
        #analyst_name = analyst_name.group(1,2)
        analysis_list.append(analyst_name)
        return analysis_list
    except:
        #print "Analyst nicht verfügbar!"
        #print analysis_list        
        analyst_name = "N_A"
        analysis_list.append(analyst_name)
        return analysis_list
                

############################################
# ermittelt den namen des analysehauses
# sucht in html_analysis nach dem key des bankhaus dictionary
# hängt das ergebnis an die übergebene liste an und gibt die neue wieder zurück
##########################################
def get_bank_name(html_analysis, analysis_list):
    bank_name = ""    
    for b in banks:
        s = re.search(b,html_analysis)
        if s != None:
            bank_name = s.group()
            break
    try:
        bank_name = bankhaus_dict[bank_name]
    except:
        #print "Bank Name unbekannt!"
        #print bank_name        
        bank_name = "N_A"
    analysis_list.append(bank_name)
    return analysis_list
    

######################################
# wir benötigen nur die tr tags bei denen das zweite td tag der class "ue_fl"
# die art "analyser" angibt !!!
# filter_data filtert die tr tags danach
#####################################        
def filter_data(tr_raw):
    tr_filtered = []    
    for tr_i in tr_raw:
        td_i = tr_i.find_all("td", { "class" : "ue_fl" })
        if td_i[1].get_text().strip()=="Analyser":
            tr_filtered.append(tr_i)
    return tr_filtered
    
###########################################
# ermittelt die seitenanzahl für jedes unternehmen
##########################################
def get_site_count(soup):
    try:    
        anzahl_seiten = soup.find("td",{"class":"textzusatz"})
        anzahl_seiten = anzahl_seiten.get_text()
        anzahl_seiten = anzahl_seiten.replace("Anzahl:","")
        reg_exp_anz = r"Treffer:(.)*"
        anzahl_seiten = re.sub(reg_exp_anz,"",anzahl_seiten)
        anzahl_seiten.strip()
        anzahl_seiten = float(anzahl_seiten)
        anzahl_seiten = math.ceil(anzahl_seiten/10.)
        anzahl_seiten = int(anzahl_seiten)
        return anzahl_seiten
    except:
        print "Fehler bei Anzahl_Seiten"
        print soup        
        anzahl_seiten = 1
        return anzahl_seiten
###########################################
# iteriert über die anzahl an seiten 
#parsed die jeweilige seite
#key sind die seiten
# ruft für jede seite get_prediction auf
# get_prediction zeiht die daten aus der geparsten seite und liefert liste mit den resultaten zurück
# nachdem alle seiten abgearbeitet wurden, können die daten im textfile gespeichert werden --> to_textfile 
###########################################     
def parse_company(start, stop, t,company_result_set):
    while start < stop:
        try:
            cp_link = "http://www.boersen-zeitung.de/index.php?l=0&li=5&flag=research&quelle=dpa&ansicht=analyser&artikel=&isin=%s&page_number=%d#jump" % (symbol_dict[t][0],start)
            html = urllib2.urlopen(cp_link).read()
            time.sleep(2)            
            soup = BeautifulSoup(html)
             #
            # aufruf get_prediction()
            # besorgt die prognosedaten
            # get_prediction() liefert eine liste der prognosedaten
            #die im dictionary company_result_set unter dem key seitenzahl abgelegt wird
            # sind alle seiten abgearbeitet wird to_textfile aufgerufen
            #
            data = get_prediction(soup)
            company_result_set[start] = [data]
            start = start + 1
        except:
            print "Fehler in parse_company bei Unternehmen %s auf Seite %d" %(t,start)
    to_textfile(company_result_set,t,stop)

###############################################
# speichert das company_result_set als textfile unter dem namen des unternehmens
# ebenso wird die anzahl an seitendurchläufen und die dafür benötigte zeit in 
#einem textfile mit dem zusatz _COUNT gespeichert
#################################################
def to_textfile(company_result_set,t,stop):  
    keys = company_result_set.keys()
    cp_file = "txtfiles/%s.txt" % symbol_dict[t][1]
    fout=open(cp_file,"w")
    fout.write("ISIN,Datum,Zeithorizont,Neues_Kursziel,Altes_Kursziel,Neue_Einstufung,Alte_Einstufung,Kurs_bei_Veroeffentlichung,Analyst,Analysehaus\n") 
    for k in keys:
        l1 = len(company_result_set[k][0])
        if l1>0:
            for i in range(0,l1):       
                for z in range(0,10):           
                    fout.write(company_result_set[k][0][i][z])
                    if(z!=10):
                        fout.write(",")
                        
                fout.write("\n")
    fout.close()
    stop = str(stop) 
    dauer = str(datetime.now() - start_time)
    count = "txtfiles/%s_COUNT.txt" % symbol_dict[t][1]
    fout_count = open(count,"w")
    fout_count.write(stop)
    fout_count.write("\n")
    fout_count.write(dauer)
    fout_count.close()
    
        
    
def main_prediction():
    for t in tickers:
        print "In Bearbeitung: %s" % symbol_dict[t][1]
        global start_time
        start_time = datetime.now()
        company_result_set = {} 
        #############################################
        #initialer seitenaufruf --> die anzahl an seiten holen
        ############################################
        initial_cp_link = "http://www.boersen-zeitung.de/index.php?l=0&li=5&flag=research&quelle=dpa&ansicht=analyser&artikel=&isin=%s&page_number=0#jump" % (symbol_dict[t][0])
        try:
            initial_html = urllib2.urlopen(initial_cp_link).read()
            time.sleep(1)
        except:
            print "Fehler in main_prediction bei Unternehmen: %s" %t
            print "Link konnte nicht geöffnet werden"                        
        
        soup_initial = BeautifulSoup(initial_html)
        ##################################################
        # um die seite '0' nicht doppelt parsen zu müssen: sofortiger aufruf von get_prediction
        # und ablegen der daten in company_result_set
        ##################################################
        initial_data = get_prediction(soup_initial)
        company_result_set[0] = [initial_data]
        site_counter = get_site_count(soup_initial)
        ###################################################
        # nun kennen wir die seitenanzahl
        # gibt es mehr als eine seite: parse_company iteriert über die seiten beginnend bei 1
        #weil die 0te seite bereits geparsed wurde
        #das company_result_set wird mit übergeb, das in dem fall aus den daten auf der 0ten seite besthet bereits ausgewertete 0te seite wird mit übergeben
        ###################################################
        if site_counter > 1:
            parse_company(1,site_counter,t,company_result_set)
         #####################################################
        # existiert nur eine Seite muss diese in parse_company nochmals geparsed werden
        # company_result_set ist ein dictionary! key ist die seitenanzahl
        # unternehmen die nur eine seite besitzen: ihre eine seite wird zweimal geparsed
        # da seitenzahl der key im dictionary ist, wird einfach überschrieben --> keine doppelte abspeicherung
        ######################################################
        else:
            parse_company(0,1,t,company_result_set)
        
        
tickers = symbol_dict.keys()
banks = bankhaus_dict.keys()

  