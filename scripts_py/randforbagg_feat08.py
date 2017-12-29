  # -*- coding: utf-8 -*-
"""-------------------------------------------------------
Created on Sun Nov 12 00:53:26 2017

@author: Cedric Bezy
-------------------------------------------------------"""

"""============================================================================
    Import Packages
============================================================================"""

import re
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import train_test_split

import utils_meteo_v2 as utils

"""============================================================================
    Regression Lineaire
============================================================================"""

## Path
path_files = "D:/Ced/Documents/UNIVERSITE/Cours/2017_M2-SID/sidstorm_meteo/data_cleaned/"
## Submits
path_submit = "D:/Ced/Documents/UNIVERSITE/Cours/2017_M2-SID/sidstorm_meteo/submits/"

"""----------------------------------------------------------------------------
    Import Data
----------------------------------------------------------------------------"""

data_train, data_test, best_submit = utils.ImportData(path_files)

## Suppress Nan in tH2
data_train = data_train[pd.notnull(data_train["dtH2"])]

"""----------------------------------------------------------------------------
    Select Variables
----------------------------------------------------------------------------"""

x_vars = [
        'insee',
        'ech',
        'tH2',
        'tH2_VGrad_2.100',
        'tH2_XGrad',
        'tH2_YGrad',
        'capeinsSOL0',
        'fllat1SOL0',
        'flsen1SOL0',
        'hcoulimSOL0',
        'huH2',
        'ntSOL0_HMoy',
        'pMER0',
        'tpwHPA850',
        'ux1H10',
        'vapcSOL0',
        'vx1H10'
]

y_vars = 'dtH2'

## Today format
name_script = re.findall("/([^/]+)\.py", __file__)[0]


"""============================================================================
    RandomForest and Bagging
============================================================================"""


RFR = RandomForestRegressor(criterion = "mse",
                            n_estimators = 20,
                            min_samples_split = 2,
                            min_samples_leaf = 2)

BGR = BaggingRegressor(base_estimator = RFR,
                       n_estimators = 40)


    
##-------------------------------
## MAKE TRAIN AND TEST
##-------------------------------
## Xtrain and X test
Xtrain, Xtest = utils.Select_Variables(dfTrain = data_train,
                                       dfTest = data_test,
                                       variables = x_vars,
                                       center_floats = True,
                                       scale_floats = True,
                                       max_pct_na = 0.3)
## Ytrain
Ytrain = data_train[y_vars]

##-------------------------------
## MAKE PREDICTION
##-------------------------------
## save dfTrain
itH2 = data_test["tH2"]
dfAnswer = data_test[["date", "insee", "ech"]]
dfAnswer.is_copy = False

##-------------------------------
## MAKE PREDICTION
##-------------------------------
imat_rfbagg = pd.DataFrame(copy = False)
for i in range(3):
    print(i)
    bgfit = BGR.fit(Xtrain, Ytrain)
    imat_rfbagg[i] = pd.Series(bgfit.predict(Xtest)[:], index = Xtest.index)
    ## MAKE PREDICTION
    dtH2_rfbagg = imat_rfbagg.apply(np.mean, axis = 1)
    dfAnswer["tH2_obs"] = itH2 + dtH2_rfbagg
    ## SUBMISSION
    utils.Submit(dfAnswer,
                 name_file = name_script,
                 path = path_submit)
    continue







