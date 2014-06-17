# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 10:06:27 2014

@author: mattjohnson
"""
import os
import numpy as np

def find_hrrr_nonzerolocs(filename, parameter, directory = None):
    """
    """
    
    if directory != None:
        wkdir = os.getcwd()
        os.chdir(directory)
    
    [data,parameterlist,datah,dataloc,units] = read_hrrr(filename,[parameter], directory = directory)
    
    data = np.array(data)
    data = data[0]
    lats = dataloc[0]
    lons = dataloc[1]
    goodlocs = []
    
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                if data[i][j][k] > 0:
                    goodlocs.append((lats[j][k],lons[j][k]))
                    
    goodlocs = list(set(goodlocs))
                    
    if directory != None:
        os.chdir(wkdir)
                    
    return goodlocs
                    
    