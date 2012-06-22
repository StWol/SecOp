# -*- coding: iso-8859-1 -*-
"""
Created on Thu May 10 11:53:09 2012

@author: Stan
"""
import urllib2, sys, datetime, time

from read_textfile import *
from valid_dictionaries import *
from db_connector import *

from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from secop.models import Index, Company, Quote, Bank, Analyst, Ranking, Prediction

reader = ''
######################################################################
###############         Init DB Connection        ####################
######################################################################


now = datetime.datetime.now()
y = now.year
m = now.month-1
d = now.day

indexDict = {}
rankingDict = {}
companyDict = {}
bankDict = {}
analystDict = {}
#####################################################################
#####################################################################
#####################################################################


################################################################################
###TEST#########################################################################
################################################################################

################################################################################
###END TEST ####################################################################
################################################################################


def get_dateFromString(stringDate):
    date_split = stringDate.split("-")
    return datetime.date(int(date_split[0]),int(date_split[1]),int(date_split[2]))
    

def einstufungenToDB(einstufungen):
    for i in einstufungen:
        new_object = Ranking(wert=i,slug=i.lower())
        
        try:
            new_object.save()
            rankingDict[new_object.wert] = new_object
        except:
            print "ERROR: Einstufung '%s' konnte nicht gespeichert werden" % new_object.wert
            continue

# alle Indizes in der DB speichern
###############################################
def indexToDB(indizes_list):
    for index in indizes_list:
        new_object = Index(index=index, slug=index.lower())
        try:
            new_object.save()
            indexDict[new_object.index] = new_object
        except:
            print "ERROR: Index %s konnte nicht gespeichert werden" % new_object.index
            continue

# alle Unternehmen in der DB speichern
###############################################
def companyToDB(company_dict):
    
    for key, value in company_dict.iteritems():
        
        new_object = Company(
            name=value[1], 
            kuerzel=key, 
            isin=value[0], 
            index=indexDict[value[2]], 
            slug=value[1].lower().replace("_","-"))
        
        try:
            new_object.save()
            companyDict[new_object.name] = new_object
            print "unternehmen %s eingefuegt" % key 
        except:
            print "Unexpected error: %s " %(sys.exc_info()[1])
        
# alle Kursdaten in der DB speichern
###############################################
def kursdatenToDB(symbol_dict):
    for kuerzel in symbol_dict.keys():
        company = symbol_dict[kuerzel][1]
        try:
            rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=01&c=2006&d=%s&e=%s&f=%s&g=d&ignore=.csv'%(kuerzel,m,d,y)).readlines()     
        except:
            print 'Fehler bei Link: %s' % company
            continue            
            
        for row in rows[1:]:
            row = row.split(',')
            datum = str(row[0])
            op = float(row[1])
            cl = float(row[4])
            vl = int(row[5])
            amount_ch = cl - op
            percent_ch = (amount_ch/op)*100
                  
            new_object = Quote(
                company = companyDict[company],
                date = get_dateFromString(datum),
                opening_price = op,
                closing_price = cl,
                volume = vl,
                amount_change = amount_ch,
                percent_change = percent_ch)
                
            try:
                new_object.save()
            except:
                print "Fehler bei insert: %s" % company 
                print sys.exc_info()[1]
                continue

        print "unternehmen %s eingefuegt mit %d zeilen" % (company, len(rows))
    upd = datetime.datetime.strftime(now,'%Y-%m-%d')
    upd = str(upd)
    version_string = "Stocks_Version/version.txt"
    fin_version = open(version_string,"w")
    version = fin_version.write(upd)
    fin_version.close() 
    


# alle Analystenhaeuser in die DB speichern
###############################################
def analystenhausToDB(haus_list):
    for haus in set(haus_list):
        
        
        new_object = Bank(name=haus, slug=haus.lower().replace("_","-"))
        try:
            new_object.save()
            bankDict[new_object.name] = new_object
        except : 
            #print "Error %d: %s" % (e.args[0], e.args[1])
            continue
    


# alle Analysten in die DB speichern
###############################################
def analystToDB(analyst_dict):

    for analyst_row in analyst_dict:
        analyst = analyst_row[0]
        haus = analyst_row[1]
        
        u_analyst = analyst.decode('iso-8859-1')
        
        new_object = Analyst(name=u_analyst, bank = bankDict[haus], slug=u_analyst.replace(" ","_")+ "-" + haus.lower())
        
        
        try:
            new_object.save()
            analystDict[new_object.slug] = new_object
            
        except:
            continue


