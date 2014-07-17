# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 15:50:02 2014

@author: mattjohnson
"""
import os
import datetime

def mass_compress_radartohrrr(radar_ident, sounding_ident, ceil_ident, radar_namelength = None, sounding_namelength = None,ceil_namelength = None,radar_directory = os.getcwd(),sounding_directory = os.getcwd(),ceil_directory = os.getcwd(),output_directory = os.getcwd()):
    """
    converts radar and soundings into HRRR model format (minus the lowest two pressure levels) ident is the characters before the date in the filename
    """
    
    radar_dirlist = os.listdir(radar_directory)
    if radar_namelength != None:
        
        def suf_len(namelength):
            return radar_namelength == namelength
        
        radar_dirlist = filter(suf_len,radar_dirlist)
    radar_date = []
    for name in radar_dirlist:
        radar_date.append(datetime.datetime(int(name[radar_ident:radar_ident+4]),int(name[radar_ident+4:radar_ident+6]),int(name[radar_ident+6:radar_ident+8])))
        
        
    sounding_dirlist = os.listdir(sounding_directory)
    if sounding_namelength != None:
        
        def suf_len(namelength):
            return sounding_namelength == namelength
        
        sounding_dirlist = filter(suf_len,sounding_dirlist)
        
    sounding_date = []
    for name in sounding_dirlist:
        sounding_date.append(datetime.datetime(int(name[sounding_ident:sounding_ident+4]),int(name[sounding_ident+4:sounding_ident+6]),int(name[sounding_ident+6:sounding_ident+8])))
    
    ceil_dirlist = os.listdir(ceil_directory)
    if ceil_namelength != None:
        
        def suf_len(namelength):
            return ceil_namelength == namelength
        
        ceil_dirlist = filter(suf_len,ceil_dirlist)
        
    ceil_date = []
    for name in ceil_dirlist:
        ceil_date.append(datetime.datetime(int(name[ceil_ident:ceil_ident+4]),int(name[ceil_ident+4:ceil_ident+6]),int(name[ceil_ident+6:ceil_ident+8])))
        

    for i in range(len(radar_dirlist)):
        if i==0 or radar_date[i] != radar_date[i-1]:
            filestring = produce_radar_txt_string(radar_date[i])
            print 'making:'
            print filestring
            if not filestring in os.listdir(output_directory):
                j = sounding_date.index(radar_date[i])
                k = ceil_date.index(radar_date[i])
                compress_radartohrrr(radar_dirlist[i], sounding_dirlist[j], ceil_dirlist[k],radar_directory=radar_directory, sounding_directory=sounding_directory, ceil_directory=ceil_directory, output_directory = output_directory,tsinds = None, hsinds = None, produce_file = True)
                print 'finished:'
                print filestring
    
    return
       