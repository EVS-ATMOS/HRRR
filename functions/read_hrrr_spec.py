# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 09:43:46 2014

@author: mattjohnson
"""

import numpy as np
import os
import pygrib

def read_hrrr_spec(filename, parameters = [''],directory = None,loc = [36.605,-97.485], coords=None, max = False):   
    """
    With an option for returning just the maximum values of a given list of parameters at a specific location, this 
    function takes in a filename, list of parameters (all parameters if left blank) and returns the ndarray of data, 
    the list of parameters, list of heights in hPa, location in latitude, longitude and the list of units 
    corresponding to each parameter in a list.  
    """
    if directory != None:
        wkdir = os.getcwd()
        os.chdir(directory)
        
    myfile = pygrib.open(filename) 
    parameterlist = ['Geopotential Height','Temperature','Relative humidity','Dew point temperature',
            'Specific humidity','Vertical velocity','U component of wind','V component of wind',
            'Absolute vorticity','Cloud mixing ratio','Cloud Ice','Rain mixing ratio','Snow mixing ratio',
            'Graupel (snow pellets)']  
            
    if parameters != ['']:
        for i in range(len(parameters)):
            x = parameterlist.count(parameters[i])
            if x == 0:                    
                print 'requested parameter not in list'
                print parameters[i]  
        parameterlist = parameters[:]
        
    data = []
    grb = myfile.select(name = parameterlist[0]) 
    grb_cube = grb_to_grid(grb)
    dataloc =  np.array(grb[0].latlons())
    datah = grb_cube['levels']
    units = []
    
    if coords == None:
        xyindex = convert_latlon2coords(loc,dataloc)
        loc = convert_coords2latlon(xyindex,dataloc)
    else:
        xyindex = coords
        loc = convert_coords2latlon(xyindex,dataloc)

    for p in parameterlist:
        grb = myfile.select(name = p)
        grb_cube = grb_to_grid(grb)
        if not max:
            data.append(grb_cube['data'].T[xyindex[1]][xyindex[0]][:])
        else:
            data.append(grb_cube['data'].T[xyindex[1]][xyindex[0]][:].max(axis=0))
        units.append(grb_cube['units'])

        
    myfile.close()
    
    if directory !=  None:
        os.chdir(wkdir)
        
    return [data,parameterlist,datah,loc,xyindex,units]