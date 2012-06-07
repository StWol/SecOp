# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:21:48 2012

@author: Philipp
"""
import datetime
import MySQLdb
import numpy as np
from pylab import figure, show
from matplotlib.dates import MONDAY, SATURDAY
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib import dates
import trefferquoten as tq
from random import randrange
import math

try:
    conn = MySQLdb.connect (host="141.62.65.151",
                            user = "stan",
                            passwd = "money!",
                            db = "secop")
                      
    print "Mit secop verbunden"
                            
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])

    
cursor = conn.cursor ()



def get_select(sql):
    result = []
    try:
        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchall()
        result = np.array(result)
        #result = np.transpose(result)
        return result
        
    except MySQLdb.Error, e:
        conn.rollback()
        print "Error %d: %s" % (e.args[0], e.args[1])
        


################################################################################        
def get_sigma(new_kurs,avg,datum_list):
    """The function to predict."""
    MSE = 0
    l = len(datum_list)
    for z,j in zip(new_kurs,avg):
        MSE = MSE + ((z-j)**2)
    MSE = MSE/l
    return np.sqrt(MSE)

################################################################################        
def prepare_plotting(kurse, avgs, daten,analysten_prognosen_dict,k):
    liste = plot_analyst(kurse, avgs, daten) 
    v = analysten_prognosen_dict[k]
    for k,v in analysten_prognosen_dict.iteritems():
        prognose_kurs = [q[0] for q in v]
        prognose_datum = [q[1] for q in v]
        
        plot_future(prognose_kurs, prognose_datum,liste)


def plot_future_unbekannt(prognose_kurs, prognose_datum,color):
    
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)
    


################################################################################    
def plot_future(prognose_kurs, prognose_datum,color):
    
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)

def plot_trend(prognose_datum,quote,last_kurs,color):
    trend = []
    print quote
    for i in range(0,len(prognose_datum)):
        trend.append(last_kurs)
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, trend, '-', color=color,linewidth=4 + (2 * quote/100))
    ax.hold(True)
    ax = fig.add_subplot(111)

    
################################################################################    
def plot_analyst(kurse, avg, daten,trefferquote):
    if trefferquote >= 0.7:
        color =  "#5DFC0A"
        #print trefferquote
    elif trefferquote >=0.3 <0.7:
        color = '#EEC900'
        #print trefferquote
    else:
        color = '#FF0000'
        #print trefferquote
     
    ax = fig.add_subplot(111)
    ax.plot_date(daten, kurse, 'o', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    #ax.plot_date(datum_avg,new_kurs -+ 1.9600 * sigma, '-')
    #ax.fill_between(datum_avg,datum_avg + 1.9600 * sigma, new_kurs - 1.9600 * sigma)
    #sigma = get_sigma(kurse,avg,daten)
    #print sigma
    #print len(kurse)
    #ax.fill_between(daten, kurse + 1.9600 * sigma, kurse - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)
    ax.hold(True)
    return color
   


cp=input("Für welches Unternehmen?\n")







sql = "SELECT close , `datum` FROM kursdaten WHERE unternehmen =%d " %(cp)

sql4 = """SELECT neues_kursziel, zieldatum, analyst,neue_einstufung FROM prognose
 WHERE unternehmen = %d
 AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
 ORDER BY zieldatum""" %(cp)
 
 
sql5 = """SELECT neue_einstufung,analyst FROM prognose
 WHERE unternehmen = %d
 AND `zieldatum`>(SELECT CURDATE()) AND neues_kursziel >0
 ORDER BY zieldatum""" %(cp)



trefferquoten_dict = tq.start_company()


avg_kurse = get_select(sql)
prognose = get_select(sql4)
einstufung = get_select(sql5)
avg = [q[0] for q in avg_kurse]

datum_avg = [q[1] for q in avg_kurse]
datum_avg =dates.date2num(datum_avg)


datum_prognose = [q[1] for q in prognose]
datum_prognose = dates.date2num(datum_prognose)

#avg_2 = [q[3] for q in ziel_kurse]

buy = 0
buy_clean = 0
neutral = 0
neutral_clean = 0
sell = 0
sell_clean = 0
tr_qt_buy = 1.
tr_qt_sell = 1.
tr_qt_neutral = 1.
gewicht_buy = 0
gewicht_sell = 0

print "=================="
print len(trefferquoten_dict[cp])
print "=================="
for i in einstufung:
    if i[0] == 1:
        buy = buy+1
        try:
            #if trefferquoten_dict[cp][i[1]][0]>5:            
                tr_qt_buy = tr_qt_buy * (trefferquoten_dict[cp][i[1]][2]+1)
                buy_clean = buy_clean+1
        except: 
            continue
    elif i[0] == 2:
        sell = sell+1
        try:
            #if trefferquoten_dict[cp][i[1]][0]>5:
                tr_qt_sell = tr_qt_sell * (trefferquoten_dict[cp][i[1]][2] +1)
                sell_clean = sell_clean +1
        except:
            continue
    elif i[0] == 3:
        neutral = neutral +1
        try:
            #if trefferquoten_dict[cp][i[1]][0]>5:
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

print "buy: ", buy
print "sell: " ,sell
print "neutral: " ,neutral
print 
print
print "%f Prozent aller Analysten sagen Buy!" %(prozent_buy)
print "Mittlere Trefferquote derer die Buy sagen: %f" %(t_q_buy)
print
print "%f Prozent aller Analysten sagen Sell!" %(prozent_sell)
print "Mittlere Trefferquote derer die Sell sagen: %f" %(t_q_sell)
print
print "%f Prozent aller Analysten sagen Neutral!" %(prozent_neutral)
print "Mittlere Trefferquote derer die Neutral sagen: %f" %(t_q_neutral)


analysten_dict ={}

analysten_prognosen_dict ={} 


for row in prognose:
    analysten_prognosen_dict[row[2]] = []


for row in prognose:  
    value = analysten_prognosen_dict[row[2]]
    value.append([row[0],dates.date2num(row[1]), row[3]])
    
print "------------------"
print "------------------"
#date1 = datetime.date( 2006, 1, 31 )
#date2 = datetime.date( 2012, 5, 21 )

months    = MonthLocator(range(1,13))
monthsFmt = DateFormatter("%b '%y")


fig = figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.hold(True)

#################################################################################
#### Die Schleife läuft jeden Analysten durch und ruft die methode zum zeichnen auf
##

mittel_buy = 0.
mittel_sell = 0.
mittel_neutral = 0.

count_buy = 0.
count_sell = 0.
count_neutral = 0.

for k in analysten_prognosen_dict.keys():
        val = analysten_prognosen_dict[k]
        
        prognose_buy = []
        prognose_sell = []
        prognose_neutral = []
        
        datum_buy = []
        datum_sell = []
        datum_neutral = []
        
        #sigma_prog = []
        for i in val:
            
            
            
            if i[2] == 1.:        
                color ='#00FF00'
                mittel_buy += i[0]
                count_buy += 1
                prognose_buy.append(i[0])
                datum_buy.append(i[1])
                
            elif i[2] == 2.:
                color ='#FF0000'
                mittel_sell += i[0]
                count_sell += 1
                prognose_sell.append(i[0])
                datum_sell.append(i[1])
                
            elif i[2]== 3.:
                color ='#FFFF00'
                mittel_neutral += i[0]
                count_neutral += 1
                prognose_neutral.append(i[0])
                datum_neutral.append(i[1])
                
                
                
        
         #   sigma_prog.append(1.)
        
        plot_future_unbekannt(prognose_buy, datum_buy,'#00FF00')
        plot_future_unbekannt(prognose_sell, datum_sell,'#FF0000')
        plot_future_unbekannt(prognose_neutral, datum_neutral,'#FFFF00')
        



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


#print buy
#print buy_clean
#print count_buy


print "====================="
print count_sell + count_neutral + count_buy
print "====================="
ax = fig.add_subplot(111)
ax.plot_date(datum_avg, avg,'-',color='black',label='tats. Kurs',linewidth=2)
ax.hold(True)

plot_trend(datum_prognose,t_q_neutral,mittel_neutral,'#FFFF00')
plot_trend(datum_prognose,t_q_buy,mittel_buy,'#00FF00')
plot_trend(datum_prognose,t_q_sell,mittel_sell,'#FF0000')




    
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.autoscale_view()    
ax.grid(True)
ax.legend(loc='upper left')
fig.autofmt_xdate()

show()
