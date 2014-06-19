# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 15:06:35 2014

@author: mattjohnson
"""

import numpy as np



def find_hrrr_high_locs(filename,parameter,directory = None, minval = 0):
    """
    Returns a list of locations (lat,lon) at which values higher than minval were observed for the given
    parameter
    """
    [data,parameterlist,datah,dataloc,units] = read_hrrr(filename,[parameter], directory = directory)
    data = np.array(data)
    data = data[0]
    
    goodcoords = (data>minval).nonzero()
    
    lats = dataloc[0]
    lons = dataloc[1]
    
    goodlocs = []

    for i in range(len(goodcoords[0])):
        x = goodcoords[1][i]
        y = goodcoords[2][i]
        goodlocs.append((lats[x][y],lons[x][y]))
        
    goodlocs = list(set(goodlocs))
    
    return goodlocs
