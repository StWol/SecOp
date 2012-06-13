# -*- coding: utf-8 -*-
"""
Created on Wed May 16 07:53:13 2012

@author: Stan
"""

from valid_dictionaries import *
from db_connector import *

UPDATE_MODE = "update"
INIT_MODE = "init"

class Reader(object):
   
    
    def __init__(self, mode=INIT_MODE):
        if(mode == INIT_MODE):
            self.__cp_file = "txtfiles/%s.txt"
        else:
            self.__cp_file = "UPDATE_txtfiles/%s.txt"
            
        self.tickers = symbol_dict.keys()
        self.__analysten_list = self.__allAnalystFromTextAsDict()
        
    ###############################################
    def get_companyPredictionsAsList(self, cp_name):
        text_file = self.__cp_file % cp_name
        temp_list = []
        
        try:
                fin = open(text_file,"r")
                cp_raw = fin.readlines()
                fin.close()
                
                for row in cp_raw[1:]:
                    row_as_list = row.split(",",9)
                    try:
                        row_as_list[2] = int(row_as_list[2].strip())
                    except:
                        row_as_list[2] = -1
                    
                    try:
                        row_as_list[3] = float(row_as_list[3].strip())
                    except:
                        row_as_list[3]= -1
                        
                    try:
                        row_as_list[4] = float(row_as_list[4].strip())
                    except:
                        row_as_list[4]= -1
                        
                    try:
                        row_as_list[7] = float(row_as_list[7].strip())
                    except:
                        row_as_list[7]= -1
                    
                    row_as_list[8] = (row_as_list[8].replace('\'',"\\'")).strip()
                    
                    row_as_list[9] = (row_as_list[9].replace(',\n',"")).strip()            
                    temp_list.append(row_as_list)
                    
                
        except:
            print "FILE nicht da: %s" % text_file
            
        return temp_list
    
    ###############################################
    def __load_analystFromTextFile(self, cp_raw):
        
        temp_dict = []
        
        for i in range(1,len(cp_raw)):
            
            cp_list = cp_raw[i].split(",",9)
            
            key = cp_list[8].strip().replace('\'',"\\'")
            value = (cp_list[9].replace(',\n',"")).strip()
            
            temp_dict.append((key,value))
            
        return  temp_dict
    
    ###############################################
    def __allAnalystFromTextAsDict(self):
        temp_list = []
        for t in self.tickers:
            
            text_file = self.__cp_file % symbol_dict[t][1]
            
#            try:
            fin = open(text_file,"r")
            cp_raw = fin.readlines()
            fin.close()
            
            temp_dict = self.__load_analystFromTextFile(cp_raw)
            
            for i in temp_dict:
                temp_list.append((i[0],i[1]))
#            except:
#                print "FILE nicht da: %s" % text_file
    
        return set(temp_list)
        
    ###############################################     
    def get_analyseHaeuser(self):
        haeuser = []
        for haus in self.__analysten_list:
            haeuser.append(haus[1])
        return haeuser
        
    def get_analystenList(self):
        return self.__analysten_list


