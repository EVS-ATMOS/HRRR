import datetime
import pyhrrr
enddirectory = '/home/mjohnson/python/hrrr_txt'
directory = '/data/san_store/HRRR'
startdate = datetime.datetime(2014,3,15)
enddate = datetime.datetime(2014,4,18)
pyhrrr.massconvert_hrrr_grib2txt(startdate=startdate,enddate=enddate,hours = [0,4],directory=directory,enddirectory=enddirectory)
