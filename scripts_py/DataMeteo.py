# -*- coding: utf-8 -*-
"""-------------------------------------------------------
Created on Thu Nov  9 19:16:24 2017

@author: Cedric Bezy
-------------------------------------------------------"""

"""============================================================================
    Import Packages
============================================================================"""

import os
import re
import pandas as pd
import utils_sidstorm as utils
from dict_insee import dict_insee

"""============================================================================
    
============================================================================"""


class DataMeteo:
    def __init__(self, path):
        path = re.sub(r"[/\\]+$", "", path) + "/"
        self.train = pd.read_csv(path + "data_train.csv",
                                 sep = ";",
                                 encoding = "latin-1")
        self.test = pd.read_csv(path + "data_test.csv",
                                 sep = ";",
                                 encoding = "latin-1")
        self.answer = pd.read_csv(path + "data_answer.csv",
                                 sep = ";",
                                 encoding = "latin-1")
        self.insee = dict_insee
    
    ## Find Insee number
    def Find_insee(self, x):
        if utils.Contains("^[0-9]+$", str(x)):
            x = str(int(x)) ## supression 0 inutile
            res = [k for k in self.insee.keys() if utils.Contains("^" + x, k)]
            if (len(res) == 1):
                res = res[0]
        else:
            res = x
        ## results
        return res
    
    
    ## Export
    def Export(self, insee = [], ech = []):
        return self.train, self.test
    
    ## Submit
    def Submit(self, prediction):
        resDf = pd.merge(left = self.answer[["date", "insee", "ech"]],
                         right = prediction[["date", "insee", "ech", "tH2_obs"]],
                         on = [["date", "insee", "ech"]])
        return resDf
    
