# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 09:43:46 2014

@author: mattjohnson
"""


import os
import pygrib
import datetime


def read_hrrr_spec(filename, parameters = [''],directory = None,loc = [36.605,-97.485], no_txt = False, coords=None, max = False):   
    """
    With an option for returning just the maximum values of a given list of parameters at a specific location, this 
    function takes in a filename, list of parameters (all parameters if left blank) and returns the ndarray of data, 
    the list of parameters, list of heights in hPa, location in latitude, longitude and the list of units 
    corresponding to each parameter in a list.  
    """
    
    #look for a txt file option
    if not no_txt:
        date = datetime.datetime(int(filename[8:12]),int(filename[12:14]),int(filename[14:16]))
        modelh = int(filename[21:24])
    
        hour_spec = int(filename[16:18])
        
        
        [data,dates,parameterlist,loc,indexes,units] = read_hrrr_txt(date=date,hour=modelh,loc=loc,directory=directory,read_modelhours = False)
        times = [int((i-dates[0]).total_seconds()/(60*60)) for i in dates]
        if not (hour_spec in times):
            print 'hour'
            print hour_spec
            print 'for date'
            print date[0]
            print 'not present in txt file'
        elif parameters == ['']:
            return [data[hour_spec],parameterlist,loc,indexes,units]
        else:
            inds = []
            for i in parameters:
                inds.append(parameterlist.index(i))
            return [data[hour_spec][inds],parameterlist[inds],loc,indexes,units[inds]]
            

    if directory != None:
        wkdir = os.getcwd()
        os.chdir(directory)
        
    if not (filename in os.listdir(directory)):
        print filename
        print 'not in directory'
        return
    try:
        myfile = pygrib.open(filename)
    except IOError:
        return None
    
    parameterlist = ['Geopotential Height','Temperature','Relative humidity','Dew point temperature',
                'Specific humidity','Vertical velocity','U component of wind','V component of wind',
                'Absolute vorticity','Cloud mixing ratio','Cloud Ice','Rain mixing ratio','Snow mixing ratio',
                'Graupel (snow pellets)']  
                
    if parameters != ['']:
        for i in range(len(parameters)):
            if parameters[i] == 'Total mixing ratio':
                continue
            x = parameterlist.count(parameters[i])
            if x == 0:                    
                print 'requested parameter not in list'
                print parameters[i]  
        parameterlist = parameters[:]
            
    data = []
    units = []
        
    if coords == None:
        xyindex = convert_latlon2coords(loc)
        loc = convert_coords2latlon(xyindex)
    else:
        xyindex = coords
        loc = convert_coords2latlon(xyindex)
    
    for p in parameterlist:
        if p == 'Total mixing ratio':
            
            params = ['Cloud mixing ratio','Rain mixing ratio','Cloud Ice','Snow mixing ratio', 'Graupel (snow pellets)']
            mixdata = np.zeros(40)
            
            for j in params:
                
                grb = myfile.select(name = p)
                grb_cube = grb_to_grid(grb)
                
                if grb_cube == None:
                    return None
                    
                if not max:
                    q = grb_cube['data'].T[xyindex[1]][xyindex[0]][:] 
                else:
                    q = grb_cube['data'].T[xyindex[1]][xyindex[0]][:].max(axis=0)
            
                mixdata = mixdata + q
                
            data.append(mixdata)
            units.append(grb_cube['units'])
            continue
        
        try:
            grb = myfile.select(name = p)
        except ValueError:
            data.append(None)
            continue
        grb_cube = grb_to_grid(grb)
        if not max:
            data.append(grb_cube['data'].T[xyindex[1]][xyindex[0]][:])
        else:
            data.append(grb_cube['data'].T[xyindex[1]][xyindex[0]][:].max(axis=0))
        units.append(grb_cube['units'])
    
            
    myfile.close()
        
    if directory !=  None:
        os.chdir(wkdir)
            
    return [data,parameterlist,loc,xyindex,units]