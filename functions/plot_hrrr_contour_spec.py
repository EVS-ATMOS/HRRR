# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 16:10:08 2014

@author: mattjohnson
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
    
def plot_hrrr_contour_spec(directory, parameter,datetimestart=None,datetimeend=None,scaling = 1,final_unit = None,hour = 0,
                           loc = [36.605,-97.485],plot_modelhours = False, figsize = [15,8],vmin = None, vmax = None):
    """
    Creates a contour plot of a parameter over the hrrr files in a given directory at a specific location
    over a given time period at a set model hour or a series of model hours, 
    
    issues when crossing month boundary for modelhour plots
    """
    

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
            string = string +str(datetimestart.hour)+'00f0'
            if i<10:
                string = string+'0'
            string = string+str(i)+'.grib2'
            y.append(string)
            
        times = []    
        x = matplotlib.dates.date2num(datetimestart)
        
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

    values = []
    count = 0
    
    for i in range(len(y)):
        if y[i] == None:
            times.remove(times[i])
            count = count+1
            continue
        info = read_hrrr_spec(y[i], [parameter],directory = directory,loc = loc, max = False)
        values.append(np.array(info[0][0])*float(scaling))
        #times.append(count)
        if not plot_modelhours:
            times.append(dates[i+startindex])
        count = count+1
        

    dates = times[:]        
    times = [((((times[i].year-times[0].year)*365)+(times[i].day-times[0].day)*24)+times[i].hour-times[0].hour) for i in range(len(times))]        
    
        
    hinp = HRRR_PS
    times.append(times[-1]+1)
    times = np.array(times)
    values = np.array(values)
    
    
    if final_unit == None:
        final_unit = info[-1]
    if type(final_unit) == list:
        final_unit = final_unit[0]
    u = []
    v = []

    dateset = np.unique(np.array([i.date() for i in dates])).tolist()
    dateset = [datetime.datetime(i.year,i.month,i.day) for i in dateset]
    
    if len(dateset)>1:
        dateset[len(dateset):] = dateset[0]-datetime.timedelta(days = 1)
        dateset[len(dateset):] = dateset[-1]+datetime.timedelta(days = 1)
    else:
        dateset = [dateset[0]-datetime.timedelta(days = 1),dateset[0],dateset[-1]+datetime.timedelta(days = 1)]

    
    for i in dateset:
        f = get_sun(i,loc = loc,no_dst = True)
        u.append(f[0][0])
        v.append(f[0][1])

        
            
    plt.figure(figsize = figsize)
    ax = plt.gca()
    
    ax.set_yscale('log')
    
    # x axis
    xmajorLocator = MultipleLocator(1)
    ax.xaxis.set_major_locator(xmajorLocator)
    xmajorFormatter = FormatStrFormatter('%d')
    ax.xaxis.set_major_formatter(xmajorFormatter)

    # y axis
    ymajorLocator = MultipleLocator(100)
    ax.yaxis.set_major_locator(ymajorLocator)
    ymajorFormatter = FormatStrFormatter('%d')
    ax.yaxis.set_major_formatter(ymajorFormatter)
    
    pc = plt.pcolormesh(times,hinp,np.transpose(values))
    ax.set_ylim([0,max(hinp)])
    ax.set_xlim([min(times),max(times)])
    ax.invert_yaxis()
    plt.colorbar(mappable = pc,label=parameter+' '+final_unit)    
    plt.xlabel('Time in hrs')
    plt.ylabel('Height in hPa')

    
    yval = (max(hinp)+min(hinp))/2
    
    for i in range(len(u)):
        if u[i] != None and u[i]+24*i<max(times) and u[i]+24*i>min(times):
            ax.text(u[i]+24*i,yval, 'Sunrise')
            ax.axvline(u[i]+24*i, linestyle = '--', color='k')          
        if v[i] != None and v[i]+24*i<max(times) and v[i]+24*i>min(times):
            ax.axvline(v[i]+24*i, linestyle = '--', color='k')
            ax.text(v[i]+24*i,yval,'Sunset')

    plt.show()
    return   
    