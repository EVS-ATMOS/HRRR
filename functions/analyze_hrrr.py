# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 09:14:32 2014

@author: mattjohnson
"""
import os
import datetime

def analyze_hrrr(analysis_day = data,analysis_hour = analysis,analysis_overall = analysish,hourlists,directory=os.getcwd(),loc,indexes):
    """
    """
    
    analysisd = []
    analysish = []
    
    for j in hourlists:
        for i in dates:
            filestring = produce_hrrr_grib2strings([i],[j])
            [data,dates,parameterlist,loc,indexes,units] = read_hrrr_txt(date=i,hour=j,filenum = 24,directory=directory,filename = None,loc=loc,indexes=indexes, read_modelhours = False)
            analysisd.append(eval(analysis_day))
        analysish.append(eval(analysis_hour))
    analysis = eval(analysis_overall)
        
    return [analysis, dates]