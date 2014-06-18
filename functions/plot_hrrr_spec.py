# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 14:51:46 2014

@author: mattjohnson
"""
def plot_hrrr_spec(parameter,directory = os.getcwd(),datetimestart,datetimeend,contour = False,plot_modelhours = False,scaling = 1,final_unit = '',hinp = None,hour=0,loc = [-97.485,36.605],vmin = None, vmax = None):
    """
    Plots a given parameter over a given timespan for a given parameter, modelhour, height, location and directory of 
    HRRR files.  Leaving hinp empty will cause it to plot the maximum values over all heights.  
    
    Alternatively if plot_modelhours = True, it will graph the given parameter against time for the selcted model hours
    contained in hours.  
    """
    import numpy as np
    import matplotlib
    import os
    import matplotlib.pyplot as plt
    import datetime
    
    
    if contour:
        return plot_hrrr_contour_spec(directory=directory,parameter=parameter,datetimestart = datetimestart,datetimeend=datetimeend,scaling = scaling,hour = hour,loc = loc,plot_modelhours = plot_modelhours,vmin = vmin, vmax = vmax)
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

            if datetimestart.hour<10:
                string = string+'0'

            string = string +str(datetimestart.hour)

            string = string+'00f0'

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
            return
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
        if y[i] == None:
            continue
        else:
            if hinp != None:
                info = read_hrrr_spec(y[i], [parameter],loc = [-97.485,36.605], max = False)
                index = info[2].tolist().index(hinp)
                datart = np.array(info[0][0])
                datarts = datart[index]*float(scaling)
            else:
                info = read_hrrr_spec(y[i], [parameter],loc = [-97.485,36.605], max = True)
                datarts = np.array(info[0][0])*float(scaling)
        values.append(datarts)
        if not plot_modelhours:
            times.append(x[1][i])
            
    
    if final_unit == '':
        final_unit = info[-1]

    values = np.array(values)

    plt.plot(times,values)
    plt.xlabel('Time hrs')
    plt.ylabel(parameter+' '+final_unit[0])
    plt.tight_layout()
    
    
    os.chdir(wkdir)
    
    return