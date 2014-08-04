# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 09:13:30 2014

@author: mattjohnson
"""
import os
import json
directory = '/home/mjohnson/python/hrrr_txt'


bads = []

for i in os.listdir(directory):
    f = open(i,'r')
    try:
        u = json.load(f)
    except ValueError:
        #os.remove(directory+'/'+i)
        bads.append(i)

print bads