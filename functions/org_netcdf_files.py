# -*- coding: utf-8 -*-

'''
This function takes files from a radar, sounding, ceilometer, or disdrometer directory and gives each of them a date (datetime object). 
<<<<<<< HEAD
It returns the files with the appropriate date in a list. 

Authors: Grant McKercher & Matt Johnson
=======
It returns the files with the appropriate date in an appropriate list form. 

Authors: Grant McKercher
>>>>>>> b4b42df7b84e5690c37f380fbb34549057eb4e4a
'''

import os
import datetime

def org_netcdf_files(directory): 

    filename = os.listdir(directory)
    
    # RADAR filename length is 34
    if (len(filename[0]) == 34):
      dates = []
      index = 15
      for i in filename:
        dates.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])))
      return [[dates],[filename]]
    
    # CEILOMETER filename length is 36
    elif (len(filename[0]) == 36):
      dates = []
      index = 17
      for i in filename:
        dates.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)]))) 
      return [[dates],[filename]]
    
    # SOUNDING filename length is 37
    elif (len(filename[0]) == 37): 
      dates = []
      index = 18
      for i in filename:
        dates.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)]),
                                             int(i[(index+9):(index+11)]),int(i[(index+11):(index+13)]))) 
      return [sorted(dates),sorted(filename)]
    
    # DISDROMETER filename length is 39
    elif (len(filename[0]) == 39): 
      dates = []
      index = 20
      for i in filename:
        dates.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])))   
      return [[dates],[filename]]