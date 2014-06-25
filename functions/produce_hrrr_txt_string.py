# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 13:42:12 2014

@author: mattjohnson
"""
import datetime

def produce_hrrr_txt_string(date=datetime.datetime.now(),filenum = 24,hour = 0,loc=[36.605, -97.485], indexes = None,modelhours = False):
    """
    produce appropriate filenames for hrrr txt outputs in a unique and organized way
    """
    if ((type(hour) == list) and not modelhours):
        print 'error, can only write one model hour at a time if modelhours = False'
        return
        
    if not modelhours:
        wstr = 't'
        if date.hour<10:
            wstr = wstr+'0'
        wstr = wstr+'0'+str(date.hour)
        if date.hour+filenum<10:
            wstr = wstr+'0'
        wstr = wstr+'0'+str(date.hour+filenum)
        
        wstr = wstr+'r'
        if hour<10:
            wstr = wstr+'00'+str(hour)
        else:
            wstr = wstr+'0'+str(hour)
            
    else:                     
        wstr = 't'
        if date.hour<10:
            wstr = wstr+'0'
        wstr = wstr+'0'+str(date.hour)
        
        wstr = wstr+'m'
        if max(hour)<10:
            wstr = wstr+'0'
        wstr = wstr+'0'+str(min(hour))
        if min(hour)<10:
            wstr = wstr+'0'
        wstr = wstr+'0'+str(max(hour))
        
        
    newfilename = 'hrrr.3d.' + str(date.year)
    if date.month<10:
        newfilename = newfilename+'0'
    newfilename = newfilename + str(date.month)
    if date.day<10:
        newfilename = newfilename+'0'
    newfilename = newfilename + str(date.day)
    
    if indexes == None:
        indexes = convert_latlon2coords(loc)
        
    locstr = 'L'+str(indexes[0])+str(indexes[1])
    newfilename = newfilename+wstr+locstr+'.txt'
    
    return newfilename