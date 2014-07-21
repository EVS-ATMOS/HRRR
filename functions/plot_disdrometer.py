# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 15:27:53 2014

Function takes in the date for analysis and directory of the disdrometer data and plots the data in three useful plots and prints precipitation information.

@author: gmckercher
"""


import numpy as np
from scipy.io import netcdf
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy.ma as ma

def plot_disdrometer(date,dis_dir):
    
    path = os.getcwd()

    [disdrometer] = gather_disdrometer_files(date,dis_dir)
    
    # Gather files
    os.chdir(dis_dir)
    d = netcdf.netcdf_file(disdrometer, 'r')
    
    #Read in data
    dref = d.variables['radar_reflectivity'].data
    drr = d.variables['rain_rate'].data
    dlw = d.variables['liq_water'].data
    dpcp = d.variables['precip_dis'].data
    dt = d.variables['time'].data

    fig = plt.figure(figsize = [16,16])

    # Figure 1
    ax1 = fig.add_subplot(3,1,1)
    dt = d.variables['time'][:]
    day = [dt[i]/3600 for i in range(len(dt))]
    plt.plot(day,drr,lw=2,c='r')
    plt.title( 'Disdrometer Rain Rate 5/23/2014' )
    plt.xlabel('UTC Time (Hours)')
    plt.ylabel('Rain Rate (mm/hr)')
    ax1 = plt.gca()
    ax1.set_ylim([min(drr),max(drr)])
    ax1.set_xlim([0, 24])
    majorLocator = MultipleLocator(1)
    ax1.xaxis.set_major_locator(majorLocator)
    majorFormatter = FormatStrFormatter('%d')
    ax1.xaxis.set_major_formatter(majorFormatter)
    plt.grid()

    # Figure 2
    ax2 = fig.add_subplot(3,1,2)
    dref = ma.masked_where((dref == -9999),dref)
    plt.scatter(day,dref,c=dref,s=50,lw=0,cmap='jet')
    plt.title( 'Disdrometer Radar Reflectivity 5/23/2014' )
    plt.xlabel('UTC Time (Hours)')
    plt.ylabel(r'Reflectivity factor, $Z_e$ (dBZ)')
    ax2 = plt.gca()
    ax2.set_ylim([min(dref),max(dref)])
    ax2.set_xlim([0, 24])
    majorLocator = MultipleLocator(1)
    ax2.xaxis.set_major_locator(majorLocator)
    majorFormatter = FormatStrFormatter('%d')
    ax2.xaxis.set_major_formatter(majorFormatter)
    plt.grid()

    # Figure 3
    ax3 = fig.add_subplot(3,1,3)
    dlw = (dlw/(1000))
    plt.plot(day,dlw)
    plt.title( 'Disdrometer Liquid Water Content 5/23/2014' )
    plt.xlabel('UTC Time (Hours)')
    plt.ylabel('Liquid Water Content (g/kg)')
    ax3 = plt.gca()
    ax3.set_ylim([min(dlw),max(dlw)])
    ax3.set_xlim([0, 24])
    majorLocator = MultipleLocator(1)
    ax3.xaxis.set_major_locator(majorLocator)
    majorFormatter = FormatStrFormatter('%d')
    ax3.xaxis.set_major_formatter(majorFormatter)
    
    plt.grid()
    plt.show()


    # Precipitation Info
    
    print '--------------------------------------------------------------'
    print '-----------------PRECIPITATION INFORMATION--------------------'
    print '--------------------------------------------------------------\n'    
    
    count = 0
    for i,j in enumerate(dpcp):
        if (j!=0.):
            count = count+1
    rainsec = count*60.
    rainmin = count
    rainhr = count/60.
    rainmm = np.sum(dpcp)
    print 'Total Precipitation Duration:',float(rainhr),'hours,',float(rainmin),'minutes,',float(rainsec),'seconds'
    rainin = (rainmm/100)*0.393701
    print 'Total Precipitation Amount:',rainmm,'mm,',rainin,'in'

    # Rain Rate info
    # Total Recording Duration (Greater than 0)
    count = 0
    for i,j in enumerate(drr):
        if (j>0.):
            count = count+1
    rainsec = count*60.
    rainmin = count
    rainhr = count/60.
    print 'Total Rain Rate Recording Duration:',float(rainhr),'hours,',float(rainmin),'minutes,',float(rainsec),'seconds'

    # Light Rain Duration (Less than 2.5mm/hr)
    count = 0
    for i,j in enumerate(drr):
        if (j<2.5) and (j>0):
            count = count+1
    rainsec = count*60.
    rainmin = count
    rainhr = count/60.
    print 'Light Rain Rate Duration:',float(rainhr),'hours,',float(rainmin),'minutes,',float(rainsec),'seconds'

    # Medium Rain Duration (Between 2.5 and 76 mm/hr)
    count = 0
    for i,j in enumerate(drr):
        if (j<=76) and (j>=2.5):
            count = count+1
    rainsec = count*60.
    rainmin = count
    rainhr = count/60.
    print 'Medium Rain Rate Duration:',float(rainhr),'hours,',float(rainmin),'minutes,',float(rainsec),'seconds'

    # Heavy Rain Duration (Greater than 76mm/hr)
    count = 0
    for i,j in enumerate(drr):
        if (j>76):
            count = count+1
    rainsec = count*60.
    rainmin = count
    rainhr = count/60.
    print 'Heavy Rain Rate Duration:',float(rainhr),'hours,',float(rainmin),'minutes,',float(rainsec),'seconds'

    # Average Rain Rate
    avgin = ((np.average(drr)/100)*0.393701)
    print 'Average Rain Rate:',np.average(drr),'mm/hr,',avgin,'in/hr'
    
    os.chdir(path)