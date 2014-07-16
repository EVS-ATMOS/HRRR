# -*- coding: utf-8 -*-

'''
This function takes the sounding directories and organizes them by date. It returns the dates with the appropriate filename in a list. 

Author: Grant McKercher
'''

import os
import datetime

def org_sounding_files(sound_dir): 

    filename_sound = os.listdir(sound_dir)

    dates_sound = []

    index = 18
    for i in filename_sound:
      dates_sound.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)]),
                                           int(i[(index+9):(index+11)]),int(i[(index+11):(index+13)]))) 

    return [sorted(dates_sound),sorted(filename_sound)]