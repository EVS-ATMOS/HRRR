# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 14:51:46 2014

@author: mattjohnson
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime


def plot_hrrr_spec(parameter,datetimestart,datetimeend=None,directory = os.getcwd(),contour = False,plot_modelhours = False,scaling = 1,final_unit = None,hinp = None,hour=0,loc = [36.605,-97.485],figsize = [15,8],vmin = None, vmax = None):
    """
    Plots a given parameter over a given timespan for a given parameter, modelhour, height, location and directory of 
    HRRR files.  Leaving hinp empty will cause it to plot the maximum values over all heights.  
    
    Alternatively if plot_modelhours = True, it will graph the given parameter against time for the selcted model hours
    contained in hours.  
    """ 
    if ((type(hour) == list) and not plot_modelhours):
        print 'error, can only plot one model hour at a time if plot_modelhours = False'
        return
    
    if contour:
        return plot_hrrr_contour_spec(directory=directory,parameter=parameter,datetimestart = datetimestart,datetimeend=datetimeend,scaling = scaling,hour = hour,loc = loc,plot_modelhours = plot_modelhours,figsize = [15,8],final_unit = final_unit,vmin = vmin, vmax = vmax)
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
            
            times = []
            
            for i in hour:
                if datetimestart.hour+i<24:
                    times.append(datetime.datetime(datetimestart.year,datetimestart.month,datetimestart.day,datetimestart.hour+i))
                else:
                    times.append(datetime.datetime(datetimestart.year,datetimestart.month,datetimestart.day+1,datetimestart.hour+i-24))
            dates = times[:]
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
            startindex = dates.index(datetimestart)-hour
            endindex = dates.index(datetimeend)-hour
            if startindex<0:
                print 'missing early HRRR files'
                startindex = 0
            if endindex>len(dates)-1:
                print 'missing late HRRR files'
                endindex = len(dates)-1
                
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
                info = read_hrrr_spec(y[i], [parameter],loc = loc, max = False)
                index = info[2].tolist().index(hinp)
                datart = np.array(info[0])
                datarts = datart[index]*float(scaling)
            else:
                info = read_hrrr_spec(y[i], [parameter],loc = loc, max = True)
                datarts = np.array(info[0])*float(scaling)
        values.append(datarts)
        if not plot_modelhours:
            times.append(x[1][i+startindex])
    
    times = [((((times[i].year-times[0].year)*365)+(times[i].day-times[0].day)*24)+times[i].hour-times[0].hour) for i in range(len(times))]        
    
    if plot_modelhours:
        dates = times[:]
    
    
    if final_unit == None:
        final_unit = info[-1]
        
    if(type(final_unit) == list):
        final_unit = final_unit[0]
        
    times.append(times[-1]+1)
    times = np.array(times)
    values = np.array(values)
    
    u = []
    v = []
    dateset = np.unique(np.array([i.date() for i in dates])).tolist()
    dateset = [datetime.datetime(i.year,i.month,i.day) for i in dateset]
    
    dateset.insert(0,dateset[0]-datetime.timedelta(days = 1))
    dateset.append(dateset[-1]+datetime.timedelta(days = 1))

    
    for i in dateset:
        f = get_sun(i,loc = loc,no_dst = True)
        u.append((f[1][0]-datetimestart).total_seconds()/(60*60))
        v.append((f[1][1]-datetimestart).total_seconds()/(60*60))
        
            

    plt.figure(figsize =figsize)
    ax = plt.gca()

    plt.plot(times,values)
    ax.set_xlim([min(times),max(times)])
    plt.xlabel('Time hrs')
        
    plt.ylabel(parameter+' '+final_unit)

    
    yval = (max(values)+min(values))/2
  
    for i in range(len(u)):
        if u[i] != None and u[i]<max(times) and u[i]>min(times):
            ax.text(u[i],yval, 'Sunrise')
            ax.axvline(u[i], linestyle = '--', color='k')          
        if v[i] != None and v[i]<max(times) and v[i]>min(times):
            ax.axvline(v[i], linestyle = '--', color='k')
            ax.text(v[i],yval,'Sunset')
                   
    os.chdir(wkdir)
    
    return