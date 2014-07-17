# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 15:37:48 2014

Function plots a balloon sounding and hrrr txt file sounding for comparison

@author: gmckercher and mjohnson
"""

def plot_skewt_compare(date,sound_dir,hrrr_hour,sound_num):
    
    import numpy as np
    from scipy.io import netcdf
    from matplotlib.dates import date2num
    import matplotlib.pyplot as plt
    import datetime
    import os
    
    path = os.getcwd()

    sounding = gather_sounding_files(date,sound_dir,sound_num)
    # Gather files
    os.chdir(sound_dir)    
    s = netcdf.netcdf_file(sounding, 'r')
    # Read in the balloon sounding variables
    psnd = s.variables['pres'].data
    hsnd = s.variables['alt'].data
    tsnd = s.variables['tdry'].data
    tdsnd = s.variables['dp'].data
    u = s.variables['u_wind'].data
    v = s.variables['v_wind'].data
    
    # Pressure level at which temperature = dewpoint temperature
    cloud = []
    for i,j in enumerate(psnd):
        if (tsnd[i]==tdsnd[i]):
            cloud.append(psnd[i])
    
    if (cloud != []):
        maxp = np.max(cloud)
        minp = np.min(cloud)
        print 'Balloon 100% saturation:',maxp,'hPa','-',minp,'hPa\n'
    else:
        print 'No cloud\n'
        
    # Plot balloon sounding skewt
    plot_skewt_wind(psnd,hsnd,tsnd,tdsnd,u,v) 

    # Read in HRRR data from text file
    p_hrrr = HRRR_PS
    name = produce_hrrr_txt_string(date,hour = hrrr_hour)
    print 'Reading',name
    [data,dates,parameterlist,loc,indexes,units] = read_hrrr_txt(directory = '/data/san_store/hrrr_txt',filename = name)
    # Find model hour closest to entered time
    hour = hrrr_hour

    [dates_sound,filename_sound] = org_sounding_files(sound_dir)
    s_dates = [i.date() for i in dates_sound]    
    
    s_index = s_dates.index(date.date())
    
    if (sound_num==2):
        s_index2 = s_index+sound_num-1
        c_date = dates_sound[s_index2]-datetime.timedelta(hours=hour)
        print 'HRRR Model Sounding, Forecast:',c_date,'for',hour,'hour'
    elif (sound_num==3):
        s_index3 = s_index+sound_num-1
        c_date = dates_sound[s_index3]-datetime.timedelta(hours=hour)
        print 'HRRR Model Sounding, Forecast:',c_date,'for',hour,'hour'
    elif (sound_num==4):
        s_index4 = s_index+sound_num-1
        c_date = dates_sound[s_index4]-datetime.timedelta(hours=hour)
        print 'HRRR Model Sounding, Forecast:',c_date,'for',hour,'hour'
    else:
        c_date = dates_sound[s_index]-datetime.timedelta(hours=hour)
        print 'HRRR Model Sounding, Forecast:',c_date,'for',hour,'hour'
    
    dates = np.array(dates)
    dates = date2num(dates)
    c_date = date2num(c_date)
    ind = ((dates-c_date)**2).tolist().index(min((dates-c_date)**2)) 
    
    # Gather parameters
    ti = HRRR_VARS.index('Temperature')
    tdi = HRRR_VARS.index('Dew point temperature')
    ui = HRRR_VARS.index('U component of wind')
    vi = HRRR_VARS.index('V component of wind')
    data=np.array(data)
    T_hrrr = (data[:,ti,:])-273.15
    T_hrrr = T_hrrr[ind,:]
    Td_hrrr = (data[:,tdi,:])-273.15
    Td_hrrr = Td_hrrr[ind,:]
    U_hrrr = data[:,ui,:]
    U_hrrr = U_hrrr[ind,:]
    V_hrrr = data[:,vi,:]
    V_hrrr = V_hrrr[ind,:]
    #Interpolation of HRRR height using balloon sounding
    h_hrrr = []
    h_hrrr = np.interp(p_hrrr[::-1],psnd[::-1],hsnd[::-1])
    h_hrrr = h_hrrr[::-1]
        
     # Plot model skewt
    plot_skewt_wind(p_hrrr,h_hrrr,T_hrrr,Td_hrrr,U_hrrr,V_hrrr)
        
    os.chdir(path)
    
    
    
    
    
    
    