# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 15:13:30 2014

Function takes in reflectivity and signal to noise ratio and returns a reflectivity without radar attenuation.

@author: gmckercher
"""

import numpy.ma as ma

def filter_ref(ref,snr,margin):

    m_ref = ma.masked_where((snr >= margin),ref) #-snr,margin=-14 for snr

    return m_ref

