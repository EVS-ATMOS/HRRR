# -*- coding: utf-8 -*-

'''
This function calls the org_netcdf_files function (which organizes the files by date) and returns the file that matches with the date. 

Authors: Grant McKercher & Matt Johnson
'''

def gather_netcdf_files(date,directory):

    [[dates],[filename]] = org_netcdf_files(directory)
   
    index = dates.index(date)

    return [filename[index]]