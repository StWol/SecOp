# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import numpy as np
from matplotlib import dates
import calculate_data as calculate_data
import plot as plot
import MySQLdb

def main(cp,conn,cursor):  
    sql3 = """SELECT neues_kursziel, zieldatum, analyst, avg FROM analyst_avg_2 WHERE unternehmen = %d  AND avg_datum> '2010-01-01' AND avg_datum<(SELECT CURDATE()) ORDER BY avg_datum, zieldatum """%(cp)
    
    sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d ORDER BY `datum`"%(cp)
    
    sql4 = """SELECT neues_kursziel, zieldatum, analyst FROM prognose
     WHERE unternehmen = %d
     AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
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
    
    analysten_dict = calculate_data.get_analysten_dict(ziel_kurse)
    
    analysten_prognosen_dict = calculate_data.get_analysten_prognosen_dict(prognose)
    
    data_for_plot_analyst = calculate_data.get_data_for_plot_analyst(analysten_dict)
    data_for_individual_analysts = calculate_data.get_data_for_individual_analysts(analysten_dict,analysten_prognosen_dict)
    data_for_future_unbekannt = calculate_data.get_data_for_future_unbekannt(analysten_dict,analysten_prognosen_dict)
    tats_kurse_datum = [datum_avg,avg]
    
    result_set = []
    result_set.append(analysten_dict)
    result_set.append(analysten_prognosen_dict)
#    result_set.append(data_for_plot_analyst)
#    result_set.append(data_for_individual_analysts)
#    result_set.append(data_for_future_unbekannt)
    result_set.append(tats_kurse_datum)
    
    calculate_data.reset_global_variables()
    calculate_data.initialize_global_variables()
    
    return result_set
    
