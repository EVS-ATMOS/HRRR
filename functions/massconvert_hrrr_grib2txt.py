# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 15:54:28 2014

@author: mattjohnson
"""
import numpy as np
import datetime

def massconvert_hrrr_grib2txt(startdate = None, enddate = None, modelstartindex = 0,directory = None, enddirectory = None, loc = [36.605, -97.485], indexes = None,modelhours = False):
    """
    converts hrrr files to txt day style->modelhours=False, combining the output at loc for each day for each hour into one .txt file
    model style-> combines the output from all files from the same date starting with the modelstartindex modelhour at that date and converts it into one
    .txt file
    """
    
    [filelists, datestrings] = gather_hrrr_files(directory)
    if startdate == None:
        index1 = 0
    else:
        index1 = datestrings.index(startdate)
        
    if enddate == None:
        index2 = len(datestrings)
    else:
        index2 = datestrings.index(enddate) 
        
        
        filelists = filelists[index1:index2]
        datestrings = datestrings[index1:index2]
        datestrings = [i.date() for i in datestrings]
        datestrings = np.unique(np.array(datestrings))
        datestrings = datestrings.tolist()
        datestrings = [datetime.datetime(i.year,i.month,i.day) for i in datestrings]
        
        
    if not modelhours:
        for i in datestrings:
            for j in range(len(filelists[0])):
                write_hrrr_grib2txt(i,hour = j,directory=directory,enddirectory=enddirectory,loc=loc, indexes = indexes,write_modelhours = modelhours)
                
    else:
        for i in datestrings:
            for j in range(len(filelists[0])):
                write_hrrr_grib2txt(i,hour = [modelstartindex,j],directory=directory,enddirectory=enddirectory,loc=loc, indexes = indexes,write_modelhours = modelhours)
    
    return