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
import Stimmungsbarometer as Stimmungsbarometer




def just_do_it(cp):
    
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

###############################################################################
# Stimmungsbarometer holen, auspacken und zeichnen
###############################################################################    
    Stimmungsbarometer.main(cp,conn,cursor)
    
    fig = figure()
    ax = fig.add_subplot(111)
    
    result_set_stimmung = Stimmungsbarometer.main(cp,conn,cursor)
    
    datum_tats_kurse = result_set_stimmung[0][0]
    tats_kurse = result_set_stimmung[0][1]
    
    
    anzahl_buy = result_set_stimmung[1][0][0][0]
    prozent_buy = result_set_stimmung[1][0][0][1]
    mittlere_trefferquote_buy = result_set_stimmung[1][0][0][2]
    
    anzahl_sell = result_set_stimmung[1][0][1][0]
    prozent_sell = result_set_stimmung[1][0][1][1]
    mittlere_trefferquote_sell = result_set_stimmung[1][0][1][2]
    
    anzahl_neutral = result_set_stimmung[1][0][2][0]
    prozent_neutral = result_set_stimmung[1][0][2][1]
    mittlere_trefferquote_neutral = result_set_stimmung[1][0][2][2]   
    
    
    print "buy: ", anzahl_buy
    print "sell: " ,anzahl_sell
    print "neutral: " ,anzahl_neutral
    print 
    print
    print "%f Prozent aller Analysten sagen Buy!" %(prozent_buy)
    print "Mittlere Trefferquote derer die Buy sagen: %f" %(mittlere_trefferquote_buy)
    print
    print "%f Prozent aller Analysten sagen Sell!" %(prozent_sell)
    print "Mittlere Trefferquote derer die Sell sagen: %f" %(mittlere_trefferquote_sell)
    print
    print "%f Prozent aller Analysten sagen Neutral!" %(prozent_neutral)
    print "Mittlere Trefferquote derer die Neutral sagen: %f" %(mittlere_trefferquote_neutral)
    
    prognose_punkte_buy =  result_set_stimmung[2][0][0][0]
    punkte_datum_buy = result_set_stimmung[2][0][0][1]
    
    prognose_punkte_sell =  result_set_stimmung[2][0][1][0]
    punkte_datum_sell = result_set_stimmung[2][0][1][1]
    
    prognose_punkte_neutral =  result_set_stimmung[2][0][2][0]
    punkte_datum_neutral = result_set_stimmung[2][0][2][1]
    
    mittelwertkurve_buy =  result_set_stimmung[2][0][3][0]
    mittelwertkurve_datum_buy = result_set_stimmung[2][0][3][1]
    
    mittelwertkurve_sell =  result_set_stimmung[2][0][4][0]
    mittelwertkurve_datum_sell = result_set_stimmung[2][0][4][1]
    
    mittelwertkurve_neutral =  result_set_stimmung[2][0][5][0]
    mittelwertkurve_datum_neutral = result_set_stimmung[2][0][5][1]
    
    
    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    plot.plot_future_unbekannt(prognose_punkte_buy, punkte_datum_buy,'#00FF00',ax,fig)
    plot.plot_future_unbekannt(prognose_punkte_sell, punkte_datum_sell,'#FF0000',ax,fig)
    plot.plot_future_unbekannt(prognose_punkte_neutral, punkte_datum_neutral,'#FFFF00',ax,fig)
    
    plot.plot_trend(mittelwertkurve_datum_buy,mittelwertkurve_buy,'#00FF00',ax,fig)
    plot.plot_trend(mittelwertkurve_datum_sell,mittelwertkurve_sell,'#FF0000',ax,fig)
    plot.plot_trend(mittelwertkurve_datum_neutral,mittelwertkurve_neutral,'#FFFF00',ax,fig)
    
    plot.show_plot(ax,fig)
    
    
    
    
###############################################################################
# Prognose nach aktuellen analysten holen, auspacken und zeichnen
###############################################################################  
    fig = figure()
    ax = fig.add_subplot(111)    
    
    result_set_prog_ind_analyst = prognose_nach_aktuellen_Analysten.main(cp,conn,cursor)    
    
    konfidenz_intervall_95_sigma_oben = result_set_prog_ind_analyst[0][0] 
    datum_konfidenz_intervall_95_sigma_oben = result_set_prog_ind_analyst[0][1]
    konfidenz_intervall_95_sigma_unten = result_set_prog_ind_analyst[1][0]
    datum_konfidenz_intervall_95_sigma_unten = result_set_prog_ind_analyst[1][1]
    datum_tats_kurse = result_set_prog_ind_analyst[2][0]
    tats_kurse = result_set_prog_ind_analyst[2][1]
    prognose_kurse_analysten = result_set_prog_ind_analyst[3][0]
    datum_prognosekurse_analysten = result_set_prog_ind_analyst[3][1]
    unsere_prognose_linie_kurse = result_set_prog_ind_analyst[4][0] 
    datum_unsere_prognose_linie = result_set_prog_ind_analyst[4][1]
    datum_unsere_prognose_punkte = result_set_prog_ind_analyst[5][0]
    unsere_prognose_punkte_kurse = result_set_prog_ind_analyst[5][1]
    sigma = result_set_prog_ind_analyst[6]
    print sigma

    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    plot.plot_future(prognose_kurse_analysten,datum_prognosekurse_analysten,'yellow',ax,fig)
    plot.plot_own_forecast_line(unsere_prognose_linie_kurse, datum_unsere_prognose_linie,sigma,ax,fig) 
    plot.plot_own_forecast_points(datum_unsere_prognose_punkte,unsere_prognose_punkte_kurse,ax,fig)   
    plot.show_plot(ax,fig)



