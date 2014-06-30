# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 09:14:32 2014

@author: mattjohnson
"""
import os


def analyze_hrrr(dates,analysis_day = 'data',analysis_hour = 'analysis',analysis_overall = 'analysish',hourlists = [1],directory=os.getcwd(),loc = [36.605,-97.485],indexes = None):
    """
    flexible analysis function for analyzing hrrr text files on several different levels, analysis strings are lines of executable code
    that are run and the returned value becomes the analysis for that level, if a level is ignored it will compile all of the data into a list for that level
    allowing analysis to take place at the next level
    """
    
    analysisd = []
    analysish = []
    
    for j in hourlists:
        for i in dates:
            [data,dates,parameterlist,loc,indexes,units] = read_hrrr_txt(date=i,hour=j,filenum = 24,directory=directory,filename = None,loc=loc,indexes=indexes, read_modelhours = False)
            analysisd.append(eval(analysis_day))
        analysish.append(eval(analysis_hour))
    analysis = eval(analysis_overall)
        
    return [analysis, dates]