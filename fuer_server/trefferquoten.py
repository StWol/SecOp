# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
from db_connector import Connector
  
connector = Connector()


def get_Analyst_quote(treffer,gesamt):
    analysten_dict_gesamt ={}
    
    for row_gesamt in gesamt:
        analysten_dict_gesamt[row_gesamt[0]] = [row_gesamt[1],0]
    
    for row_treffer in treffer:
        if row_treffer[0] in analysten_dict_gesamt:
            analysten_dict_gesamt[row_treffer[0]][1] = row_treffer[1]
            #analysten_dict_gesamt[row_treffer[0]].append(row_treffer[1])
        else:
            print row_treffer[0]
    
    for r in analysten_dict_gesamt:
        gesamtzahl_prognosen =  analysten_dict_gesamt[r][0] 
        treffer_anzahl = float(analysten_dict_gesamt[r][1])
        quote = treffer_anzahl/gesamtzahl_prognosen
        analysten_dict_gesamt[r].append(quote)
    return analysten_dict_gesamt
        

def get_Company_quotes(treffer,gesamt,unternehmen_dict):
    unternehmen_id = unternehmen_dict.keys()
    unternehmen_dict_result = {}    
    for key in unternehmen_id:
        t = []
        g =[]
        for row in gesamt:
            if key == row[2]:
                g.append(row)
        for row_treffer in treffer:
            if key == row_treffer[2]:
                t.append(row_treffer)
        result = get_Analyst_quote(t,g) 
        unternehmen_dict_result[key] = result
    return unternehmen_dict_result
    



def start_analyst():
    ####################################################
    # Gesamt Trefferquoute der Analysten ermitteln
    ####################################################
    treffer = connector.get_select(sql)
    gesamt = connector.get_select(sql2)

    # trefferquote_nach_analyst_dict auf folgende form bringen:
    # {id_des_Analysten: [gesamtanzahl_an_Prognosen, treffer, trefferquote]}
    trefferquote_nach_analyst_dict = get_Analyst_quote(treffer,gesamt)
    return trefferquote_nach_analyst_dict
    #################################################################################
    ##################################################################################

def start_company(cp):
    ####################################################
    # Trefferquouten nach Unternehmen
    ####################################################
    treffer = connector.get_select(sql4)
    gesamt = connector.get_select(sql3)
    unternehmen = connector.get_select(sql5)

    unternehmen_dict ={}
    
    for row in unternehmen:
        unternehmen_dict[row[0]] = {}

    # trefferquote_nach_unternehmen_dict auf folgende form bringen:
    # {id_des_Unternehmens: {id_des_Analysten:[gesamtanzahl_an_Prognosen, treffer, trefferquote]}}
    trefferquote_nach_unternehmen_dict = get_Company_quotes(treffer,gesamt,unternehmen_dict)
    return trefferquote_nach_unternehmen_dict
    


### Analyst <-> anzahl richtiger Prognosen
sql = """SELECT `analyst_id`, COUNT(`analyst_id`) 
        FROM `analyst_avg_2`
        WHERE `publishing_price` > 0 
        AND `target_date` > '2010-01-01'
        AND((`new_ranking_id` = 1 AND (((avg -  `publishing_price`) /  `publishing_price` ) * 100) > 2)
        OR (`new_ranking_id` = 2 AND (((avg -  `publishing_price`) /  `publishing_price` ) * 100) < -2)
        OR (`new_ranking_id` = 3 AND (((avg -  `publishing_price`) /  `publishing_price` ) * 100) > -2 
        AND ((( avg - `publishing_price`) /  `publishing_price` ) * 100) < 2)) 
        GROUP BY  `analyst_id` """


#### Analyst <-> anzahl der Prognosen   
sql2 = """SELECT `analyst_id`, COUNT(*), `company_id` 
        FROM analyst_avg_2 
        WHERE `target_date` > '2010-01-01' 
        AND `publishing_price` > 0 
        GROUP BY `analyst_id`"""


sql3 ="""SELECT `analyst_id`,COUNT(*), `company_id` 
        FROM analyst_avg_2 
        WHERE `target_date` > '2010-01-01' 
        AND `publishing_price` > 0 
        GROUP BY `analyst_id`, `company_id`"""


sql4="""SELECT `analyst_id`, COUNT(`analyst_id`), `company_id`
        FROM `analyst_avg_2`
        WHERE `publishing_price`>0 
        AND `target_date` > '2010-01-01'
        AND((`new_ranking_id`= 1 AND (((avg -  `publishing_price`) /  `publishing_price` ) * 100) > 2)
        OR (`new_ranking_id`= 2 AND (((avg -  `publishing_price`) /  `publishing_price` ) * 100) < -2)
        OR (`new_ranking_id`= 3 AND (((avg -  `publishing_price`) /  `publishing_price` ) * 100) > -2 
        AND (((avg - `publishing_price`) /  `publishing_price` ) * 100) < 2)) 
        GROUP BY  `analyst_id`, `company_id`"""
        
        
sql5 ="""SELECT `company_id` 
        FROM `analyst_avg_2` 
        WHERE `target_date` > '2010-01-01' 
        AND `publishing_price`>0 
        GROUP BY `company_id`"""


####################################################
# Gesamt Trefferquoute der Analysten ermitteln
####################################################
#start_analyst()



####################################################
# Trefferquouten nach Unternehmen
####################################################
#erg = start_company()
