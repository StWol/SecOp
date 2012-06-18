# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import numpy as np
from matplotlib import dates
import calculate_data as calculate_data
import trefferquoten as tq
from db_connector import Connector
  

connector = Connector()

def main(cp):    
    sql = """SELECT `closing_price`, `date` 
            FROM secop_quote 
            WHERE `company_id`=%d 
            ORDER BY `date`""" %(cp)
    
    sql4 = """SELECT `new_price`, `target_date`, `analyst_id`, `new_ranking_id` 
            FROM secop_prediction
            WHERE `company_id`= %d
            AND `target_date`>(SELECT CURDATE()) 
            AND `new_price` >0
            ORDER BY `target_date`""" %(cp)
     
     
    sql5 = """SELECT `new_ranking_id`,`analyst_id`
            FROM secop_prediction
            WHERE `company_id`= %d
            AND `target_date`>(SELECT CURDATE()) 
            AND `new_price`>0
            ORDER BY `target_date`""" %(cp)
    
    
    
    trefferquoten_dict = tq.start_company(cp)
    
    
    avg_kurse = connector.get_select(sql)
    prognose = connector.get_select(sql4)
    einstufung = connector.get_select(sql5)
    avg = [q[0] for q in avg_kurse]
    
    datum_avg = [q[1] for q in avg_kurse]
    datum_avg =dates.date2num(datum_avg)
    
    
    datum_prognose = [q[1] for q in prognose]
    datum_prognose = dates.date2num(datum_prognose)
    
    analysten_prognosen_dict ={} 
    
    
    for row in prognose:
        analysten_prognosen_dict[row[2]] = []
    
    
    for row in prognose:  
        value = analysten_prognosen_dict[row[2]]
        value.append([row[0],dates.date2num(row[1]), row[3]])    
    
    buy_sell_neutral_count_percent_and_mittlere_trefferquoten = calculate_data.get_buy_sell_neutral_count_percent_and_mittlere_trefferquoten(einstufung,trefferquoten_dict,cp)   
# [buy,prozent_buy,tr_qt_buy],[sell,prozent_sell,tr_qt_sell],[neutral,prozent_neutral,tr_qt_neutral]
    
    colored_trend_prognosis = calculate_data.get_colored_trend_prognosis(analysten_prognosen_dict,datum_prognose)
    tats_kurse_datum = [dates.num2date(datum_avg),avg]
     
    result_set = []
    result_set.append(tats_kurse_datum)
    result_set.append(buy_sell_neutral_count_percent_and_mittlere_trefferquoten)
    result_set.append(colored_trend_prognosis)
    
    return result_set
    
