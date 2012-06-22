# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 20:02:52 2012

@author: Philipp
"""
from pylab import figure, show
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib import dates
from random import randrange
import calculate_data as calculate_data


def prepare_plot():
    fig = figure()
    ax = fig.add_subplot(111)
    return ax

def show_plot(ax,fig):
    months    = MonthLocator(range(1,13),interval = 3)
    monthsFmt = DateFormatter("%b '%y")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.autoscale_view()    
    ax.grid(True)
    ax.legend(loc='upper left')
    fig.autofmt_xdate()
    show()

def plot_avg(datum_avg,avg,ax,fig):
    months    = MonthLocator(range(1,13),interval = 3)
    monthsFmt = DateFormatter("%b '%y")
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.hold(True)
    ax = fig.add_subplot(111)
    ax.plot_date(datum_avg, avg,'-',color='black',label='tats. Kurs',linewidth=2)
    ax.hold(True)


def plot_future(prognose_kurs, prognose_datum,color,ax,fig):
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)
    ax.hold(True)
    ax = fig.add_subplot(111)
    ax.hold(True)


def plot_future_2(prognose_kurs, prognose_datum,color,sigma,ax,fig):
    
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o-', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)

def plot_own_forecast_points(prognose_datum,prognose_kurs,ax,fig):
    color = 'green'    
    ax = fig.add_subplot(111)    
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)
    ax.hold(True)
    ax = fig.add_subplot(111)
    ax.hold(True)

def plot_own_forecast_line_2(predictions, prognose_datum,sigma,color,ax,fig):
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, predictions, '-', color=color,linewidth=1)

    ax.hold(True)
    ax = fig.add_subplot(111)
    ax.fill_between(prognose_datum, predictions + 1.9600 * sigma, predictions - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)



def plot_future_unbekannt(prognose_kurs, prognose_datum,color,ax,fig):
    
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, prognose_kurs, 'o', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
#    sigma = calculate_data.get_sigma(kurse,avg)
 #   ax.fill_between(prognose_datum, prognose_kurs + 1.9600 * sigma, prognose_kurs - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)

    ax.hold(True)



def plot_analyst(kurse, avg, daten,ax,fig):
    
    color ='#%02X%02X%02X' % (randrange(0, 255), randrange(0, 255),randrange(0, 255))
     
    ax = fig.add_subplot(111)
    ax.plot_date(daten, kurse, 'o-', color=color)

    ax.hold(True)
    ax = fig.add_subplot(111)
    sigma = calculate_data.get_sigma(kurse,avg)
    ax.fill_between(daten, kurse + 1.9600 * sigma, kurse - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)
    ax.hold(True)
    return [color,sigma]




def plot_analyst_if(kurse, avg, daten,ax,fig):
    
    color ='#%02X%02X%02X' % (randrange(0, 255), randrange(0, 255),randrange(0, 255))
    sigma = calculate_data.get_sigma(kurse,avg)
    if sigma < 10 and len(kurse)>2:
        ax = fig.add_subplot(111)
        ax.plot_date(daten, kurse, 'o-', color=color)
        ax.hold(True)
        ax = fig.add_subplot(111)
        ax.fill_between(daten, kurse + 1.9600 * sigma, kurse - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)
        ax.hold(True)
        return [color,sigma,1]
    else:
        return [color,sigma,0]


def plot_trend(prognose_datum,last_kurs,color,ax,fig):
    trend = []
    for i in range(0,len(prognose_datum)):
        trend.append(last_kurs)
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, trend, '-', color=color,linewidth=4 )
    ax.hold(True)
    ax = fig.add_subplot(111)


def plot_own_forecast_line(predictions, prognose_datum,sigma,ax,fig):
    color = 'green'
    ax = fig.add_subplot(111)
    ax.plot_date(prognose_datum, predictions, '-', color=color,linewidth=1)
    ax.hold(True)
    ax = fig.add_subplot(111)
    ax.fill_between(prognose_datum, predictions + 1.9600 * sigma, predictions - 1.9600 * sigma, alpha=0.35, linestyle='dashed' , color=color)
    ax.hold(True)