# -*- coding: utf-8 -*-


'''
This function takes in radar, sounding, and ceilometer files from their directory, organizes them by date and creates a figure with three plots. The first plot is copolar reflectivity with masked backround noise, the second plot is vertical velocity, and the third plot is spectral width. 

Authors: Grant McKercher & Matt Johnson
'''

import numpy as np
from scipy.io import netcdf
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy.ma as ma
import os



def plot_kazr(date,radar_dir,sound_dir,ceil_dir):

    path = os.getcwd()

    [radar,sound,ceil] = gather_exp_files(date,radar_dir,sound_dir,ceil_dir)
    
    # Gather files
    os.chdir(radar_dir)
    f = netcdf.netcdf_file(radar, 'r')
    os.chdir(sound_dir)
    s = netcdf.netcdf_file(sound, 'r')
    os.chdir(ceil_dir)
    c = netcdf.netcdf_file(ceil, 'r')
    os.chdir(path)

    # Read in data
    fcbh = c.variables['first_cbh'].data
    rng = f.variables['range'].data
    #refx = f.variables['range'].data
    refc = f.variables['reflectivity_copol'].data
    mdvc = f.variables['mean_doppler_velocity_copol'].data
    swc = f.variables['spectral_width_copol'].data
    
    fig = plt.figure(figsize = [25,18])

    # First Figure

    ax1 = fig.add_subplot(3,1,1)
    ax1.set_title( 'SGP KAZR Filtered Copol Reflectivity / Ceilometer Cloud Base 5/27/2014' )
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
    # Calculate Linear Depolarization Ratio
    #ldr = (refx-refc)
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
    ax2.set_title( 'SGP KAZR Copol Mean Doppler Velocity 5/27/2014' )
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
    # Plot radar reflectivity
    pc2 = plt.pcolormesh(np.array(day), rng, mdvc.T, cmap='jet')
    # Plot Colorbar
    cb = plt.colorbar(ax=ax2,mappable=pc2,orientation='vertical')
    cb.set_label(r'Velocity (m/s)')

    # Third Figure

    ax3 = fig.add_subplot(3,1,3)
    ax3.set_title( 'SGP KAZR Copol Spectral Width 5/27/2014' )
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

    f.close()
    s.close()
    c.close()
