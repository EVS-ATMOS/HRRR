# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 13:52:08 2014

@author: mattjohnson
"""

import numpy as np
import os
import json
import datetime
import matplotlib.dates


def write_hrrr_grib2txt(date=datetime.datetime.now(),filenum = 24,hour = 0,directory=os.getcwd(),enddirectory=os.getcwd(),loc=[36.605, -97.485], indexes = None,write_modelhours = False):
    """
    grabs the hrrr file corresponding to date and filenum-1 files after that for a given hour or the model predictions so many hours out at a specified time
    reads and compiles the data for a specific location and writes it to a json file
    """
    wkdir = os.getcwd()
    
    if ((type(hour) == list) and not write_modelhours):
        print 'error, can only write one model hour at a time if write_modelhours = False'
        return
    
    newfilename = produce_hrrr_txt_string(date=date,hour=hour,filenum=filenum,loc=loc,indexes =indexes,modelhours=write_modelhours)

    if newfilename in os.listdir(enddirectory):
        print 'error file already exists'
        return newfilename
    
    if not write_modelhours:
        
        datestrings = []
    
        for i in range(filenum):
            datestrings.append(datetime.datetime(date.year,date.month,date.day,date.hour+i)-datetime.timedelta(hours = hour))
            
        hourslists = [[hour] for i in range(filenum)]
        
               
    else:
        date = date-datetime.timedelta(hours=min(hour))
        filenum = hour[1]-hour[0]+1
        
        datestrings = [date]
        hourslists = [range(hour[0],hour[1]+1)]
        
    filelists = produce_hrrr_grib2strings(datestrings,hourslists)
    
    if filelists == []:
        return ''
        
    data = []

    
    dates = []
    k = -1
    
    for i in range(len(filelists)):
        if filelists[i] in os.listdir(directory):
            x = read_hrrr_spec(filename = filelists[i], directory = directory,no_txt = True,coords=indexes)
            print filelists[i]
            if x != None and i>k:
                k = len(filelists)+1
                parameterlist = x[1]
                loc = x[2]
                indexes = x[3]
                units = x[4]
            if x == None:
                continue
            x[0] = np.array(x[0])
            x[0] = x[0].tolist()
            data.append(x[0])
            x = None
            dates.append(matplotlib.dates.date2num(datestrings[i]))
            
    if not ('parameterlist' in vars().keys()):
        return
    
    os.chdir(enddirectory)
    
    f = open(newfilename, 'w')
    
    for i in range(len(data)):
        for j in data[i]:
            if type(j) == type(np.array([])):
                try:
                    data.pop(i)
                    dates.pop(i)
                except IndexError:
                    
    try:
        json.dump([data,dates,parameterlist,loc,indexes,units],f)
    except TypeError:
        print "array found in json export error -> pressure levels missing from some hour"
        return ''
        
    
    f.close()
    
    os.chdir(wkdir)
    
    return newfilename
    
    
    
    
    
    
    
    
    
    