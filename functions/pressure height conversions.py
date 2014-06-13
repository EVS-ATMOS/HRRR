# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 09:20:18 2014

@author: mattjohnson
"""

import os
import math
import numpy as np

global HRRR_PS
HRRR_PS = np.array([1013, 1000,  975,  950,  925,  900,  875,  850,  825,  800,  775,
        750,  725,  700,  675,  650,  625,  600,  575,  550,  525,  500,
        475,  450,  425,  400,  375,  350,  325,  300,  275,  250,  225,
        200,  175,  150,  125,  100,   75,   50])
        
        

def convert_press2height(temps,z0,press = HRRR_PS):
    """
    conversion from hPa to m assuming ideal gas law using the ideal gas law equation
    """
    z = [z0]
    
    for i in range(len(press)-1):
        z.append(z[i]+.0289644*8.31447*(temps[i]+temps[i+1])/2/9.81*math.log(press[i+1]/press[i]))
    
    return z

def convert_height2press(z,z0=0,T0=298.15,p0=1013.25,n = 1.4):
    """
    assumes heating in the atmosphere is polytropic with index n
    assumes atmosphere is at equilibirum
    converts m to hPa
    """
    p = []
    
    for i in range(len(z)): 
        T = T0-(n-1)/n*9.81/.0289644/8.31447*(z[i]-z0)
        p.append(p0*(T/T0)**(n/(n-1)))
    
    return p

    
    
        
        
    