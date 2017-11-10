# -*- coding: utf-8 -*-
"""-------------------------------------------------------
Created on Thu Nov  9 20:45:33 2017

@author: Cedric Bezy
-------------------------------------------------------"""

"""============================================================================
    Import Packages
============================================================================"""

import re
import pandas as pd
from numpy import nan
from datetime import datetime as dt

"""============================================================================
    
============================================================================"""
"""----------------------------------------------------
    Contains, begins by and ends_by
----------------------------------------------------"""
def Contains(pattern, x):
    ''' Is a pattern contained in x string ? '''
    ok = bool(re.search(str(pattern), str(x)))
    return ok

def BeginsBy(pattern, x):
    ''' Does pattern begin x string ? '''
    ok = Contains("^" + pattern, x)
    return ok

def EndsBy(pattern, x):
    ''' Does pattern ends x string ? '''
    ok = Contains(pattern + "$", x)
    return ok

"""----------------------------------------------------
    Convert String to Date and vice-versa
----------------------------------------------------"""
def StringToDate(s):
    ''' 
        Is a pattern contained in x ?
    '''
    ## formats
    fD = "[0-9][0-9]"
    fM = "[0-9][0-9]"
    fY = "[0-9][0-9][0-9][0-9]"
    ## events
    if Contains("{}/{}/{}".format(fD, fM, fY), s):
        res = dt.strptime(s, "%d/%m/%Y")
    elif Contains("{}-{}-{}".format(fY, fM, fD), s):
        res = dt.strptime(s, "%Y-%m-%d")
    else:
        res = nan
    ## results
    return res


def DateToString(date, tz = "%d/%m/%Y"):
    res = date.strftime(tz)
    return res

"""-------------------------------------
    Format of integers / numbers
-------------------------------------"""

def FormatInt(n, width):
    res = str(n).zfill(width)
    return res


def FormatFloat(x):
    if pd.isnull(x):
        res = nan
    elif Contains("[Ee]-1[0-9]+", str(x)):
        res = 0
    else:
        res = float(re.sub(",", ".", x))
    return res

"""============================================================================
    
============================================================================"""

"""-------------------------------------
    Concatenate Datas
-------------------------------------"""

def ConcatenateData(files, path = ""):
    resDf = pd.DataFrame()
    for f in files:
        iDf = pd.read_csv(path + f,
                          sep = ";",
                          decimal = ".")
        resDf = pd.concat([resDf, iDf])
        continue
    return resDf

"""-------------------------------------
    Replace NAs
-------------------------------------"""

def Replace_Na(x):
    if (x.dtype == "float"):
        res = x.fillna(x.mean(skipna = True))
    else:
        res = x
    return res

"""-------------------------------------
    Center / Scale
-------------------------------------"""
        
def Scale_Floats(x, center = False, scale = True):
    if (x.dtype == "float"):
        if (center):
            moy = x.mean(axis = 0, skipna = True)
            x = x - moy
        if (scale):
            stderr = x.std(axis = 0, skipna = True)
            x = x / stderr
    return x
        

