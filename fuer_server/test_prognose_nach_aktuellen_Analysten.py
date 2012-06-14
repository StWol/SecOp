# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import numpy as np
from matplotlib import dates
import calculate_data as calculate_data
import plot as plot

def main(cp,conn,cursor):    
    sql3 = """SELECT neues_kursziel, zieldatum, analyst, avg FROM analyst_avg_2 WHERE unternehmen = %d AND neues_kursziel >0 AND avg_datum<'2012-01-01' ORDER BY avg_datum, zieldatum """%(cp)
    
    sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d ORDER BY `datum"%(cp)
    
    sql4 = """SELECT neues_kursziel, zieldatum, analyst FROM prognose
     WHERE unternehmen = %d
     AND `zieldatum`>'2012-01-01' AND `zieldatum`<(SELECT CURDATE()) AND neues_kursziel >0
     ORDER BY zieldatum"""%(cp)

    avg_kurse = calculate_data.get_select(sql,cursor,conn)
    ziel_kurse = calculate_data.get_select(sql3,cursor,conn)
    prognose = calculate_data.get_select(sql4,cursor,conn)
    
    avg = [q[0] for q in avg_kurse]
    
    datum_avg = [q[1] for q in avg_kurse]
    datum_avg =dates.date2num(datum_avg)
    
    datum_ziel = [q[1] for q in ziel_kurse]
    datum_ziel =dates.date2num(datum_ziel)
    
    datum_prognose = [q[1] for q in prognose]
    datum_prognose = dates.date2num(datum_prognose)
    
    analysten_list = [q[2] for q in ziel_kurse]
    
    
    
    analysten_dict = calculate_data.get_analysten_dict(ziel_kurse)
    
    analysten_prognosen_dict = calculate_data.get_analysten_prognosen_dict(prognose)
    
    predictions_dict = calculate_data.get_prediction_dictionary(analysten_dict,analysten_prognosen_dict)
    predictions_and_dates_list = calculate_data.get_predictions_and_dates(predictions_dict)
    mittelwert = calculate_data.get_mittelwert(predictions_and_dates_list)
    Varianz = calculate_data.get_varianz(mittelwert,[q[1] for q in predictions_and_dates_list])
    standardabweichung = np.sqrt(Varianz)
    
    data_plot_future = calculate_data.get_data_for_plot_future(analysten_dict,analysten_prognosen_dict)
    data_plot_own_forecast_ponts = calculate_data.get_data_for_plot_own_forecast_points()
#    fig = figure()
#    ax = fig.add_subplot(111)
#    plot.plot_avg(datum_avg,avg,ax,fig)
#    plot.plot_future([q[0] for q in data_plot_future], [q[1] for q in data_plot_future],'yellow',ax,fig)
#    plot.plot_own_forecast_line([q[1] for q in predictions_and_dates_list], [q[0] for q in predictions_and_dates_list],standardabweichung,ax,fig) 
#    plot.plot_own_forecast_points([q[0] for q in data_plot_own_forecast_ponts],[q[1] for q in data_plot_own_forecast_ponts],ax,fig)   
#    plot.show_plot(ax,fig)
    
    konfidenz_intervall_95_sigma_oben = [[(q[1]+ 1.9600 * standardabweichung) for q in predictions_and_dates_list], [dates.num2date(q[0]) for q in predictions_and_dates_list]]
    konfidenz_intervall_95_sigma_unten = [[(q[1]- 1.9600 * standardabweichung) for q in predictions_and_dates_list], [dates.num2date(q[0]) for q in predictions_and_dates_list]]
    tats_kurse_datum = [datum_avg,avg]
    prognosekurse_analysten_datum = [q[0] for q in data_plot_future], [dates.num2date(q[1]) for q in data_plot_future]
    unsere_vorhersage_linie = [q[1] for q in predictions_and_dates_list], [dates.num2date(q[0]) for q in predictions_and_dates_list]
    unsere_vorhersage_punkte = [[q[0] for q in data_plot_own_forecast_ponts],[dates.num2date(q[1]) for q in data_plot_own_forecast_ponts]]
    
    
    standardfehler = calculate_data.get_data_test_MSE(data_plot_own_forecast_ponts,avg_kurse)    
    standardfehler = calculate_data.get_sigma([q[0] for q in standardfehler],[q[1] for q in standardfehler])
    print standardfehler
    
    result_set = []
    result_set.append(konfidenz_intervall_95_sigma_oben)
    result_set.append(konfidenz_intervall_95_sigma_unten)
    result_set.append(tats_kurse_datum)
    result_set.append(prognosekurse_analysten_datum)
    result_set.append(unsere_vorhersage_linie)
    result_set.append(unsere_vorhersage_punkte)
    result_set.append(standardabweichung)
    result_set.append(standardfehler)
    
    
    calculate_data.reset_global_variables()
    
    return result_set

