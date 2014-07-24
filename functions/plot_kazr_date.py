# -*- coding: utf-8 -*-


'''
This function takes in radar, sounding, and ceilometer files from their directory, organizes them by date and creates a figure with three plots. The first plot is copolar reflectivity with masked backround noise, the second plot is vertical velocity, and the third plot is spectral width. 

Authors: Grant McKercher & Matt Johnson
'''

from scipy.io import netcdf
import os


def plot_kazr_date(date,radar_dir):

    path = os.getcwd()

    [radar] = gather_radar_files(date,radar_dir)
    
    # Gather files
    os.chdir(radar_dir)
    f = netcdf.netcdf_file(radar, 'r')
    # Make Plot
    plot_kazr(radar)

