# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 10:31:42 2014

@author: mattjohnson
"""

def convert_latlon2coords(loc, dataloc = HRRR_DATALOC):
    """
    finds coordinates of closest coordinates in dataloc to loc in (lat,lon)
    in (x,y)
    """
    x = abs(dataloc[0]-loc[0])
    y = abs(dataloc[1]-loc[1])
    xy = x+y
    xymin = min(xy.flatten())
    xy2 = xy.flatten().tolist()
    xyflatindex = xy2.index(xymin)
    [xsize,ysize] = dataloc[0].shape
    xyindex = [xyflatindex/ysize, xyflatindex%ysize]
    
    return xyindex
    
def convert_coords2latlon(coords,dataloc):
    """
    converts the coordinates to their (lat,lon) in dataloc
    """
    return (dataloc[0][coords[0]][coords[1]],dataloc[1][coords[0]][coords[1]])