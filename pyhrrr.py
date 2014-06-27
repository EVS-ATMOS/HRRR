# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:46:41 2014

@author: mattjohnson
"""
"""
Imports all functions in the functions folder of our project.  As a script
works for any directory, but can only be directly called for import in the 
HRRR directory.  
"""

import os
import numpy as np
import json

global HRRR_PS
HRRR_PS = np.array([1013, 1000,  975,  950,  925,  900,  875,  850,  825,  800,  775,
        750,  725,  700,  675,  650,  625,  600,  575,  550,  525,  500,
        475,  450,  425,  400,  375,  350,  325,  300,  275,  250,  225,
        200,  175,  150,  125,  100,   75,   50])
        
global HRRR_VARS
HRRR_VARS =['Geopotential Height','Temperature','Relative humidity','Dew point temperature',
        'Specific humidity','Vertical velocity','U component of wind','V component of wind',
        'Absolute vorticity','Cloud mixing ratio','Cloud Ice','Rain mixing ratio','Snow mixing ratio',
        'Graupel (snow pellets)']
        


wkdir = os.getcwd()

directory = wkdir[:]

while "HRRR" in directory:
    os.chdir(os.path.abspath('..'))
    directory = os.getcwd()
    
os.chdir(directory+'/HRRR')



global HRRR_DATALOC
f = open('dataloc','r')
HRRR_DATALOC = np.array(json.load(f))
f.close()

dirpath = os.path.abspath("HRRR")

os.chdir(dirpath)

global HRRR_DATALOC
f = open('dataloc','r')
HRRR_DATALOC = np.array(json.load(f))
f.close()

dirpath2 = dirpath+'/functions/'

filenames = os.listdir(dirpath2)
    
for name in filenames:
    execfile(dirpath2+'/'+name)

os.chdir(wkdir)
    
    


