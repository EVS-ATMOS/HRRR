# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 16:00:55 2014

@author: mattjohnson
"""


import numpy as np
import os
from scipy.io import netcdf

def compress_radartohrrr(radar_filename, sounding_filename, radar_directory=os.getcwd(), sounding_directory=os.getcwd(), output_directory = os.getcwd(),tsinds = None, hsinds = None, produce_file = False):
    """
    converts high resolution copol reflectivity into a matrix of reflectivities that correspond to the set of hrrr times
    and pressures for fair comparison, range in m, times in s, 
    """
    wkdir = os.getcwd()

    x = get_netcdf_variables(filename = radar_filename, directory = radar_directory,variablelist=
                                ['reflectivity_copol','range','time'])

    copol = x[0][0][0]    

    ran = x[0][0][1]

    times = x[0][0][2]
             
    [[sdata,sdim,sunits],sdate,f] = get_netcdf_variables(filename=sounding_filename,directory=sounding_directory,variablelist=['pres','alt'])
    

    #pres = np.interp(ran,sdata[1],sdata[0])
    
    hrrr_heights = np.interp(HRRR_PS[::-1],sdata[0][::-1],sdata[1][::-1])
    hrrr_heights = hrrr_heights[::-1]
    
    if tsinds == None and hsinds == None:
        [hsinds,tsinds] = calc_radar2hrrr_inds(times,ran,hrrr_heights)
    
    
    copol = np.array(copol)
    copol = 10**(copol/10)
    
    z = []
    y = []
    

    for i in range(len(tsinds)-1):
        for j in range(len(hsinds)-1):
            if hsinds[j] != hsinds[j+1] and tsinds[i] != tsinds[i+1]:
                temp = float(np.nanmean(np.nanmean(copol[tsinds[i]:tsinds[i+1],hsinds[j]:hsinds[j+1]],axis=1),axis=0))
                if temp == None or temp == []:
                    temp = np.nan
                y.append(temp)
        z.append(y)
        y = []
        
    z = np.array(z)
    
    z = 10*np.log10(z)
   
    indexes = np.where(z==np.nan)
    indexes = np.array(indexes)
    z = z.tolist()
    
    for i in range(indexes.shape[1]):
        z[indexes[0][i]][indexes[1][i]] = None
    
    
    if produce_file:
        os.chdir(output_directory)
        import json
        import datetime
        date = datetime.datetime(int(radar_filename[15:19]),int(radar_filename[19:21]),int(radar_filename[21:23]))
        filestring = produce_radar_txt_string(date)
        g = open(filestring,'w')
        u = [z,hrrr_heights.tolist(),tsinds,hsinds]
        json.dump(u,g)
        g.close()
        os.chdir(wkdir)
        x[-1].close()
        f.close()
        return [z,hrrr_heights,tsinds,hsinds]
        
    x[-1].close()
    f.close()

    return [z,hrrr_heights,tsinds,hsinds]
        
def calc_radar2hrrr_inds(times,radarh,hrrrhf):
    """
    works out indicies closest to each pressure level and hour and thus the matrices that need to be compressed to one value
    times in sec, pres in hPa
    """
    timesf = np.array(range(0,24))*60.*60.
    
    hhsave = []
    for i in range(len(hrrrhf.tolist())+1):
        if i == 0:
            hhsave.append(hrrrhf[0])
        elif i == len(hrrrhf.tolist()):
            hhsave.append(hrrrhf[-1])
        else:
            hhsave.append((hrrrhf[i-1]+hrrrhf[i])/2)

    hhsave = set(hhsave)
    radarset = set(radarh)
    hhtest = radarset.union(hhsave)
    hhtest = sorted(list(hhtest))
    hhsave = sorted(list(hhsave))
    
    hsinds = []
    for i in range(len(hhsave)):
        hsinds.append(hhtest.index(hhsave[i])-i)
            
    timesave = []
    for i in range(len(timesf)+1):
        if i == 0:
            timesave.append(timesf[0])
        elif i == len(timesf):
            timesave.append(timesf[-1])
        else:
            timesave.append((timesf[i-1]+timesf[i])/2)
            
    timestest = set(times)
    timestest = timestest.union(set(timesave))
    timestest = list(timestest)
    timesave = list(timesave)
    timestest = sorted(timestest)
    timesave = sorted(timesave)
    
    tsinds= []
    for i in range(len(timesave)):
        tsinds.append(timestest.index(timesave[i])-i)
        
    return [hsinds,tsinds]