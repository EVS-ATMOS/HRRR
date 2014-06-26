# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 10:17:53 2014

@author: mattjohnson
"""


def produce_hrrr_grib2strings(dates,hourlists):
    """
    generates the hrrr grib2 file name for the corresponding dates and model hours
    """
    filelist = []
    for i in dates:
        for j in hourlists[i]:
            string = 'hrrr.3d.'+str(i.year)
            if i.month<10:
                string = string+'0'
            string = string+str(i.month)
            if i.day<10:
                string = string+'0'
            string = string+str(i.day)
            if i.hour<10:
                string = string+'0'
            string = string+str(i.hour)
            string = string+'00f0'
            if j<10:
                string = string+'0'
            string = string+str(j)
            string = string+'.grib2'
            filelist.append(string)
    
    return filelist
    