######################################################
# Test : Prognose nach aktuellen analysten
###################################################
    fig = figure()
    ax = fig.add_subplot(111)    
    
    result_set_test_prog_ind_analyst = test_prognose_nach_aktuellen_Analysten.main(cp,conn,cursor)    
    
    konfidenz_intervall_95_sigma_oben = result_set_test_prog_ind_analyst[0][0] 
    datum_konfidenz_intervall_95_sigma_oben = result_set_test_prog_ind_analyst[0][1]
    konfidenz_intervall_95_sigma_unten = result_set_test_prog_ind_analyst[1][0]
    datum_konfidenz_intervall_95_sigma_unten = result_set_test_prog_ind_analyst[1][1]
    datum_tats_kurse = result_set_test_prog_ind_analyst[2][0]
    tats_kurse = result_set_test_prog_ind_analyst[2][1]
    prognose_kurse_analysten = result_set_test_prog_ind_analyst[3][0]
    datum_prognosekurse_analysten = result_set_test_prog_ind_analyst[3][1]
    unsere_prognose_linie_kurse = result_set_test_prog_ind_analyst[4][0] 
    datum_unsere_prognose_linie = result_set_test_prog_ind_analyst[4][1]
    datum_unsere_prognose_punkte = result_set_test_prog_ind_analyst[5][0]
    unsere_prognose_punkte_kurse = result_set_test_prog_ind_analyst[5][1]
    standardabweichung = result_set_test_prog_ind_analyst[6]
    standardfehler = result_set_test_prog_ind_analyst[7]    
    
    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    plot.plot_future(prognose_kurse_analysten,datum_prognosekurse_analysten,'yellow',ax,fig)
    plot.plot_own_forecast_line(unsere_prognose_linie_kurse, datum_unsere_prognose_linie,standardabweichung,ax,fig) 
    plot.plot_own_forecast_points(datum_unsere_prognose_punkte,unsere_prognose_punkte_kurse,ax,fig)   
    plot.show_plot(ax,fig)
    
    
    
    
######################################################
# Prognose nach sämtlichen Analysten
###################################################
    fig = figure()
    ax = fig.add_subplot(111)
    
    result_set_alle_analysten = prognose_nach_saemtlichen_prognosen_aller_Analysten_ab_2010.main(cp,conn,cursor)
    
    training_konfidenz_intervall_95_sigma_oben_kurse = result_set_alle_analysten[0][0]
    training_konfidenz_intervall_95_sigma_oben_datum = result_set_alle_analysten[0][1]
    training_konfidenz_intervall_95_sigma_unten_kurse = result_set_alle_analysten[1][0] 
    training_konfidenz_intervall_95_sigma_unten_datum = result_set_alle_analysten[1][1]
    
    testing_konfidenz_intervall_95_sigma_oben_kurse = result_set_alle_analysten[2][0]
    testing_konfidenz_intervall_95_sigma_oben_datum = result_set_alle_analysten[2][1]
    testing_konfidenz_intervall_95_sigma_unten_kurse = result_set_alle_analysten[3][0]
    testing_konfidenz_intervall_95_sigma_unten_datum = result_set_alle_analysten[3][1]
    
    prognose_konfidenz_intervall_95_sigma_oben_kurse = result_set_alle_analysten[4][0]
    prognose_konfidenz_intervall_95_sigma_oben_datum = result_set_alle_analysten[4][1]
    prognose_konfidenz_intervall_95_sigma_unten_kurse = result_set_alle_analysten[5][0] 
    prognose_konfidenz_intervall_95_sigma_unten_datum = result_set_alle_analysten[5][1]
    
    datum_tats_kurse = result_set_alle_analysten[6][0]
    tats_kurse = result_set_alle_analysten[6][1]
    
    prognose_kurse_analysten = result_set_alle_analysten[7][0]
    datum_prognosekurse_analysten = result_set_alle_analysten[7][1]
    
    training_unsere_vorhersage_linie_kurs = result_set_alle_analysten[8][0]
    training_unsere_vorhersage_linie_datum = result_set_alle_analysten[8][1]
    testing_unsere_vorhersage_linie_kurs = result_set_alle_analysten[9][0]
    testing_unsere_vorhersage_linie_datum = result_set_alle_analysten[9][1] 
    prognose_unsere_vorhersage_linie_kurs = result_set_alle_analysten[10][0] 
    prognose_unsere_vorhersage_linie_datum = result_set_alle_analysten[10][1] 
    
    konsistenz_sigma = result_set_alle_analysten[11]
    validity_sigma = result_set_alle_analysten[12]
    prognosis_sigma = result_set_alle_analysten[13]
    
    
    plot.plot_avg(datum_tats_kurse,tats_kurse,ax,fig)
    plot.plot_own_forecast_line_2(training_unsere_vorhersage_linie_kurs,training_unsere_vorhersage_linie_datum ,konsistenz_sigma,'green',ax,fig) 
    plot.plot_own_forecast_line_2(testing_unsere_vorhersage_linie_kurs,testing_unsere_vorhersage_linie_datum ,validity_sigma,'yellow',ax,fig) 
    plot.plot_own_forecast_line_2(prognose_unsere_vorhersage_linie_kurs,prognose_unsere_vorhersage_linie_datum,prognosis_sigma,'red',ax,fig) 
    plot.plot_future(prognose_kurse_analysten,datum_prognosekurse_analysten,'yellow',ax,fig)
    plot.show_plot(ax,fig)    
    
    
just_do_it(86)
