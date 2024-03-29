# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import numpy as np
import calculate_data as calculate_data
from db_connector import Connector
  
connector = Connector()

def main(cp):
    sql3 = """SELECT `new_price`, `target_date`, `analyst_id`, `avg` 
            FROM analyst_avg_2  
            WHERE `company_id`= %d 
            AND `new_price`>0 
            AND `avg_date`<(SELECT CURDATE()) 
            ORDER BY `avg_date`, `target_date`"""%(cp)    
    
    sql = """SELECT `closing_price`, `date` 
            FROM secop_quote 
            WHERE `company_id`=%d 
            ORDER BY `date`"""%(cp)
    
    sql4 = """SELECT `new_price`, `target_date`, `analyst_id`
            FROM secop_prediction
            WHERE `company_id`= %d
            AND `target_date`>(SELECT CURDATE()) 
            AND `new_price`>0
            ORDER BY `target_date`"""%(cp)
    
    
    avg_kurse = connector.get_select(sql)
    ziel_kurse = connector.get_select(sql3)
    prognose = connector.get_select(sql4)
    
    avg = [q[0] for q in avg_kurse]
    
    datum_avg = [q[1] for q in avg_kurse]
    
    
    analysten_dict = calculate_data.get_analysten_dict(ziel_kurse)
    
    analysten_prognosen_dict = calculate_data.get_analysten_prognosen_dict(prognose)
    
    predictions_dict = calculate_data.get_prediction_dictionary(analysten_dict,analysten_prognosen_dict)
    predictions_and_dates_list = calculate_data.get_predictions_and_dates(predictions_dict)
    mittelwert = calculate_data.get_mittelwert(predictions_and_dates_list)
    Varianz = calculate_data.get_varianz(mittelwert,[q[1] for q in predictions_and_dates_list])
    sigma = np.sqrt(Varianz)
    
    
    data_plot_future = calculate_data.get_data_for_plot_future(analysten_dict,analysten_prognosen_dict)
    data_plot_own_forecast_ponts = calculate_data.get_data_for_plot_own_forecast_points()
    

    konfidenz_intervall_95_sigma_oben = [[(q[1]+ 1.9600 * sigma) for q in predictions_and_dates_list], [q[0] for q in predictions_and_dates_list]]
    konfidenz_intervall_95_sigma_unten = [[(q[1]- 1.9600 * sigma) for q in predictions_and_dates_list], [q[0] for q in predictions_and_dates_list]]
    tats_kurse_datum = [datum_avg,avg]
    prognosekurse_analysten_datum = [q[0] for q in data_plot_future], [q[1] for q in data_plot_future]
    unsere_vorhersage_linie = [q[1] for q in predictions_and_dates_list], [q[0] for q in predictions_and_dates_list]
    unsere_vorhersage_punkte = [[q[0] for q in data_plot_own_forecast_ponts],[q[1] for q in data_plot_own_forecast_ponts]]
    
    result_set = []
    result_set.append(konfidenz_intervall_95_sigma_oben)
    result_set.append(konfidenz_intervall_95_sigma_unten)
    result_set.append(tats_kurse_datum)
    result_set.append(prognosekurse_analysten_datum)
    result_set.append(unsere_vorhersage_linie)
    result_set.append(unsere_vorhersage_punkte)
    result_set.append(sigma)

    calculate_data.reset_global_variables()
    calculate_data.initialize_global_variables()
    return result_set
    