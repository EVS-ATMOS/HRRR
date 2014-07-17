# -*- coding: utf-8 -*-


'''
This function calls the org_sounding_files function (which organizes the files by date) and returns the first file by date. 

author: gmckercher
'''
import datetime

def gather_sounding_files(date,sound_dir):


    [dates_sound,filename_sound] = org_sounding_files(sound_dir)
    
    dates = [i.date for i in dates_sound]
    for i in dates:
        print str(i)
    index_sound = dates.index(date)

    return filename_sound[index_sound]
