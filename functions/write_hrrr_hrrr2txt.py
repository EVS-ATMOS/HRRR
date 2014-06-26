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

    [data,parameterlist,loc,indexes,units] = read_hrrr_spec(filename = filelists[0], directory = directory,loc=loc,no_txt = True,coords=indexes)
    print filelists[0]
    data = np.array(data)
    data = data.tolist()
    
    dates = []
    
    for i in range(len(filelists)-1):
        if filelists[i+1] in os.listdir(directory):
            x = read_hrrr_spec(filename = filelists[i+1], directory = directory,no_txt = True,coords=indexes)
            print filelists[i+1]
            if x == None:
                continue
            x[0] = np.array(x[0])
            x[0] = x[0].tolist()
            data.append(x[0])
            dates.append(matplotlib.dates.date2num(datestrings[i]))
    
    os.chdir(enddirectory)
    
    f = open(newfilename, 'w')
    
    json.dump([data,dates,parameterlist,loc,indexes,units],f)
    
    f.close()
    
    os.chdir(wkdir)
    
    return newfilename
    
    
    
    
    
    
    
    
    
    