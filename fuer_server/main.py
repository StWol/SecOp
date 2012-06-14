# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 20:02:38 2012

@author: Philipp
"""
from matplotlib import dates
import MySQLdb
import plot as plot
import prognose_nach_aktuellen_Analysten as prognose_nach_aktuellen_Analysten
import test_prognose_nach_aktuellen_Analysten as test_prognose_nach_aktuellen_Analysten
import prognose_nach_saemtlichen_prognosen_aller_Analysten_ab_2010 as prognose_nach_saemtlichen_prognosen_aller_Analysten_ab_2010
from pylab import figure
import calculate_data as calculate_data
import abweichungsschlauch_prognosen as abweichungsschlauch_prognosen
from random import randrange


def connect_to_DB():
    ####################################
    # datenbank connection herstellen
    ###################################
    try:
        conn = MySQLdb.connect (host="141.62.65.151",
                                user = "stan",
                                passwd = "money!",
                                db = "secop")
                          
        print "Mit secop verbunden"
                                
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    cursor = conn.cursor ()
    return [cursor,conn]

def get_prognose_nach_aktuellen_Analysten(cp,conn,cursor):
    ######################################################
    # Prognose nach aktuellen analysten
    ###################################################
    fig = figure()
    ax = fig.add_subplot(111)    
    
    result_set = prognose_nach_aktuellen_Analysten.main(cp,conn,cursor)    
    
    konfidenz_intervall_95_sigma_oben = result_set[0][0] 
    datum_konfidenz_intervall_95_sigma_oben = result_set[0][1]
    konfidenz_intervall_95_sigma_unten = result_set[1][0]
    datum_konfidenz_intervall_95_sigma_unten = result_set[1][1]
    datum_tats_kurse = result_set[2][0]
    tats_kurse = result_set[2][1]
    prognose_kurse_analysten = result_set[3][0]
    datum_prognosekurse_analysten = result_set[3][1]
    unsere_prognose_linie_kurse = result_set[4][0] 
    datum_unsere_prognose_linie = result_set[4][1]
    datum_unsere_prognose_punkte = result_set[5][0]
    unsere_prognose_punkte_kurse = result_set[5][1]
    sigma = result_set[6]
    print sigma

    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    plot.plot_future(prognose_kurse_analysten,datum_prognosekurse_analysten,'yellow',ax,fig)
    plot.plot_own_forecast_line(unsere_prognose_linie_kurse, datum_unsere_prognose_linie,sigma,ax,fig) 
    plot.plot_own_forecast_points(datum_unsere_prognose_punkte,unsere_prognose_punkte_kurse,ax,fig)   
    plot.show_plot(ax,fig)



def get_test_prognose_nach_aktuellen_Analysten(cp,conn,cursor):
    ######################################################
    # Test : Prognose nach aktuellen analysten
    ###################################################
    fig = figure()
    ax = fig.add_subplot(111)    
    
    result_set = test_prognose_nach_aktuellen_Analysten.main(cp,conn,cursor)    
    
    konfidenz_intervall_95_sigma_oben = result_set[0][0] 
    datum_konfidenz_intervall_95_sigma_oben = result_set[0][1]
    konfidenz_intervall_95_sigma_unten = result_set[1][0]
    datum_konfidenz_intervall_95_sigma_unten = result_set[1][1]
    datum_tats_kurse = result_set[2][0]
    tats_kurse = result_set[2][1]
    prognose_kurse_analysten = result_set[3][0]
    datum_prognosekurse_analysten = result_set[3][1]
    unsere_prognose_linie_kurse = result_set[4][0] 
    datum_unsere_prognose_linie = result_set[4][1]
    datum_unsere_prognose_punkte = result_set[5][0]
    unsere_prognose_punkte_kurse = result_set[5][1]
    standardabweichung = result_set[6]
    standardfehler = result_set[7]    
    
    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    plot.plot_future(prognose_kurse_analysten,datum_prognosekurse_analysten,'yellow',ax,fig)
    plot.plot_own_forecast_line(unsere_prognose_linie_kurse, datum_unsere_prognose_linie,standardabweichung,ax,fig) 
    plot.plot_own_forecast_points(datum_unsere_prognose_punkte,unsere_prognose_punkte_kurse,ax,fig)   
    plot.show_plot(ax,fig)

def get_prognose_nach_saemtlichen_prognosen_aller_Analysten_ab_2010(cp,conn,cursor):
    ######################################################
    # Prognose nach sämtlichen Analysten
    ###################################################
    fig = figure()
    ax = fig.add_subplot(111)
    
    result_set = prognose_nach_saemtlichen_prognosen_aller_Analysten_ab_2010.main(cp,conn,cursor)
    
    training_konfidenz_intervall_95_sigma_oben_kurse = result_set[0][0]
    training_konfidenz_intervall_95_sigma_oben_datum = result_set[0][1]
    training_konfidenz_intervall_95_sigma_unten_kurse = result_set[1][0] 
    training_konfidenz_intervall_95_sigma_unten_datum = result_set[1][1]
    
    testing_konfidenz_intervall_95_sigma_oben_kurse = result_set[2][0]
    testing_konfidenz_intervall_95_sigma_oben_datum = result_set[2][1]
    testing_konfidenz_intervall_95_sigma_unten_kurse = result_set[3][0]
    testing_konfidenz_intervall_95_sigma_unten_datum = result_set[3][1]
    
    prognose_konfidenz_intervall_95_sigma_oben_kurse = result_set[4][0]
    prognose_konfidenz_intervall_95_sigma_oben_datum = result_set[4][1]
    prognose_konfidenz_intervall_95_sigma_unten_kurse = result_set[5][0] 
    prognose_konfidenz_intervall_95_sigma_unten_datum = result_set[5][1]
    
    datum_tats_kurse = result_set[6][0]
    tats_kurse = result_set[6][1]
    
    prognose_kurse_analysten = result_set[7][0]
    datum_prognosekurse_analysten = result_set[7][1]
    
    training_unsere_vorhersage_linie_kurs = result_set[8][0]
    training_unsere_vorhersage_linie_datum = result_set[8][1]
    testing_unsere_vorhersage_linie_kurs = result_set[9][0]
    testing_unsere_vorhersage_linie_datum = result_set[9][1] 
    prognose_unsere_vorhersage_linie_kurs = result_set[10][0] 
    prognose_unsere_vorhersage_linie_datum = result_set[10][1] 
    
    konsistenz_sigma = result_set[11]
    validity_sigma = result_set[12]
    prognosis_sigma = result_set[13]
    
    
    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    plot.plot_own_forecast_line_2(training_unsere_vorhersage_linie_kurs,training_unsere_vorhersage_linie_datum ,konsistenz_sigma,'green',ax,fig) 
    plot.plot_own_forecast_line_2(testing_unsere_vorhersage_linie_kurs,testing_unsere_vorhersage_linie_datum ,validity_sigma,'yellow',ax,fig) 
    plot.plot_own_forecast_line_2(prognose_unsere_vorhersage_linie_kurs,prognose_unsere_vorhersage_linie_datum,prognosis_sigma,'red',ax,fig) 
    plot.plot_future(prognose_kurse_analysten,datum_prognosekurse_analysten,'yellow',ax,fig)
    plot.show_plot(ax,fig)
    

def get_abweichungsschlauch_prognosen(cp,conn,cursor):
    fig = figure()
    ax = fig.add_subplot(111)
    
    result_set = abweichungsschlauch_prognosen.main(cp,conn,cursor)
    analysten_dict = result_set[0]    
    analysten_prognosen_dict = result_set[1]
    tats_kurse = result_set[2][1]
    datum_tats_kurse = dates.num2date(result_set[2][0])
    
    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    
    for k,v in analysten_dict.iteritems():
        kurse = [q[0] for q in v]
        avgs = [q[1] for q in v]
        daten = [q[2] for q in v]
        #prepare_plotting(kurse, avgs, daten,analysten_prognosen_dict,k)
        #plot_analyst(kurse, avgs, daten)
        col_sig_list = plot.plot_analyst(kurse, avgs, daten,ax,fig) 
        color = col_sig_list[0]
        sigma = col_sig_list[1]
        if k in analysten_prognosen_dict.keys():    
            val = analysten_prognosen_dict[k]
            prognose_kurs=[] 
            prognose_datum = []
            for i in val:
                prognose_kurs.append(i[0])
                prognose_datum.append(i[1])
            analyst_prognose = [prognose_kurs,prognose_datum,color,sigma]
            plot.plot_future_2(prognose_kurs, prognose_datum,color,sigma,ax,fig)
    
    for k in analysten_prognosen_dict.keys():
        if k not in analysten_dict.keys():
            val = analysten_prognosen_dict[k]
            prognose_kurs=[] 
            prognose_datum = []
            color ='#%02X%02X%02X' % (randrange(0, 255), randrange(0, 255),randrange(0, 255))
            #sigma_prog = []
            for i in val:
                prognose_kurs.append(i[0])
                prognose_datum.append(i[1])
            plot.plot_future_unbekannt(prognose_kurs, prognose_datum,color,ax,fig)
    
    plot.show_plot(ax,fig)

      
#    data_for_plot_analyst = result_set[0]
#    data_for_individual_analysts = result_set[1]
#    data_for_future_unbekannt = result_set[2]
#    tats_kurse = result_set[3][1]
#    datum_tats_kurse = dates.num2date(result_set[3][0])
#    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)    
    
#    erg = []
#    for i in data_for_plot_analyst:
#        for z,j in zip(i[0],i[1]):
#            erg.append([j,z])
#        erg.sort()
#        plot.plot_analyst([q[1] for q in erg],[q[0] for q in erg],i[2],ax,fig)
#                    
#    plot.show_plot(ax,fig)       



def get_if_abweichungsschlauch_prognosen(cp,conn,cursor):
    fig = figure()
    ax = fig.add_subplot(111)
    
    result_set = abweichungsschlauch_prognosen.main(cp,conn,cursor)
    analysten_dict = result_set[0]    
    analysten_prognosen_dict = result_set[1]
    tats_kurse = result_set[2][1]
    datum_tats_kurse = dates.num2date(result_set[2][0])
    
    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    
    for k,v in analysten_dict.iteritems():
        kurse = [q[0] for q in v]
        avgs = [q[1] for q in v]
        daten = [q[2] for q in v]
        col_sig_list = plot.plot_analyst_if(kurse, avgs, daten,ax,fig) 
        color = col_sig_list[0]
        sigma = col_sig_list[1]
        plotted_or_not = col_sig_list[2]
        
        if plotted_or_not == 1:
            if k in analysten_prognosen_dict.keys():  
                val = analysten_prognosen_dict[k]
                prognose_kurs=[] 
                prognose_datum = []
                for i in val:
                    prognose_kurs.append(i[0])
                    prognose_datum.append(i[1])
                plot.plot_future_2(prognose_kurs, prognose_datum,color,sigma,ax,fig)
        else:
            continue

    plot.show_plot(ax,fig)


def just_do_it(cp):
    
    connector_result = connect_to_DB()
    cursor = connector_result[0]     
    conn = connector_result[1]

    get_prognose_nach_aktuellen_Analysten(cp,conn,cursor)
    get_test_prognose_nach_aktuellen_Analysten(cp,conn,cursor)
    get_prognose_nach_saemtlichen_prognosen_aller_Analysten_ab_2010(cp,conn,cursor)
    get_abweichungsschlauch_prognosen(cp,conn,cursor)
    get_if_abweichungsschlauch_prognosen(cp,conn,cursor)
    
    
just_do_it(101)
