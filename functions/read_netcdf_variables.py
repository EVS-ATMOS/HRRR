# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 15:58:05 2014

@author: mattjohnson
"""


import os

def get_netcdf_variables(filename, variablelist = [], directory = os.getcwd()):
    """
    Accesses a specified netCDF file and recovers specified variables (if variablelist is empty will return all variables)
    returns a list of data arrays,  dimensions and units for each variable in a list with the date of the file.  
    """
    print 'made to function get'
    wkdir = os.getcwd()
    os.chdir(directory)
    
    print 'directories finished'
    
    import datetime
    from scipy.io import netcdf
    print 'imports finished'
    
    f = netcdf.netcdf_file(filename, 'r')
    print 'file accessed'
    
    if variablelist == []:
        variablelist = f.variables
    
    date = datetime.datetime(int(filename[-19:-15]),int(filename[-15:-13]),int(filename[-13:-11]))
    print 'date'
    data = []
    units = []
    dim = []
    
    for i in range(len(variablelist)):
        data.append(f.variables[variablelist[i]].data[:])
        units.append(f.variables[variablelist[i]].units[:])
        dim.append(f.variables[variablelist[i]].dimensions[:])
    print 'data gathered'
    f.close()
    print 'file closed'
    os.chdir(wkdir)
    
        
    return [[data,dim,units],date]