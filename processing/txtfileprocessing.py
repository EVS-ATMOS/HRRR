# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 10:06:27 2014

@author: mattjohnson
"""


strings = []
strings.append('import datetime')
strings.append('import pyhrrr')

strings.append("enddirectory = '/home/mjohnson/python/hrrr_txt'")

strings.append("directory = '/data/san_store/HRRR'")


import datetime

n = 4

startdate = datetime.datetime(2014,3,15)

enddate = datetime.datetime(2014,7,6)

t = enddate-startdate
dt = int(t.days/n)
dt = datetime.timedelta(days=dt)
datepairs = []
newstart = startdate

for i in range(n):
    if i<(n-1):
        datepairs.append((newstart,newstart+dt))
    else:
        datepairs.append((newstart,enddate))
    newstart = newstart+dt


for i in range(n):
    sdatepair = datepairs[i][0]
    edatepair = datepairs[i][1]
    newstrings = strings[:]
    newstrings.append('startdate = '+'datetime.datetime('+str(sdatepair.year)+','+str(sdatepair.month)+','+str(sdatepair.day)+')')
    newstrings.append('enddate = '+'datetime.datetime('+str(edatepair.year)+','+str(edatepair.month)+','+str(edatepair.day)+')')
    newstrings.append('pyhrrr.massconvert_hrrr_grib2txt(startdate=startdate,enddate=enddate,hours = [0,1,2,3,4],directory=directory,enddirectory=enddirectory)')
    
    f = open('process'+str(i)+'.py','w')
    
    for j in newstrings:
        f.write(j+'\n')
    
    f.close()