# alle Vorhersagen in die DB speichern
###############################################
def allPredictionsToDB(company_list):
    predict_count = 0
    predict_count_all = 0
    for company in company_list:
         
        predict_count = __companyPredictionsToDB(company[1])
        
        predict_count_all += predict_count
        
        print "%d \t %s " % (predict_count,company[1])
        
    return predict_count_all

# alle Vorhersagen einer Firma in die DB speichern    
###############################################
def __companyPredictionsToDB(company):
    predcit_list = reader.get_companyPredictionsAsList(company)    
    
    for row in predcit_list:
        date = datetime.datetime.strptime(row[1],'%Y-%m-%d')
        zieldatum = date + relativedelta( months =+ int(row[2]) )
        
        u_analyst = row[8].decode('iso-8859-1')
        analyst_slug = u_analyst.replace(" ","_")+ "-" + row[9].lower()
        
        try:
            Analyst.objects.get(slug=analyst_slug)
        except:
            print analyst_slug
            
        ranking_old= row[6]
        if len(row[6]) == 0:
            ranking_old = None
        else:
            ranking_old = rankingDict[row[6]]
        
        new_object = Prediction(
            company = companyDict[company], 
            analyst = Analyst.objects.get(slug=analyst_slug),
            date = get_dateFromString(row[1]),
            target_date = zieldatum,
            time_frame = row[2],
            new_price = row[3],
            old_price = row[4],
            new_ranking = rankingDict[row[5]],
            old_ranking = ranking_old,
            publishing_price = row[7])
        
        try:
            new_object.save()
        except:
            continue
            
    return len (predcit_list)
    

# Fuer Initialisierung
def installDB():
    global reader 
    reader = Reader() 
    main()
    kursdatenToDB(symbol_dict)

# Fuer Update
def updateDB():
    global reader
    reader = Reader(mode="update") 
    
    for o in Index.objects.all():
        indexDict[o.index] = o

    for o in Ranking.objects.all():
        rankingDict[o.wert] = o
    
    for o in Company.objects.all():
        companyDict[o.name] = o
        
    for o in Bank.objects.all():
        bankDict[o.name] = o
    
    for o in Analyst.objects.all():
        analystDict[o.slug] = o
        
    main()
    kursdatenToDB(symbol_dict)
    
def main():
             
    #1. Einstuffungen
    einstufungenToDB(einstufungen)
    print "Einstuffungen gespeichert"
    
    #2. Indizes 
    indexToDB(indizes_dic.values())   
    print "insert %d indizies" % len( indexDict )
    
    #3. Analystenhaeuser
    analystenhausToDB(reader.get_analyseHaeuser())
    print "insert %d analystenhaeuser" % len( bankDict )
    
    #4. Analysten
    analystToDB(reader.get_analystenList())
    print "insert %d analyst" % len( analystDict )
    
    #5. Unternehmen
    companyToDB(symbol_dict)
    print "%d Unternehmen eingefügt" % len(companyDict)
    
    #6. Vorhersagen
    count = allPredictionsToDB(symbol_dict.values())
    print "%d Vorhersagen eingefügt" % count

t_start = time.time()
#installDB()
updateDB()

now_end = datetime.datetime.now()
zeit = relativedelta(now_end, now)
print "Dauer %dh %dm %d,%ds " % (zeit.hours,zeit.minutes, zeit.seconds, zeit.microseconds)


#reader = Reader() 

#analystToDB(reader.get_analystenList())
#einstufungenToDB(einstufungen)
#count = allPredictionsToDB(symbol_dict.values())

#anal = reader.get_analystenList()
#anal = reader.get_companyPredictionsAsList('SGL_Carbon')
#for a in anal :
#    if a[0] == "Analyst":
#        print a[1]

#for a in anal:
#    if a[0] == 'Markus Mayer' :
#            print a[1]
#analystenhausToDB(reader.get_analyseHaeuser())

#new_object = Analyst(name=u"ÜDfsÜ", bank = Bank.objects.get(pk=1), slug=u"äääßß".lower().replace("_","-")+ "-")
#print new_object
#new_object.save()