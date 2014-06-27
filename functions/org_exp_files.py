#! /usr/bin/env python

import os
import datetime


def org_exp_files(radar_dir,sounding_dir,ceilometer_dir):

    wkdir = os.getcwd()  

    filename_rad = os.listdir(radar_dir)
    filename_sound = os.listdir(sounding_dir)
    filename_ceil = os.listdir(ceilometer_dir)


    dates_radar = []
    dates_sounding = []
    dates_ceil = []
    
    index = 
    for i in filename_rad:
      dates_radar.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)]))    

    index = 
    for i in filename_sound:
      dates_sounding.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])) 

    index = 
    for i in filename_ceil:
      dates_ceil+.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])) 

    return [[dates_radar,dates_sounding,dates_ceil],[filename_rad,filename_sound,filename_ceil]]



#radar = 'sgpkazrgeC1.a1.20140527.000002.cdf'
#sounding = 'sgpsondewnpnC1.b1.20140527.052800.custom.cdf'
#ceilometer = 'sgpvceil25kC1.b1.20140527.000007.cdf'




