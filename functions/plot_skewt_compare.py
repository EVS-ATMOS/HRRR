# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 15:37:48 2014

Function plots a balloon sounding and hrrr txt file sounding for comparison

@author: gmckercher and mjohnson
"""

def plot_skewt_compare(date,sound_dir,hrrr_hour):
    
    import numpy as np
    from scipy.io import netcdf
    import datetime
    import os
    
    path = os.getcwd()

    sounding = gather_sounding_files(date,sound_dir)
    
    # Gather files
    os.chdir(sounding_dir)    
    s = netcdf.netcdf_file(sounding, 'r')
    # Read in the sounding variables
    psnd = s.variables['pres'].data
    hsnd = s.variables['alt'].data
    tsnd = s.variables['tdry'].data
    tdsnd = s.variables['dp'].data
    u = s.variables['u_wind'].data
    v = s.variables['v_wind'].data
    
    # Read in HRRR data from text file
    p_hrrr = HRRR_PS
    [data,dates,parameterlist,loc,indexes,units] = read_hrrr_txt(date = date,hour=hrrr_hour,filenum=24,
                                directory = '/data/san_store/hrrr_txt',loc = [36.605,-97.485],
                                indexes=None,read_modelhours=False)
    # Find model hour closest to entered time
    hour = hrrr_hour
    
    
    [dates_sound,filename_sound] = org_sounding_files(sounding_dir)
    s_dates = [i.date for i in dates_sound]
    s_index = s_dates.index(date)
    
    c_date = dates_sound[s_index]-datetime.timedelta(hours=hour)
    date_ch = [i-c_date for i in dates]
    date_shifts = [i.total_seconds() for i in date_ch]
    date_shifts = np.array(date_shifts)**2
    ind = date_shifts.tolist().index(min(date_shifts))
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
    
    # Plot sounding skewt
    plot_skewt_wind(psnd,hsnd,tsnd,tdsnd,u,v)
    
    # Plot model skewt
    plot_skewt_wind(p_hrrr,h_hrrr,T_hrrr,Td_hrrr,U_hrrr,V_hrrr)
    
    os.chdir(path)
    
    
    
    
    
    
    