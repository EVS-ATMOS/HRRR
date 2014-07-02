# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 16:00:55 2014

@author: mattjohnson
"""


import numpy as np

def compress_radartohrrr(filename, directory):
    """
    should break into two functions...one for working out the indexes another for the actual calculations
    """
    [[data,dim,units],date] = get_netcdf_variables(filename = 'sgpkazrgeC1.a1.20140419.000001.cdf', directory = '/Users/mattjohnson/',variablelist=
                                ['reflectivity_copol','range','time'])
                                
    #get pres from sounding
    #remove later
    pres = HRRR_PS
    
    copol = data[0]
    times = data[2]
    
    timesf = range(0,24)
    presf = HRRR_PS
    
    hpsave = []
    for i in range(len(presf.tolist())):
        if i == 0:
            hpsave.append(presf[0])
        elif i == len(presf.tolist())-1:
            hpsave.append(presf[-1])
        else:
            hpsave.append((presf[i]+presf[i+1])/2)
            
    pres = set(pres)
    prestest = pres.union(hpsave)
    prestest = list(prestest)
    
    hpsave = list(set(hpsave))
    psinds = []
    for i in hpsave:
        psinds.append(prestest.index(i))
        
    timesave = []
    for i in range(len(timesf)):
        if i == 0:
            timesave.append(timesf[0])
        elif i == len(timesf)-1:
            timesave.append(timesf[-1])
        else:
            timesave.append((timesf[i]+timesf[i+1])/2)
            
    timestest = set(times)
    timestest = timestest.union(set(timesave))
    tsinds= []
    for i in timesave:
        tsinds.append(timestest.index(i))
        
        
    copol = np.array(copol)
    x = []
    y = []
    for i in range(len(tsinds)):
        for j in range(len(psinds)):
            y.append(np.mean(np.mean(copol[tsinds[i]+1:tsinds[i+1]][psinds[i]+1:psinds[i+1]],axis=1),axis=0))
        x.append(y)
        y = []
        
    return [x,timesf,presf,tsinds,psinds]
        
        
        