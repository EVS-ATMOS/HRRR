import datetime
import pyhrrr
enddirectory = '/home/mjohnson/python/hrrr_txt'
directory = '/data/san_store/HRRR'
startdate = datetime.datetime(2014,6,26)
enddate = datetime.datetime(2014,7,3)
pyhrrr.massconvert_hrrr_grib2txt(startdate=startdate,enddate=enddate,hours = [0,1,2,3,4],directory=directory,enddirectory=enddirectory)
