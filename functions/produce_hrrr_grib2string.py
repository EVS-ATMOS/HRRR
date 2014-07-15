# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 10:17:53 2014

@author: mattjohnson
"""

import datetime

def produce_hrrr_grib2strings(dates,hourlists):
    """
    generates hrrr grib2 file names for the corresponding dates and model hours
    returned in a one dimensional array in order of date then order of model hour
    """
    filelist = []
    for i in range(len(dates)):
        for j in hourlists[i]:
            date = dates[i]-datetime.timedelta(hours=j)
            string = 'hrrr.3d.'+str(dates[i].year)
            if date.month<10:
                string = string+'0'
            string = string+str(date.month)
            if dates[i].day<10:
                string = string+'0'
            string = string+str(date.day)
            if dates[i].hour<10:
                string = string+'0'
            string = string+str(date.hour)
            string = string+'00f0'
            if j<10:
                string = string+'0'
            string = string+str(j)
            string = string+'.grib2'
            filelist.append(string)
    
    return filelist
    