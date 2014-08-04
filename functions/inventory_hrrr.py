# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 09:35:18 2014

@author: mattjohnson
"""

def inventory_hrrr(in_dir):
    """
    Takes in a directory containing hrrr files.  Returns a list of the number of
    dates having each index's number of files, a list containing the number of 
    missing files for each date, a list of lists in which true corresponds to 
    missing files, and the list of dates.
    """
    
    x = gather_hrrr_files(in_dir)
    z = x[0]
    y = [[(None == z[j][i]) for i in range(len(z[j]))] for j in range(len(z))]
    
    k = []
    for i in range(len(z)):
        r = 0
        for j in range(len(z[i])):
            if y[i][j] == True:
                r = r+1
        k.append(r)

    u = [0 for i in range(len(z[0]))]

    for i in k:
        u[i] = u[i]+1

    return [u,k,y,x[1]]