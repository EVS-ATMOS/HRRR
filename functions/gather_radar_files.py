# -*- coding: utf-8 -*-


'''
This function calls the org_radar_files function (which organizes the files by date) and returns the first file by date given. 

Authors: Grant McKercher & Matt Johnson
'''

def gather_radar_files(date,radar_dir):


    [[dates_radar],[filename_radar]] = org_radar_files(radar_dir)

    index_radar = dates_radar.index(date)

    return [filename_radar[index_radar]]

