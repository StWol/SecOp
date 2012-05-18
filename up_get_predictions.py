# -*- coding: iso-8859-1 -*-
"""
Created on Tue Apr 24 19:51:53 2012

@author: Philipp
"""

#############################################
# Auszuführen NACHDEM Initial_get_Predictions erfolgreich ausgeführt wurde!!!
# Hängt neue Prognosedaten an die bestehenden txtfiles an!
#############################################

import urllib2
from bs4 import BeautifulSoup
from datetime import *
import re
import time
import math
import h5py
import numpy as np
from valid_dictionaries import *

#start_time=datetime.now()

 

####################################
# besorgt die prognosedaten
###################################
def get_prediction(soup,t):
    analysis_result = [] 
    tr_filtered = []
    #print soup.prettify()
    
    tabelle = soup.find_all("table",{"id":"show_artikel"})[0]
    tr_raw = tabelle.find_all("tr")
    #############################################
    # tr tags müssen gefiltert werden !!!
    #############################################
    #print tr_raw    
    tr_filtered = filter_data(tr_raw,t)
    
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
# in der UPDATE Version wird zusätzlich nach dem Veröffentlichungsdatum gefiltert
#####################################    
def filter_data(tr_raw,t):
    tr_filtered = []
    date_from_initial_file = "txtfiles/%s.txt" % symbol_dict[t][1]
    date_from_update_file = "UPDATE_txtfiles/%s.txt" % symbol_dict[t][1]    
    try:
        fin_date = open(date_from_update_file,"r")
        line_1 = fin_date.readline()
        line_2 = fin_date.readline()
        fin_date.close()
        line_2 = line_2.split(",",9)
        date_from_file = datetime.strptime(line_2[1],'%Y-%m-%d')
        t = timedelta(days=1)
        date_from_file = date_from_file - t
    except:
        fin_date = open(date_from_initial_file,"r")
        line_1 = fin_date.readline()
        line_2 = fin_date.readline()
        fin_date.close()
        line_2 = line_2.split(",",9)
        date_from_file = datetime.strptime(line_2[1],'%Y-%m-%d')
        t = timedelta(days=1)
        date_from_file = date_from_file - t 
    
    for tr_i in tr_raw:
        td_i = tr_i.find_all("td", { "class" : "ue_fl" })
        date_from_site = td_i[0].get_text()
        date_from_site = date_from_site.strip()
        reg_exp_date = r"[0-9][0-9].[0-1][0-9].[0-9][0-9]"
        reg_search_date = re.search(reg_exp_date,date_from_site)
        date_from_site = reg_search_date.group()
        date_from_site = date_from_site.split(".")
        year = date_from_site[2]
        year = "20%s"%year
        date_from_site = "%s-%s-%s"% (year,date_from_site[1], date_from_site[0])
        #print date_from_site
        date_from_site = datetime.strptime(date_from_site, '%Y-%m-%d')
                
        if td_i[1].get_text().strip()=="Analyser" and date_from_site.date() > date_from_file.date():
                tr_filtered.append(tr_i)
        else:
            continue
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
def parse_company(start, stop, t,company_result_set,sum_sites):
    while start < stop:
       # try:
            cp_link = "http://www.boersen-zeitung.de/index.php?l=0&li=5&flag=research&quelle=dpa&ansicht=analyser&artikel=&isin=%s&page_number=%d#jump" % (symbol_dict[t][0],start)
            html = urllib2.urlopen(cp_link).read()
            time.sleep(2)            
            soup = BeautifulSoup(html)
            #
            # aufruf get_prediction()
            # besorgt die prognosedaten
            # zurück kommt eine liste die im dictionary company_result_set unter dem key seitenzahl
            # abgelegt wird
            # sind alle seiten abgearbeitet wird zo_textfile aufgerufen 
            #
            #try:            
            data = get_prediction(soup,t)
            #except:
                #print "aufruf von get_pre"
            company_result_set[start] = [data]
            start = start + 1
        #except:
         #   print "Fehler in parse_company bei Unternehmen %s auf Seite %d" %(t,start)
    to_textfile(company_result_set,t,sum_sites)



###############################################
# speichert das company_result_set als textfile unter dem namen des unternehmens
# ebenso wird die anzahl an seitendurchläufen und die dafür benötigte zeit in 
#einem textfile mit dem zusatz _COUNT gespeichert
###############################################

