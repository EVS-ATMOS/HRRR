# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 09:48:54 2014

@author: mattjohnson
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt



def plot_hrrr_dayfromtxt(parameter,date=datetime.datetime.now(), hour=1,hinp = None,directory=os.getcwd(),filename = None,loc=[36.605, -97.485],indexes=None,contour = False):
    
    
    [data,dates,parameterlist,loc,indexes,units] = read_hrrr_txt(date=date,hour=hour,directory=directory,filename = filename,loc=loc,indexes=indexes, read_modelhours = False)
    
    ind = parameterlist.index(parameter)
    data = data[:,ind]
    units = units[:,ind]
    
    times = [int((i-dates[0]).total_seconds()/(60*60)) for i in dates]
    times = np.array(times)
    
    
    if contour:
        from matplotlib.ticker import MultipleLocator, FormatStrFormatter
        
        values = np.array(data)
        
        if final_unit == None:
            final_unit = info[-1]
        if type(final_unit) == list:
            final_unit = final_unit[0]
        u = []
        v = []
    
        dateset = [date-datetime.timedelta(days=1),date,date+datetime.timedelta(days=1)]
    
        for i in dateset:
            f = get_sun(i,loc = loc,no_dst = True)
            u.append((f[1][0]-date).total_seconds()/(60*60))
            v.append((f[1][1]-date).total_seconds()/(60*60))
    
            
                
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
        
        pc = plt.pcolormesh(times,HRRR_PS,np.transpose(values))
        ax.set_ylim([0,max(HRRR_PS)])
        ax.set_xlim([min(times),max(times)])
        ax.invert_yaxis()
        plt.colorbar(mappable = pc,label=parameter+' '+final_unit)    
        plt.xlabel('Time in hrs')
        plt.ylabel('Pressure Level in hPa')
    
        
        yval = (max(HRRR_PS)+min(HRRR_PS))/2
        
        for i in range(len(u)):
            if u[i] != None and u[i]<max(times) and u[i]>min(times):
                ax.text(u[i],yval, 'Sunrise')
                ax.axvline(u[i], linestyle = '--', color='k')          
            if v[i] != None and v[i]<max(times) and v[i]>min(times):
                ax.axvline(v[i], linestyle = '--', color='k')
                ax.text(v[i],yval,'Sunset')
    
        plt.show()
        return
    else:
        if hinp == None:
            values = np.array(data[:])
            values = values.max(axis=1)
        else:
            pind = HRRR_PS.index(hinp)
            values = np.array(data[:,pind])
    
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