# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 15:58:52 2014

This function takes local netCDF filenames of an ARM KAZR and ARM CEILOMETER for a certain day. 
It produces a figure including 3 subplots. 
(1) SNR filtered co-polar reflectivity with ceilometer cloud base
(2) Co-polar mean dopplar velocity
(3) Co-polar spectral width

@author: Grant McKercher
"""


import numpy as np
from scipy.io import netcdf
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy.ma as ma

def plot_kazr_mulitplot(kazr_filename,ceilometer_filename):
    f = netcdf.netcdf_file(kazr_filename, 'r')
    c = netcdf.netcdf_file(ceilometer_filename, 'r')
    
    # Read in data
    fcbh = c.variables['first_cbh'].data
    rng = f.variables['range'].data
    refc = f.variables['reflectivity_copol'].data
    mdvc = f.variables['mean_doppler_velocity_copol'].data
    swc = f.variables['spectral_width_copol'].data
    
    fig = plt.figure(figsize = [20,16])
    
    # First Figure
    
    ax1 = fig.add_subplot(3,1,1)
    ax1.set_title( 'SGP KAZR Filtered Copol Reflectivity / Ceilometer Cloud Base' )
    ax1.set_xlabel('UTC Time (Hour)',fontsize=14)
    ax1.set_ylabel('Height (m)',fontsize=14)
    ax1 = plt.gca()
    ax1.set_ylim([min(rng),max(rng)])
    ax1.set_xlim([0, 24])
    # x axis
    xmajorLocator = MultipleLocator(1)
    ax1.xaxis.set_major_locator(xmajorLocator)
    xmajorFormatter = FormatStrFormatter('%d')
    ax1.xaxis.set_major_formatter(xmajorFormatter)
    # y axis
    ymajorLocator = MultipleLocator(2500)
    ax1.yaxis.set_major_locator(ymajorLocator)
    ymajorFormatter = FormatStrFormatter('%d')
    ax1.yaxis.set_major_formatter(ymajorFormatter)
    # Filter signal to noise ratio
    stnrc = f.variables['signal_to_noise_ratio_copol'].data
    refc = ma.masked_where((stnrc <= -14),refc)
    # Plot radar reflectivity
    t = f.variables['time'][:]
    day = [t[i]/3600 for i in range(len(t))]
    pc1 = plt.pcolormesh(np.array(day), rng, refc.T, cmap='jet')
    # Plot Colorbar
    cb = plt.colorbar(ax=ax1,mappable=pc1,orientation='vertical')
    cb.set_label(r'Reflectivity factor, $Z_e$ (dBZ)')
    # Plot cloud-base height
    ct = c.variables['time'][:]
    cday = [ct[i]/3600 for i in range(len(ct))]
    plt.scatter(cday,fcbh,s=2, marker='.')
    
    # Second Figure
    
    ax2 = fig.add_subplot(3,1,2)
    ax2.set_title( 'SGP KAZR Copol Mean Doppler Velocity' )
    ax2.set_xlabel('UTC Time (Hour)',fontsize=14)
    ax2.set_ylabel('Height (m)',fontsize=14)
    ax2 = plt.gca()
    ax2.set_ylim([min(rng),max(rng)])
    ax2.set_xlim([0, 24])
    # x axis
    xmajorLocator = MultipleLocator(1)
    ax2.xaxis.set_major_locator(xmajorLocator)
    xmajorFormatter = FormatStrFormatter('%d')
    ax2.xaxis.set_major_formatter(xmajorFormatter)
    # y axis
    ymajorLocator = MultipleLocator(2500)
    ax2.yaxis.set_major_locator(ymajorLocator)
    ymajorFormatter = FormatStrFormatter('%d')
    ax2.yaxis.set_major_formatter(ymajorFormatter)
    # Filter signal to noise ratio
    mdvc = ma.masked_where((stnrc <= -14),mdvc)
    # Plot radar reflectivity
    pc2 = plt.pcolormesh(np.array(day), rng, mdvc.T, cmap='jet')
    # Plot Colorbar
    cb = plt.colorbar(ax=ax2,mappable=pc2,orientation='vertical')
    cb.set_label(r'Velocity (m/s)')
    
    # Third Figure
    
    ax3 = fig.add_subplot(3,1,3)
    ax3.set_title( 'SGP KAZR Copol Spectral Width' )
    ax3.set_xlabel('UTC Time (Hour)',fontsize=14)
    ax3.set_ylabel('Height (m)',fontsize=14)
    ax3 = plt.gca()
    ax3.set_ylim([min(rng),max(rng)])
    ax3.set_xlim([0, 24])
    # x axis
    xmajorLocator = MultipleLocator(1)
    ax3.xaxis.set_major_locator(xmajorLocator)
    xmajorFormatter = FormatStrFormatter('%d')
    ax3.xaxis.set_major_formatter(xmajorFormatter)
    # y axis
    ymajorLocator = MultipleLocator(2500)
    ax3.yaxis.set_major_locator(ymajorLocator)
    ymajorFormatter = FormatStrFormatter('%d')
    ax3.yaxis.set_major_formatter(ymajorFormatter)
    # Plot radar reflectivity
    swc = ma.masked_where((swc == -9999),swc)
    pc3 = plt.pcolormesh(np.array(day), rng, swc.T, cmap='jet')
    # Plot Colorbar
    cb = plt.colorbar(ax=ax3,mappable=pc3,orientation='vertical')
    cb.set_label(r'Velocity (m/s)')
    
    fig.tight_layout()