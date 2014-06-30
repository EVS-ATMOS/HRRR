#! /usr/bin/env python

'''
This function takes the radar, sounding, and ceilometer directories and organizes them by date. It returns the dates with the appropriate filename in a list. 

Authors: Grant McKercher & Matt Johnson
'''

import os
import datetime


def org_exp_files(radar_dir,sound_dir,ceil_dir):

    wkdir = os.getcwd()  

    filename_radar = os.listdir(radar_dir)
    filename_sound = os.listdir(sound_dir)
    filename_ceil = os.listdir(ceil_dir)


    dates_radar = []
    dates_sound = []
    dates_ceil = []
    
    index = 15
    for i in filename_radar:
      dates_radar.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)]))    

    index = 18
    for i in filename_sound:
      dates_sound.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])) 

    index = 18
    for i in filename_ceil:
      dates_ceil+.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])) 

    return [[dates_radar,dates_sound,dates_ceil],[filename_radar,filename_sound,filename_ceil]]



#radar = 'sgpkazrgeC1.a1.20140527.000002.cdf'
#sounding = 'sgpsondewnpnC1.b1.20140527.052800.custom.cdf'
#ceilometer = 'sgpvceil25kC1.b1.20140527.000007.cdf'




