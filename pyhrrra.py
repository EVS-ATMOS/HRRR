

import os
import numpy as np

global HRRR_PS
HRRR_PS = np.array([1013, 1000,  975,  950,  925,  900,  875,  850,  825,  800,  775,
        750,  725,  700,  675,  650,  625,  600,  575,  550,  525,  500,
        475,  450,  425,  400,  375,  350,  325,  300,  275,  250,  225,
        200,  175,  150,  125,  100,   75,   50])
        
global HRRR_VARS
HRRR_VARS =['Geopotential Height','Temperature','Relative humidity','Dew point temperature',
        'Specific humidity','Vertical velocity','U component of wind','V component of wind',
        'Absolute vorticity','Cloud mixing ratio','Cloud Ice','Rain mixing ratio','Snow mixing ratio',
        'Graupel (snow pellets)']
        
path = os.getcwd()

x = os.listdir(path)

for i in x:
    if '.ipynb' in i or i == 'pyhrrra.py' or i == 'pyhrrra.pyc' or i == 'pyhrrr.py' or i == 'pyhrrr.pyc':
        continue
    elif '.py' in i:
        execfile(path+'/'+i)
        
        