# -*- coding: utf-8 -*-

'''
This function takes the disdrometer directories and organizes them by date. It returns the dates with the appropriate filename in a list. 

Authors: Grant McKercher & Matt Johnson
'''

import os
import datetime

def org_dis_files(dis_dir): 

    filename_dis = os.listdir(dis_dir)

    dates_dis = []
    
    index = 20
    for i in filename_dis:
      dates_dis.append(datetime.datetime(int(i[index:index+4]),int(i[(index+4):(index+6)]),int(i[(index+6):(index+8)])))   

    return [[dates_dis],[filename_dis]]
