# -*- coding: utf-8 -*-

'''
This function takes the radar directories and organizes them by date. It returns the dates with the appropriate filename in a list. 

Authors: Grant McKercher & Matt Johnson
'''

import os
import datetime

def org_radar_files(radar_dir): 

    filename_radar = os.listdir(radar_dir)

    dates_radar = []
    
    index = 15
    for i in filename_radar:
      dates_radar.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])))   

    return [[dates_radar],[filename_radar]]
