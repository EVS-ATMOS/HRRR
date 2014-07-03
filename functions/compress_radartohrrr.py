# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 16:00:55 2014

@author: mattjohnson
"""


import numpy as np

def compress_radartohrrr(radar_filename, sounding_filename, radar_directory, sounding_directory, tsinds = None, psinds = None):
    """
    converts high resolution copol reflectivity into a matrix of reflectivities that correspond to the set of hrrr times
    and pressures for fair comparison
    """
    print 'made to first function'
    copol = get_netcdf_variables(filename = radar_filename, directory = radar_directory,variablelist=
                                ['reflectivity_copol'])
    print 'get_netcdf finished'
    copol = copol[0][0]
    print 'got copol'
    ran = get_netcdf_variables(filename = radar_filename, directory = radar_directory,variablelist=
                                ['range'])
    ran = ran[0][0]
    print 'got ran'
    times = get_netcdf_variables(filename = radar_filename, directory = radar_directory,variablelist=
                                ['time'])
    times = times[0][0]
    
    print 'finished file1'              
    [[sdata,sdim,sunits],sdate] = get_netcdf_variables(filename=sounding_filename,directory=sounding_directory,variablelist=['pres','alt'])
    
    print 'finished files'      
                      
    pres = np.interp(ran,sdata[1],sdata[0])
    
    print 'finished interp'
    
    
    if tsinds == None and psinds == None:
        [psinds,tsinds] = calc_radar2hrrr_inds(times,pres)
    
    print 'finished calc inds'
    
    copol = np.array(copol)
    x = []
    y = []
    for i in range(len(tsinds)):
        for j in range(len(psinds)):
            y.append(np.mean(np.mean(copol[tsinds[i]+1:tsinds[i+1]][psinds[i]+1:psinds[i+1]],axis=1),axis=0))
        x.append(y)
        y = []
        
    return [x,tsinds,psinds]
        
def calc_radar2hrrr_inds(times,pres):
    """
    works out indicies closest to each pressure level and hour and thus the matrices that need to be compressed to one value
    """
    timesf = range(0,24)
    presf = np.log(HRRR_PS)
    pres = np.log(pres)
    
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
        
    return [psinds,tsinds]