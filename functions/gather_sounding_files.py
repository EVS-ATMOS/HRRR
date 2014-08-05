# -*- coding: utf-8 -*-


'''
This function calls the org_netcdf_files function (which organizes the files by date) and returns the file that matches with the date.
It is meant specifically for soundings and prints the file name for reference.

author: Grant Mckercher

'''
import datetime

def gather_sounding_files(date,directory,sound_num):


    [(dates_sound),(filename_sound)] = org_netcdf_files(directory)
    dates = [i.date() for i in dates_sound]
    index_sound = dates.index(date.date())
    
    index_sound_num = index_sound+(sound_num-1)
    
    
    print 'Reading',filename_sound[index_sound_num]
    
    return filename_sound[index_sound_num]