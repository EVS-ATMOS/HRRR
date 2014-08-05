# -*- coding: utf-8 -*-
'''
This function takes in a date as a datetime object and the directory of ARM KAZR radar files.
It plots a basic reflectivity plot for the entered date quickly without using pcolor or pcolormesh.
(pcolor took too long to run these large files)
The X-axis has incorrect values, but the grids are every hour for the 24 time period.
Reflectivity is filtered (masked) by the SNR. 


Author: Grant McKercher
'''

from scipy.io import netcdf
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy.ma as ma

def plot_kazr(date,radar_dir):

    path = os.getcwd()

    [radar] = gather_radar_files(date,radar_dir)
    
    # Gather files
    os.chdir(radar_dir)
    f = netcdf.netcdf_file(radar, 'r')
    
    # Make Plot
    
    # Read in data
    rng = f.variables['range'].data
    refc = f.variables['reflectivity_copol'].data
    stnrc = f.variables['signal_to_noise_ratio_copol'].data
    # Masking Radar Attenuation
    refc = ma.masked_where((stnrc <= -14),refc)
    
    fig = plt.figure(figsize = [15,8])
    
    ax = fig.add_subplot(111)
    im = plt.imshow(refc.T,aspect=20,extent=[0,1000000,min(rng),max(rng)],origin='bottom')
    ax.set_title('SGP copolar reflectivity, masked SNR')
    # x axis
    xmajorLocator = MultipleLocator(41666.66666666667) 
    ax.xaxis.set_major_locator(xmajorLocator)
    xmajorFormatter = FormatStrFormatter('%d')
    ax.xaxis.set_major_formatter(xmajorFormatter)

    ax.set_xlabel('Hours (UTC) - Grid by hour')

    # y axis
    ymajorLocator = MultipleLocator(2500)
    ax.yaxis.set_major_locator(ymajorLocator)
    ymajorFormatter = FormatStrFormatter('%d')
    ax.yaxis.set_major_formatter(ymajorFormatter)
    ax.set_ylabel('Height (m)')
    plt.grid()
    
    cb = plt.colorbar(ax=ax,mappable=im,aspect=20,orientation='vertical',shrink=0.55)
    cb.set_label(r'Reflectivity factor, $Z_e$ (dBZ)')

    f.close()