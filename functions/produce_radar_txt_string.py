# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 09:06:10 2014

@author: mattjohnson
"""

import datetime

def produce_radar_txt_string(date=datetime.datetime.now()):
    
    newfilename = 'radar.' + str(date.year)
    if date.month<10:
        newfilename = newfilename+'0'
    newfilename = newfilename + str(date.month)
    if date.day<10:
        newfilename = newfilename+'0'
    newfilename = newfilename + str(date.day)
    
    return newfilename
        
    