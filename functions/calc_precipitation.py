# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 11:30:17 2014

@author: mattjohnson
"""
import numpy as np
import os
import json

def calc_precipitation(date,hrrr_dir=os.getcwd(),radar_dir=os.getcwd(),rain_margin = 0):
    """
    estimates the precipitation in the HRRR model, assumes all rain-mixing-ratio water reaches the ground
    and that the rain-mixing-ratio is constant over the hour, returns the values in mm over the 3 km* 3 km grid space
    also estimates rain duration by determing which hours have a max rain-mixing-ratio greater than the margin
    """
    radar_string = produce_radar_txt_string(date)

    hrrr_string = produce_hrrr_txt_string(date,filenum = 24,hour = 1,loc=[36.605, -97.485], indexes = None,
                                             modelhours = False)
    wkdir = os.getcwd()
    os.chdir(hrrr_dir)
    hrrrf = open(hrrr_string,'r')
    hrrr = json.load(hrrrf)
    hrrr[0] = np.array(hrrr[0])

    rho_air = np.divide(HRRR_PS*np.ones(HRRR_PS.shape[0]).T*29/1000*100,8.314*hrrr[0][:,1,:])
    
    os.chdir(radar_dir)
    radarf = open(radar_string,'r')
    [z,hrrr_heights,tsinds,psinds] = json.load(radarf)
    
    
    volboxes = [((hrrr_heights[i]+hrrr_heights[i+1])/2-(hrrr_heights[i-1]+hrrr_heights[i])/2) for i in range(1,hrrr_heights.shape[0]-1)]
    volboxes.insert(0,(hrrr_heights[1]+hrrr_heights[0])/2)
    volboxes.append((hrrr_heights[-1]-(hrrr_heights[-1]+hrrr_heights[-2])/2))
    volboxes = np.array(volboxes)
    
    rainmassperarea = np.multiply(np.multiply(volboxes,rho_air),hrrr[0][:,11,:])
    
    raininmeters = rainmassperarea/1000
    
    raininmm = raininmeters*10**3
    
    duration = hrrr[0][:,11,:]>rain_margin
    duration = duration.max(axis=1)
    duration = duration.sum(axis=0)
    
    os.chdir(wkdir)
    
    return [raininmm, duration, ['mm','hr']]