# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 09:20:18 2014

@author: mattjohnson
"""

import os
import math
import numpy as np

def convert_press2height(temps,z0=0,press = HRRR_PS):
    """
    conversion from hPa to m assuming ideal gas law using the ideal gas law equation
    """
    z = [z0]
    
    for i in range(len(press)-1):
        z.append(z[i]+.0289644*8.31447*(temps[i]+temps[i+1])/2/9.81*math.log(press[i+1]/press[i]))
    
    return z

def convert_height2press(z,T = None,z0=0,T0=298.15,p0=1013.25,n = 1.4):
    """
    assumes heat loss going up in the atmosphere is polytropic with index n
    converts m to hPa
    """
    if T == None:
        p = []
    
        for i in range(len(z)): 
            T = T0-(n-1)/n*9.81/.0289644/8.31447*(z[i]-z0)
            p.append(p0*(T/T0)**(n/(n-1)))
        return p
    
    p = [p0]
    
    for i in range(len(z)-1):
        p.append(p[i]*math.exp(9.81*(z[i+1]-z[i])/.0289644/8.31447/(T[i]+T[i+1])/2))
        
        

    
    
        
        
    