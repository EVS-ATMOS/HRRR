# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 15:13:30 2014

Function takes in reflectivity and signal to noise ratio and returns a reflectivity without radar attenuation.

@author: gmckercher
"""

import numpy.ma as ma

def filter_ref_snr(ref,snr):

    m_ref = ma.masked_where((snr <= -14),ref)
    
    return m_ref

