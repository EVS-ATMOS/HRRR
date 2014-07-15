# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 10:00:36 2014

@author: mattjohnson
"""
import datetime
import pyhrrr
import json
import os
import matplotlib.dates
import numpy as np

dates = [datetime.datetime(2014,3,15)+datetime.timedelta(i) for i in range(100)]
baddates = []

for i in baddates:
    dates.remove(i)
    
wkdir = os.getcwd()
radar_directory = '/home/mjohnson/python/radar_txt'
hrrr_directory = '/home/mjohnson/python/hrrr_txt'
output_directory = '/home/mjohnson/python/'

radar_strings = [pyhrrr.produce_radar_txt_string(i) for i in dates]
hrrr_strings = [pyhrrr.produce_hrrr_txt_string(i,filenum = 24,hour = 1,loc=[36.605, -97.485], indexes = None,modelhours = False) for i in dates]

radarfiles = os.listdir(radar_directory)
hrrrfiles = os.listdir(hrrr_directory)

hour = 1

radar_margin = -10 #dBz
hrrr_margin = .1 #kg/kg
c_fracts_hrrr = []
c_fracts_radar = []
hrrr_hoursets = []

for i in range(len(dates)):
    if (radar_strings[i] in radarfiles) and (hrrr_strings[i] in hrrrfiles):
        
        os.chdir(hrrr_directory)
        hrrrf = open(hrrr_strings[i],'r')
        
        hrrr = json.load(hrrrf)
        
        #hrrr analysis
        datetimes = matplotlib.dates.num2date(hrrr[1])
        timeshift = datetime.timedelta(hours=hour)
        hrrr_hours = [(i+timeshift).hour for i in datetimes]
            
        ind = hrrr[2].index('Cloud mixing ratio')
        hrrr_data = hrrr[0]
        hrrr_data = np.array(hrrr_data)
        hrrr_c = hrrr_data[:,ind,:]
        
        c_cover = 0
        for i in range(hrrr_c.shape[0]):
            temp = hrrr_c[i,:].max(axis=0)
            if temp>hrrr_margin:
                c_cover = c_cover+1
                c_fract = float(c_cover)/float(hrrr_c.shape[0])

        c_fracts_hrrr.append(c_fract)
        dates.append(dates[i])
        hrrr_hoursets.append(hrrr_hours)
        
        #kill storage vars
        hrrr = None
        hrrr_data = None
        hrrr_c = None
        hrrrf.close()
        
        #radar analysis
        os.chdir(radar_directory)
        radarf = open(radar_strings[i],'r')
        
        radar = json.load(radarf)
        radar = np.array(radar[0]) 
        
        radar = np.array(radar[0])
        c_fract = sum(radar.max(axis=1)>radar_margin)/float(radar.shape[0])
        c_fracts_radar.append(c_fract)
        
        #kill storage vars
        radar = None
        radarf.close()

h = open('radarhrrrcompareoutput','w')

json.dump([c_fracts_radar,c_fracts_hrrr,dates,hrrr_hoursets,['radar_c_fracts','hrrr_c_fracts','dates','hrrr_hoursets']],h)

h.close()

        
        
        
        
        
        
        
        
        
        
        


    