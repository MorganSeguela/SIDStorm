# -*- coding: utf-8 -*-
"""-------------------------------------------------------
Created on Thu Nov  9 19:20:09 2017

@author: Cedric
-------------------------------------------------------"""

"""============================================================================
    Import Packages
============================================================================"""

from DataMeteo import DataMeteo
import pandas as pd
import utils_sidstorm as utils

"""============================================================================
    
============================================================================"""


path = "D:/Ced/Documents/UNIVERSITE/Cours/2017_M2-SID/sidstorm_meteo/data_cleaned/"

data_meteo = DataMeteo(path)

data_train, data_test = data_meteo.Export()
data_answer = data_meteo.answer

df1 = data_test.loc[14110:14130]
df2 = df1.apply(utils.Replace_Na)
df3 = df2.apply(utils.Scale_Floats, center = True, scale = False)

df3.mean()

data_meteo.find_insee("06")