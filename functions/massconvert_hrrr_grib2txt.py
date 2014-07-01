# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 15:54:28 2014

@author: mattjohnson
"""

import datetime

def massconvert_hrrr_grib2txt(startdate = None, enddate = None, hours = 0,modelstartindex = 0,directory = None, enddirectory = None, loc = [36.605, -97.485], indexes = None,modelhours = False):
    """
    converts hrrr files to txt day style->modelhours=False, combining the output at loc for each day for each hour into one .txt file
    model style-> combines the output from all files from the same date starting with the modelstartindex modelhour at that date and converts it into one
    .txt file
    """
    datestrings = [startdate+datetime.timedelta(days=i) for i in range((enddate-startdate).days)]
    hourslists = [hours for i in range(len(datestrings))]
    filelists = produce_hrrr_grib2strings(datestrings,hourslists)
    
    if startdate == None:
        index1 = 0
    else:
        index1 = datestrings.index(startdate)
        
    if enddate == None:
        index2 = len(datestrings)
    else:
        index2 = datestrings.index(enddate-datetime.timedelta(days=1)) 
        
        
        filelists = filelists[index1:index2]
        datestrings = datestrings[index1:index2]
        
        hours = range(min(hours),max(hours)+1)
        
    if not modelhours:
        
        for i in datestrings:
            for j in hours:
                name = write_hrrr_grib2txt(i,hour = j,directory=directory,enddirectory=enddirectory,loc=loc, indexes = indexes,write_modelhours = modelhours)
                print name
                
    else:
        for i in datestrings:
            for j in range(len(filelists[0])):
                name = write_hrrr_grib2txt(i,hour = [modelstartindex,j],directory=directory,enddirectory=enddirectory,loc=loc, indexes = indexes,write_modelhours = modelhours)
                print name
    
    return