# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:19:26 2014

@author: mattjohnson
"""

import numpy as np
import datetime

"""
Warning the dst if statements have not been extensively tested as they aren't vital to our project
"""
def get_sun(date = datetime.datetime.now(),loc = [36.605,-97.485],timeshift = np.floor(abs(loc[1]/15))):
    """
    takes in the date, location, daylight savings time boolean and the timeshift for the timezone
    returns the fractional hour of sunrise and sunset and the datetimes of sunrise and sunset accurate to a minute
    
    The timezone calculation is only an approximation and only work when loc is a decent distance from timezone borders
    for example chicago, IL, US will be put in the wrong timezone by this function
    
    """
    hour = 0
    day_of_year = date.timetuple().tm_yday
    loc = np.array(loc[:])
    loc[1] = -loc[1]
    
    gamma = np.pi*2/365*(day_of_year-1+(hour-12)/24)
    
    eqtime=229.18*(0.000075+0.001868*np.cos(gamma)-0.032077*np.sin(gamma)-0.014615*np.cos(2*gamma)-0.040849*np.sin(2*gamma))
    decl = .006918-.399912*np.cos(gamma)+.070257*np.sin(gamma)-.006758*np.cos(2*gamma)+.000907*np.sin(2*gamma)-.0026967*np.cos(3*gamma)+.00148*np.sin(3*gamma)
    
    ha = np.arccos((np.cos(90.833*2*np.pi/360.0)/(np.cos(loc[0]*np.pi*2/360.0)*np.cos(decl)))-np.tan(loc[0]*2*np.pi/360)*
               np.tan(decl))
    
    sunrise = 720+4*(loc[1]-ha*360/(2*np.pi))-eqtime
    sunset = 720+4*(loc[1]+ha*360/(2*np.pi))-eqtime
    
    if date.month>3 and date.month<11:
        dst = 1
    elif date.month<3 or date.month == 12:
        dst = 0
    elif date.month == 3:
        day = date.day
        dayssincesun = date.isoweekday()
        week = day/7
        dayofweek = day%7
        if week == 1:
            dst = 0
        elif week >2:
            dst = 1
        elif dayssincesun == 7:
            dst = 1
        elif dayofweek-dayssincesun>0:
            dst = 1
        else:
            dst = 0
            
    
    sunrise = sunrise/60+timeshift+dst
    sunset = sunset/60+timeshift+dst
    
    sunrisedate = datetime.datetime(2014,6,19,int(sunrise),int((sunrise-int(sunrise))*60))
    sunsetdate = datetime.datetime(2014,6,19,int(sunset),int((sunset-int(sunset))*60))
    
    return[[sunrise,sunset],[sunrisedate,sunsetdate]]