# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import numpy as np
from matplotlib import dates
import calculate_data as calculate_data
import plot as plot
from pylab import figure


def main(cp,conn,cursor):
    sql_training = """SELECT neues_kursziel, zieldatum,avg FROM analyst_avg_2 WHERE unternehmen = %d  AND avg_datum>'2010-01-01'AND avg_datum<'2012-03-01'"""%(cp)
    sql_testing = """SELECT neues_kursziel, zieldatum, analyst, avg FROM analyst_avg_2 WHERE unternehmen = %d  AND avg_datum>'2012-03-01' AND avg_datum<(SELECT CURDATE())"""%(cp)
    sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d ORDER BY `datum"%(cp)
    
    sql_prognose = """SELECT neues_kursziel, zieldatum FROM prognose
     WHERE unternehmen = %d
     AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
     """%(cp)
    
    
    #fig = figure()
    #ax = fig.add_subplot(111)    
    
    avg_kurse = calculate_data.get_select(sql,cursor,conn)
    kurse_training = calculate_data.get_select(sql_training,cursor,conn)
    kurse_testing = calculate_data.get_select(sql_testing,cursor,conn)
    prognose = calculate_data.get_select(sql_prognose,cursor,conn)
    
    avg = [q[0] for q in avg_kurse]
    datum_avg = [q[1] for q in avg_kurse]
    datum_avg =dates.date2num(datum_avg)
    trainya = calculate_data.train_machine(kurse_training)
    
    testinya = calculate_data.get_testing_data(kurse_testing)
    
        
    ###################################################
    #predict training and testing data --> consistency, validity
    ##################################################
    consistency = calculate_data.predict_own(trainya)
    testing_check = calculate_data.predict_own(testinya)
    
    
    sigma_training = calculate_data.get_sigma(consistency,[q[1] for q in calculate_data.training_predictions_and_dates_list])
    #print sigma_training
    #plot.plot_own_forecast_line_2(consistency, [q[0] for q in calculate_data.training_predictions_and_dates_list],sigma_training,'green',ax,fig) 
    konsitenz = [consistency, [q[0] for q in calculate_data.training_predictions_and_dates_list]]
    konsistenz_sigma = sigma_training
    
    sigma_testing = calculate_data.get_sigma(testing_check,[q[1] for q in calculate_data.testing_predictions_and_dates_list])
    #print sigma_testing
    #plot.plot_own_forecast_line_2(testing_check, [q[0] for q in calculate_data.testing_predictions_and_dates_list],sigma_testing,'yellow',ax,fig)
    validity = [testing_check, [q[0] for q in calculate_data.testing_predictions_and_dates_list]]
    validity_sigma = sigma_testing
    
    ################################# predict future
    prognose_kurs = calculate_data.get_future_data(prognose)
    predictions = calculate_data.predict_own(prognose_kurs)
    mittelwert = calculate_data.get_mittelwert_2(predictions)
    Varianz_prog = calculate_data.get_varianz(mittelwert,[q[1] for q in calculate_data.forecast_predictions_and_dates_list])
    sigma_prog = np.sqrt(Varianz_prog)
    #print sigma_prog
    #plot.plot_own_forecast_line_2(predictions, [q[0] for q in calculate_data.forecast_predictions_and_dates_list],sigma_prog,'red',ax,fig)
    prognosis = [predictions, [q[0] for q in calculate_data.forecast_predictions_and_dates_list]]
    prognosis_sigma = sigma_prog
    #plot analysten prognosen zum vergleich
    #plot.plot_future([q[1] for q in calculate_data.forecast_predictions_and_dates_list],[q[0] for q in calculate_data.forecast_predictions_and_dates_list],'yellow',ax,fig)
    #plot.plot_avg(datum_avg,avg,ax,fig)    
    #plot.show_plot(ax,fig)
    
    training_konfidenz_intervall_95_sigma_oben = [[(q+ 1.9600 * konsistenz_sigma) for q in consistency], [dates.num2date(q[0]) for q in calculate_data.training_predictions_and_dates_list]]
    training_konfidenz_intervall_95_sigma_unten = [[(q- 1.9600 * konsistenz_sigma) for q in consistency], [dates.num2date(q[0]) for q in calculate_data.training_predictions_and_dates_list]]
    testing_konfidenz_intervall_95_sigma_oben = [[(q+ 1.9600 * validity_sigma) for q in validity], [dates.num2date(q[0]) for q in calculate_data.testing_predictions_and_dates_list]]
    testing_konfidenz_intervall_95_sigma_unten = [[(q- 1.9600 * validity_sigma) for q in validity], [dates.num2date(q[0]) for q in calculate_data.testing_predictions_and_dates_list]] 
    prognose_konfidenz_intervall_95_sigma_oben = [[(q+ 1.9600 * prognosis_sigma) for q in prognosis], [dates.num2date(q[0]) for q in calculate_data.forecast_predictions_and_dates_list]]
    prognose_konfidenz_intervall_95_sigma_unten = [[(q- 1.9600 * prognosis_sigma) for q in prognosis], [dates.num2date(q[0]) for q in calculate_data.forecast_predictions_and_dates_list]] 
    tats_kurse_datum = [dates.num2date(datum_avg),avg]
    prognosekurse_analysten_datum = [[q[1] for q in calculate_data.forecast_predictions_and_dates_list],[dates.num2date(q[0]) for q in calculate_data.forecast_predictions_and_dates_list]]
    training_unsere_vorhersage_linie = [consistency, [dates.num2date(q[0]) for q in calculate_data.training_predictions_and_dates_list]]
    testing_unsere_vorhersage_linie = [testing_check, [dates.num2date(q[0]) for q in calculate_data.testing_predictions_and_dates_list]]
    prognose_unsere_vorhersage_linie = [predictions, [dates.num2date(q[0]) for q in calculate_data.forecast_predictions_and_dates_list]]    
    
    
    result_set = []
    result_set.append(training_konfidenz_intervall_95_sigma_oben)
    result_set.append(training_konfidenz_intervall_95_sigma_unten)
    result_set.append(testing_konfidenz_intervall_95_sigma_oben)
    result_set.append(testing_konfidenz_intervall_95_sigma_unten)
    result_set.append(prognose_konfidenz_intervall_95_sigma_oben)
    result_set.append(prognose_konfidenz_intervall_95_sigma_unten)
    result_set.append(tats_kurse_datum) 
    result_set.append(prognosekurse_analysten_datum)
    result_set.append(training_unsere_vorhersage_linie)
    result_set.append(testing_unsere_vorhersage_linie)
    result_set.append(prognose_unsere_vorhersage_linie)
    result_set.append(konsistenz_sigma)
    result_set.append(validity_sigma)
    result_set.append(prognosis_sigma)
    
    
    calculate_data.reset_global_variables()
    calculate_data.initialize_global_variables()
    
    return result_set
    