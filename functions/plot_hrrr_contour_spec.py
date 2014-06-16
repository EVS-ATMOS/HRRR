# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 16:10:08 2014

@author: mattjohnson
"""

def plot_hrrr_contour_spec(directory, parameter,datetimestart,datetimeend,scaling = 1,final_unit = '',hour = 0,loc = [-97.485,36.605],plot_modelhours = False, vmin = None, vmax = None):
    """
    Creates a contour plot of a parameter over the hrrr files in a given directory at a specific location
    over a given time period at a set model hour or a series of model hours, 
    
    issues when crossing month boundary for modelhour plots
    """
    import os
    import numpy as np
    import matplotlib
    import matplotlib.dates
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
            
        times = []    
        x = matplotlib.dates.date2num(datetimestart)
        times = [matplotlib.dates.num2date(x+float(i)/24) for i in hour]
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
        

        
    values = []
        
    for i in range(len(y)):
        info = read_hrrr_spec(y[i], [parameter],directory = directory,loc = loc, max = False)
        values.append(info[0][0])
        if not plot_modelhours:
            times.append(x[1][i])
            
            
    times = [(i-times[0]).total_seconds()/60/60 for i in times]
    times = np.array(times)

    hinp = np.array(info[2])

    values = np.array(values)

    if final_unit == '':
        final_unit = info[-1]

    pc = plt.pcolormesh(times,hinp,values.transpose())
    
    ax = plt.gca()
    ax.set_ylim([0,max(hinp)])
    ax.set_xlim([0,max(times)])
    
    plt.colorbar(mappable = pc,label=parameter+' '+final_unit[0])
    plt.xlabel('Time in hrs')
    plt.ylabel('Height in hPa')

    return
    