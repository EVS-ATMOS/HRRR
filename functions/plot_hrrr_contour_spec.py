# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 16:10:08 2014

@author: mattjohnson
"""

def plot_hrrr_contour_spec(directory, parameter,datetimestart,datetimeend,hour,loc,plot_modelhours):
    """
    Creates a contour plot of a parameter over the hrrr files in a given directory at a specific location
    over a given time period at a set model hour or a series of model hours, 
    """
    import os
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import datetime

    if plot_modelhours:
        y = []
        for i in hour:
            string = 'hrrr.3d.'
            string = string+str(datetimestart.year)
            if datetimestart.month<10:
                string = string+'0'
            string = string+str(datetimestart.month)
            if datetimestart.day<10:
               string =string+'0'
            string = string+str(datetimestart.day)
            string = string +str(datetimestart.hour)+'00f0'
            if i<10:
                string = string+'0'
            string = string+str(i)+'.grib2'
            y.append(string)
                
            times = [datetime.datetime(datetimestart.year,datetimestart.month,datetimestart.day,datetimestart.hour+i) for i in hour]
    else:
        x = gather_hrrr_files(directory)
        y = np.array(x[0])
        y = y.transpose()
        y = y[hour]
    
        dates = x[1]
    
        if datetimestart == None != datetimeend:
            print 'error datetimestart and datetime end must both not be or both be none'
        elif datetimestart == None:
            startindex = 0
            endindex = len(dates)
        else:
            startindex = dates.index(datetimestart)
            endindex = dates.index(datetimeend) 
    
        y = y[startindex:endindex]
        times = []
        
    wkdir = os.getcwd()
    os.chdir(directory)
        
    values = []
        
    for i in range(len(y)):
        info = read_hrrr_spec(y[i], [parameter],loc = [-97.485,36.605], max = False)
        values.append(info[0][0])
        if not plot_modelhours:
            times.append(x[1][i])
            
            

    times = [(i-times[0]).total_seconds()/60/60 for i in times]
    times = np.array(times)
    
    hinp = np.array(info[2])
    
    values = np.array(values)
    
    units = info[-1]

    pc = plt.pcolormesh(times,hinp,values.transpose())
    
    plt.colorbar(mappable = pc)
        
    plt.xlabel('Time')
    plt.ylabel(info[1][0]+' '+units[0])
    
        
    os.chdir(wkdir)
    
    return
    