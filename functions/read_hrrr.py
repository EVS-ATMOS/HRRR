# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 13:33:41 2014

@author: mattjohnson
"""


import numpy as np
import os
import pygrib

def grb_to_grid(grb_obj):
    #from scollis
    """Takes a single grb object containing multiple
    levels. Assumes same time, pressure levels. Compiles to a cube"""
    n_levels = len(grb_obj)
    levels = np.array([grb_element['level'] for grb_element in grb_obj])
    indexes = np.argsort(levels)[::-1] # highest pressure first
    cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[1].values.shape[1]])
    for i in range(n_levels):
        cube[i,:,:] = grb_obj[indexes[i]].values
    cube_dict = {'data' : cube, 'units' : grb_obj[0]['units'],
                 'levels' : levels[indexes]}
    return cube_dict
    
def read_hrrr(filename, parameters = None,directory = os.getcwd(),max = False):
    
    """
    With an option for returning just the maximum values of a given list of parameters at each location, this function 
    takes in a filename, list of parameters (all parameters if left blank) and returns the ndarray of data, the list
    of parameters, list of heights in hPa, ndarray of locations and the list of units corresponding to each parameter
    in a list.  
    """
    wkdir = os.getcwd()
    os.chdir(directory)
        
    try:
        myfile = pygrib.open(filename) 
    except IOError:
        print 'file access error in pygrib.open'
        print os.getcwd()
        print filename
        return None
       
    if parameters != None:
        for i in range(len(parameters)):
            if parameters[i] == 'Total mixing ratio':
                continue
            x = HRRR_VARS.count(parameters[i])
            if x == 0:                    
                print 'requested parameter not in list'
                print parameters[i]  
                parameters.remove(parameters[i])
        parameterlist = parameters[:]
    else:
        parameterlist = HRRR_VARS
                
    data = []
    units = []
    
    for p in parameterlist:
        
        if p == 'Total mixing ratio':
            params = ['Cloud mixing ratio','Rain mixing ratio','Cloud Ice','Snow mixing ratio', 'Graupel (snow pellets)']
            mixdata = np.zeros(40)
            for j in params:
                grb = myfile.select(name = p)
                grb_cube = grb_to_grid(grb)
                mixdata = mixdata + grb_cube['data']
            if not max:
                data.append(mixdata)
            else:
                data.append(mixdata.max(axis=0))
            units.append(grb_cube['units'])
            continue

        grb = myfile.select(name = p)
        grb_cube = grb_to_grid(grb)
        if not max:
            data.append(grb_cube['data'])
        else:
            data.append(grb_cube['data'].max(axis=0))
        units.append(grb_cube['units'])
    
    myfile.close()

    if directory != None:
        os.chdir(wkdir)
    
    return [data,parameterlist,units]
    

    
    