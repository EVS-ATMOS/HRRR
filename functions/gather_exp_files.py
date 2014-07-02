#! /usr/bin/env python


'''
This function calls the org_exp_files function (which organizes the files by date) and returns the first file by date. 

Authors: Grant McKercher & Matt Johnson
'''

def gather_exp_files(date,radar_dir,sound_dir,ceil_dir):


    [[dates_radar,dates_sound,dates_ceil],[filename_radar,filename_sound,filename_ceil]] = org_exp_files(radar_dir,sound_dir,ceil_dir)

    index_radar = dates_radar.index(date)
    index_sound = dates_sound.index(date)
    index_ceil = dates_ceil.index(date)

    return [filename_radar[index_radar],filename_sound[index_sound],filename_ceil[index_ceil]]

