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
    wkdir = os.getcwd()
    os.chdir(directory)
    
    
    import datetime
    from scipy.io import netcdf
    
    f = netcdf.netcdf_file(filename, 'r')
    
    if variablelist == []:
        variablelist = f.variables
    
    date = datetime.datetime(int(filename[-19:-15]),int(filename[-15:-13]),int(filename[-13:-11]))

    data = []
    units = []
    dim = []
    
    for i in range(len(variablelist)):
        data.append(f.variables[variablelist[i]].data)
        units.append(f.variables[variablelist[i]].units)
        dim.append(f.variables[variablelist[i]].dimensions)

    x =[[data,dim,units],date]
    x = x[:][:][:][:][:]


    os.chdir(wkdir)


    return [[data,dim,units],date,f]