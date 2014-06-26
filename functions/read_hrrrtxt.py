# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 14:51:59 2014

@author: mattjohnson
"""
import json
import datetime
import os
import matplotlib

def read_hrrr_txt(date=datetime.datetime.now(),hour=1,filenum = 24,directory=None,filename = None,loc=[36.605, -97.485],indexes=None, read_modelhours = False):
    """
    Reads txt files output by pyhrrr.write_hrrr_grib2txt()
    """
    if directory != None:
        wkdir = os.getcwd()
        os.chdir(directory)

    
    if ((type(hour) == list) and not read_modelhours):
        print 'error, can only read one model hour at a time if write_modelhours = False'
        return
        
    if filename != None:
        f = open(filename, 'r')
        [data,dates,parameterlist,loc,indexes,units] = json.load(f)
        return [data,matplotlib.dates.num2date(dates),parameterlist,loc,indexes,units]
        
    if indexes==None:
        indexes = convert_latlon2coords(loc)
    
    filename = produce_hrrr_txt_string(date=date,hour=hour,filenum = filenum,loc=loc,indexes =indexes,modelhours=read_modelhours)
    
    
    f = open(filename, 'r')
    [data,dates,parameterlist,loc,indexes,units] = json.load(f)
    
    if directory != None:
        os.chdir(wkdir)
    
    return [data,matplotlib.dates.num2date(dates),parameterlist,loc,indexes,units]