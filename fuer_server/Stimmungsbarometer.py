# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import numpy as np
from matplotlib import dates
import calculate_data as calculate_data
import trefferquoten as tq

   

def main(cp,conn,cursor):    
    sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d ORDER BY `datum`" %(cp)
    
    sql4 = """SELECT neues_kursziel, zieldatum, analyst,neue_einstufung FROM prognose
     WHERE unternehmen = %d
     AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
     ORDER BY zieldatum""" %(cp)
     
     
    sql5 = """SELECT neue_einstufung,analyst FROM prognose
     WHERE unternehmen = %d
     AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
     ORDER BY zieldatum""" %(cp)
    
    
    
    trefferquoten_dict = tq.start_company(cp,conn,cursor)
    
    
    avg_kurse = calculate_data.get_select(sql,cursor,conn)
    prognose = calculate_data.get_select(sql4,cursor,conn)
    einstufung = calculate_data.get_select(sql5,cursor,conn)
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
    