#       DIE INITIALEN TEXTFILES WERDEN NICHT ANGERÜHRT
def to_textfile(company_result_set,t,sum_sites):  
    keys = company_result_set.keys()
    #
    # schreibe oder überschreibe in updated_txtfiles nur die neuen zeilen!
    # diese wrden für updatevorgang herangezogen
    # erstelle neues countfile mit aktualisiertem count
    #
    cp_file = "UPDATE_txtfiles/%s.txt" % symbol_dict[t][1]
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
    
    sum_sites = str(sum_sites) 
    dauer = str(datetime.now() - start_time)
    count = "UPDATE_txtfiles/%s_COUNT.txt" % symbol_dict[t][1]
    fout_count = open(count,"w")
    fout_count.write(sum_sites)
    fout_count.write("\n")
    fout_count.write(dauer)
    fout_count.close()
    
    
    # die neuen zeilen im Ordner APPENDED_txtfiles an bestehende textfiles anhängen!
    # bevor das so funktioniert wie es soll müssen alle txt files aus dem ordner txtfiles
    # von hand in den ordner APPENDED_txtfiles kopiert werden
    
    append_initial_txtfile = "APPENDED_txtfiles/%s.txt" % symbol_dict[t][1]
    fout=open(append_initial_txtfile,"a")
    fout.write("\n") 
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
    
    
    append_initial_countfile = "APPENDED_txtfiles/%s_COUNT.txt" % symbol_dict[t][1]
    fout_count=open(append_initial_countfile,"w")
    fout_count.write(sum_sites)
    fout_count.write("\n")
    fout_count.write(dauer)
    fout_count.close()
    
        
    
def main_prediction():
    for t in tickers:
        print "In Bearbeitung: %s" % symbol_dict[t][1]
        global start_time
        start_time = datetime.now()
        company_result_set = {}
        ##########################################################
        #abhängig davon ob bereits geupdated wurde, muss das entsprechende _COUNT file 
        #geöffnet werden woraus wir die anzahl an bereits abgearbeiteten seiten erhalten
        ############################################################
        count_initial = "txtfiles/%s_COUNT.txt" % symbol_dict[t][1]
        count_updated = "UPDATE_txtfiles/%s_COUNT.txt" % symbol_dict[t][1]
        try:
            fin_sites = open(count_updated,"r")
            done_sites = (fin_sites.readline()).strip()
            done_sites = int(done_sites)
            fin_sites.close()
        except:
            fin_sites = open(count_initial,"r")
            done_sites = (fin_sites.readline()).strip()
            done_sites = int(done_sites)
            fin_sites.close()
        #############################################
        #initialer seitenaufruf --> die anzahl an seiten holen
        ############################################
        initial_cp_link = "http://www.boersen-zeitung.de/index.php?l=0&li=5&flag=research&quelle=dpa&ansicht=analyser&artikel=&isin=%s&page_number=0#jump" % (symbol_dict[t][0])
        #try:
        initial_html = urllib2.urlopen(initial_cp_link).read()
        time.sleep(1)
        #except:
        #    print "Fehler in main_prediction bei Unternehmen: %s" %t
        #    print "Link konnte nicht geöffnet werden"                        
        
      
        soup_initial = BeautifulSoup(initial_html)
      
        # aktuelle seitenzahl abfragen
            
        site_counter = get_site_count(soup_initial)

        # differenz bilden um herauszufinden wieviele neue seiten hinzu gekommen sind
        
        differenz = site_counter - done_sites
        
        # bis Differenz+1 iterieren! --> stop 
        # zusätzlich sum_sites übergeben die angibt wieviele seiten es nun gibt (für das COUNT txtfile)
        stop = differenz + 1
       
        if differenz >= 0 :
            parse_company(0,stop,t,company_result_set, site_counter)
        else:
            print "FEHLER! Differenz negativ bei %s" %t
            print "Abbruch des Update Vorgangs für %S" %t
        
        
##################################
#           START
#################################
#
tickers = symbol_dict.keys()
banks = bankhaus_dict.keys()
print "Ausfuehrung gestartet!"



main_prediction()


print "Ausfuehrung beendet"

  