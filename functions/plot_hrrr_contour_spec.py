# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 16:10:08 2014

@author: mattjohnson
"""

def plot_hrrr_contour_spec(directory, parameter,datetimestart=None,datetimeend=None,scaling = 1,final_unit = None,hour = 0,
                           loc = [-97.485,36.605],plot_modelhours = False, vmin = None, vmax = None):
    """
    Creates a contour plot of a parameter over the hrrr files in a given directory at a specific location
    over a given time period at a set model hour or a series of model hours, 
    
    issues when crossing month boundary for modelhour plots
    """
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
            startindex = dates.index(datetimestart)
            endindex = dates.index(datetimeend) 

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
    
        
    hinp = np.array(info[2])
    times = np.array(times)
    values = np.array(values)
    
    
    if final_unit == None:
        final_unit = info[-1]
    if type(final_unit) == list:
        final_unit = final_unit[0]
    u = []
    v = []
    
    for i in range(len(dates)):
        if i == 0 or dates[i].day-dates[i-1].day != 0:
            f = get_sun(dates[i],loc)
            u.append(f[0][0])
            v.append(f[0][1])
        
            
    count = 0
    print len(times)    
    print times
    plt.figure(figsize = [8,8])
    ax = plt.gca()
    
    pc = plt.pcolormesh(times,hinp,np.transpose(values))
    ax.set_ylim([0,max(hinp)])
    ax.set_xlim([0,max(times)])
    ax.invert_yaxis()
    plt.colorbar(mappable = pc,label=parameter+' '+final_unit)    
    plt.xlabel('Time in hrs')
    plt.ylabel('Height in hPa')
    
    yval = (max(hinp)+min(hinp))/2
    
    for i in range(len(u)):
        if u[i] != None and u[i]+24*i<max(times):
            ax.text(u[i]+24*i,yval, 'Sunrise')
            ax.axvline(u[i]+24*i, linestyle = '--', color='k')          
        if v[i] != None and v[i]+24*i<max(times):
            ax.axvline(v[i]+24*i, linestyle = '--', color='k')
            ax.text(v[i]+24*i,yval,'Sunset')
            

            
    

    plt.show()
    return   
    