# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 13:31:58 2014

@author: mattjohnson
"""
"""
Note:  requires Image Magick
"""
import os

def makegif_hrrr_imagefiles(imagefilelist,directory = os.getcwd(),name = 'video',inputtype = '.png',outputtype = '.gif'):
    """
    This converts a series of images in alphabetical order existing in a given directory, for which they 
    are the only images of their type into a .gif file.  Other outputtypes may not be valid.  
    """
    import os
    
    wkdir = os.getcwd()
    os.chdir(directory)
    
    name = name+outputtype
    
    namet = name
    
    i = 0
    
    while namet in os.listdir(directory):
        namet = name+str(i)
        i = i+1
    
    string = 'convert *'+inputtype+' '+namet
    
    os.system(string)
    os.chdir(wkdir)
    
    return name
    
    
