# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 19:59:51 2012

@author: Philipp
"""

import math
from sklearn import *
import MySQLdb
import numpy as np
from matplotlib import dates
from random import randrange
from db_connector import Connector


connector = Connector()

predictions_mittel_dict = {}
predictions_varianz_dict={}
training_predictions_and_dates_list = []
testing_predictions_and_dates_list = []
forecast_predictions_and_dates_list = []
clf = 0

def initialize_global_variables():
    global predictions_mittel_dict
    predictions_mittel_dict = {}
    global predictions_varianz_dict
    predictions_varianz_dict={}
    global training_predictions_and_dates_list
    training_predictions_and_dates_list = []
    global testing_predictions_and_dates_list
    testing_predictions_and_dates_list = []
    global forecast_predictions_and_dates_list
    forecast_predictions_and_dates_list = []
    global clf
    clf = 0

def reset_global_variables():
    global predictions_mittel_dict
    global predictions_varianz_dict
    global training_predictions_and_dates_list
    global testing_predictions_and_dates_list
    global forecast_predictions_and_dates_list
    global clf
    predictions_mittel_dict.clear()
    predictions_varianz_dict.clear()
    del training_predictions_and_dates_list
    del testing_predictions_and_dates_list
    del forecast_predictions_and_dates_list
    del clf

        
def get_varianz(mittel,prognosen):
    """The function to predict."""
    Varianz = 0
    for z in prognosen:
        Varianz = Varianz + ((z-mittel)**2)
    Varianz = Varianz/len(prognosen)
    return Varianz


def get_data_for_individual_analysts(analysten_dict,analysten_prognosen_dict):
    result = []    
    for k,v in analysten_dict.iteritems():
        kurse = [q[0] for q in v]
        avgs = [q[1] for q in v]
        sigma = get_sigma(kurse,avgs) 
        if k in analysten_prognosen_dict.keys():    
            val = analysten_prognosen_dict[k]
            for i in val:
                result.append([i[0],i[1],sigma])
    return result

def get_data_for_plot_analyst(analysten_dict):
    result = []    
    for k,v in analysten_dict.iteritems():
        kurse = [q[0] for q in v]
        avgs = [q[1] for q in v]
        daten = [q[2] for q in v]
        sigma = get_sigma(kurse,avgs)
        color ='#%02X%02X%02X' % (randrange(0, 255), randrange(0, 255),randrange(0, 255))
        result.append([kurse,daten,sigma,color])
    return result

def get_data_for_future_unbekannt(analysten_dict,analysten_prognosen_dict):
    result = [] 
    for k in analysten_prognosen_dict.keys():
        if k not in analysten_dict.keys():
            val = analysten_prognosen_dict[k]
            for i in val:
                result.append([i[0],i[1]])
    return result

def get_data_for_plot_future(analysten_dict,analysten_prognosen_dict):
    result = []    
    for k,v in analysten_dict.iteritems():
        if k in analysten_prognosen_dict.keys():    
            val = analysten_prognosen_dict[k]
            for i in val:
                result.append([i[0],i[1]])
    return result


def get_data_for_plot_own_forecast_points():
    global  predictions_mittel_dict   
    result = []    
    for k in predictions_mittel_dict.keys():
        result.append([k, predictions_mittel_dict[k]])
    return result


def get_prediction_dictionary(analysten_dict,analysten_prognosen_dict):
    ################################################################################
    ### Die Schleife läuft jeden Analysten durch und ruft die methode zum zeichnen auf
    c = 100.
    eps = 0.5    
    predictions_dict = {}
    for k,v in analysten_dict.iteritems():
        kurse = [q[0] for q in v]
        avgs = [q[1] for q in v]
        training_prognosen = np.array(kurse)
        training_prognosen=np.resize(training_prognosen,(len(training_prognosen),1))
        training_tats_kurse = np.array(avgs)
        ################################# SVR mit Parametern belegen und antrainieren
        clf = svm.SVR(C=c, epsilon=eps,kernel='rbf')
        clf = svm.SVR.fit(clf,training_prognosen,training_tats_kurse)
        if k in analysten_prognosen_dict.keys():    
            val = analysten_prognosen_dict[k]
            for i in val:
                if i[1] in predictions_dict:
                    predictions = svm.SVR.predict(clf,i[0])
                    predictions_dict[i[1]].append(predictions) 
                else:
                    predictions_dict[i[1]] = []
                    predictions = svm.SVR.predict(clf,i[0])
                    predictions_dict[i[1]].append(predictions)
    return predictions_dict



def get_analysten_dict(ziel_kurse):
    analysten_dict ={}    
    for row in ziel_kurse:
        analysten_dict[row[2]] = []
    
    for row in ziel_kurse:  
        value = analysten_dict[row[2]]
        value.append([row[0],row[3] ,dates.date2num(row[1])])
    return analysten_dict
    

def get_analysten_prognosen_dict(prognose):
    analysten_prognosen_dict ={} 
    for row in prognose:
        analysten_prognosen_dict[row[2]] = []
    for row in prognose:  
        value = analysten_prognosen_dict[row[2]]
        value.append([row[0],dates.date2num(row[1])])
    return analysten_prognosen_dict
    
def get_predictions_and_dates(predictions_dict):
    global predictions_mittel_dict
    global predictions_varianz_dict
    predictions_and_dates_list = []
    for k in predictions_dict.keys():
        mittel = 0
        count = 0
        prognosen = []
        predictions_varianz_dict[k] = []
        for i in predictions_dict[k]:
            mittel=mittel+i[0]
            count = count +1
            prognosen.append(i[0])
        mittel = mittel/count
        Varianz = get_varianz(mittel,prognosen)
        predictions_mittel_dict[k] = mittel
        std = math.sqrt(Varianz)
        predictions_varianz_dict[k] = [Varianz,std]
        predictions_and_dates_list.append([k,mittel])
    predictions_and_dates_list.sort()
    return predictions_and_dates_list
    
def get_mittelwert(liste):
    mittelwert = 0
    count = 0 
    for z in liste:
        mittelwert = mittelwert+z[1]
        count = count +1
    mittelwert = mittelwert/count
    return mittelwert

def get_mittelwert_2(liste):
    mittelwert = 0
    count = 0 
    for z in liste:
        mittelwert = mittelwert+z
        count = count +1
    mittelwert = mittelwert/count
    return mittelwert



def get_data_test_MSE(data_plot_own_forecast_ponts,avg_kurse):
    std_test =[]
    for i,j in zip([q[0] for q in data_plot_own_forecast_ponts],[q[1] for q in data_plot_own_forecast_ponts]):
        for z,x in zip(dates.date2num([q[1] for q in avg_kurse]),[q[0] for q in avg_kurse]):
            if i == z:
                std_test.append([j,x])
    return std_test
    
        
def get_sigma(new_kurs,avg):
    MSE = 0
    l = len(new_kurs)
    for z,j in zip(new_kurs,avg):
        MSE = MSE + ((z-j)**2)
    MSE = MSE/l
    return np.sqrt(MSE)
    
    

def train_machine(kurse_training):
    global training_predictions_and_dates_list
    training_predictions_and_dates_list = []
    for i in kurse_training:
        training_predictions_and_dates_list.append([dates.date2num(i[1]),i[2],i[0]])
    training_predictions_and_dates_list.sort()
    trainya = np.array([q[2] for q in training_predictions_and_dates_list])
    trainya=np.resize(trainya,(len(trainya),1))
    training_tats_kurse = np.array([q[1] for q in training_predictions_and_dates_list])
    global clf
    clf = 0
    c = 100.
    eps = 0.5
    clf = svm.SVR(C=c, epsilon=eps,kernel='rbf')
    clf = svm.SVR.fit(clf,trainya,training_tats_kurse)
    return trainya
    
def get_testing_data(kurse_testing):
    global testing_predictions_and_dates_list
    testing_predictions_and_dates_list = []
    for i in kurse_testing:
        testing_predictions_and_dates_list.append([dates.date2num(i[1]),i[3],i[0]])
    testing_predictions_and_dates_list.sort()
    testinya = np.array([q[2] for q in testing_predictions_and_dates_list])
    testinya=np.resize(testinya,(len(testinya),1))
    return testinya

def get_future_data(prognose):
    global forecast_predictions_and_dates_list 
    forecast_predictions_and_dates_list = []
    for i in prognose:
        forecast_predictions_and_dates_list.append([dates.date2num(i[1]),i[0]])
    
    forecast_predictions_and_dates_list.sort()
    prognose_kurs=np.array(forecast_predictions_and_dates_list)
    prognose_kurs=np.resize(prognose_kurs,(len(prognose_kurs),1))
    return prognose_kurs    
    
    
def predict_own(data):
    result = svm.SVR.predict(clf,data)
    return result
    

    
  
def get_buy_sell_neutral_count_percent_and_mittlere_trefferquoten(einstufung,trefferquoten_dict,cp):
    buy = 0
    buy_clean = 0
    neutral = 0
    neutral_clean = 0
    sell = 0
    sell_clean = 0
    tr_qt_buy = 1.
    tr_qt_sell = 1.
    tr_qt_neutral = 1.
    
    result = []
    
    for i in einstufung:
        if i[0] == 1:
            buy = buy+1
            try:
                if trefferquoten_dict[cp][i[1]][0]>3:            
                    tr_qt_buy = tr_qt_buy * (trefferquoten_dict[cp][i[1]][2]+1)
                    buy_clean = buy_clean+1
            except: 
                continue
        elif i[0] == 2:
            sell = sell+1
            try:
                if trefferquoten_dict[cp][i[1]][0]>3:
                    tr_qt_sell = tr_qt_sell * (trefferquoten_dict[cp][i[1]][2] +1)
                    sell_clean = sell_clean +1
            except:
                continue
        elif i[0] == 3:
            neutral = neutral +1
            try:
                if trefferquoten_dict[cp][i[1]][0]>3:
                    tr_qt_neutral = tr_qt_neutral * (trefferquoten_dict[cp][i[1]][2] +1)
                    neutral_clean = neutral_clean+1
            except:
                continue
    
    prozent_buy = (float(buy) / (buy + sell + neutral))*100
    prozent_sell = (float(sell) / (buy + sell + neutral))*100
    prozent_neutral = (float(neutral) / (buy + sell + neutral))*100
    
    try:
        t_q_buy = (((float(tr_qt_buy))**(1./buy_clean))-1)*100
    except:
        t_q_buy=0
    try:
        t_q_sell = (((float(tr_qt_sell))**(1./sell_clean))-1)*100
    except:
        t_q_sell=0
    try:
        t_q_neutral = (((float(tr_qt_neutral))**(1./neutral_clean))-1)*100
    except:
        t_q_neutral=0
        
    result.append([[buy,prozent_buy,t_q_buy],[sell,prozent_sell,t_q_sell],[neutral,prozent_neutral,t_q_neutral]])
    
    return result
    
    
def get_colored_trend_prognosis(analysten_prognosen_dict,datum_prognose):
    result = []    
    mittel_buy = 0.
    mittel_sell = 0.
    mittel_neutral = 0.
    count_buy = 0.
    count_sell = 0.
    count_neutral = 0. 
    prognose_buy = []
    prognose_sell = []
    prognose_neutral = []
    
    datum_buy = []
    datum_sell = []
    datum_neutral = []
    for k in analysten_prognosen_dict.keys():
        val = analysten_prognosen_dict[k]
        for i in val:
            if i[2] == 1.:        
                mittel_buy += i[0]
                count_buy += 1
                prognose_buy.append(i[0])
                datum_buy.append(i[1])
                
            elif i[2] == 2.:
                mittel_sell += i[0]
                count_sell += 1
                prognose_sell.append(i[0])
                datum_sell.append(i[1])
                
            elif i[2]== 3.:
                mittel_neutral += i[0]
                count_neutral += 1
                prognose_neutral.append(i[0])
                datum_neutral.append(i[1])
            else:
                continue
    try:
        mittel_neutral = float(mittel_neutral)/count_neutral
    except:
        mittel_neutral = 0
    try:
        mittel_sell = float(mittel_sell)/count_sell
    except:
        mittel_sell = 0
    try:
        mittel_buy = float(mittel_buy)/count_buy
    except:
        mittel_buy = 0
    
    arith_mittel_buy=[]
    arith_mittel_sell=[]
    arith_mittel_neutral=[]
    for i in range(0,len(datum_prognose)):
        arith_mittel_buy.append(mittel_buy) 
        arith_mittel_sell.append(mittel_sell)
        arith_mittel_neutral.append(mittel_neutral)

    result.append([[prognose_buy,dates.num2date(datum_buy)],[prognose_sell,dates.num2date(datum_sell)],[prognose_neutral,dates.num2date(datum_neutral)],[arith_mittel_buy,dates.num2date(datum_prognose)],[arith_mittel_sell,dates.num2date(datum_prognose)],[arith_mittel_neutral,dates.num2date(datum_prognose)]])                
    return result
    
    

    
    