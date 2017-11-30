# -*- coding: utf-8 -*-
"""-------------------------------------------------------
Created on Sun Nov 12 00:53:26 2017

@author: Cedric Bezy

Gradient Boosting
-------------------------------------------------------"""

"""============================================================================
    Import Packages
============================================================================"""

import re
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from datetime import datetime

import utils_meteo as utils

"""============================================================================
    Gradient Boosting
============================================================================"""

## Path
path_files = 'D:/Ced/Documents/UNIVERSITE/Cours/2017_M2-SID/sidstorm_meteo/data_cleaned/'
## Submits
path_submit = 'D:/Ced/Documents/UNIVERSITE/Cours/2017_M2-SID/sidstorm_meteo/submits/'

"""----------------------------------------------------------------------------
    Import Data
----------------------------------------------------------------------------"""

data_train, data_test, best_submit = utils.ImportData2(path_files)

"""----------------------------------------------------------------------------
    Clean Data
----------------------------------------------------------------------------"""

## Suppress Nan in tH2
data_train = data_train[pd.notnull(data_train['dtH2'])]
data_train = data_train[pd.notnull(data_train['ddH10_rose4'])]


"""----------------------------------------------------------------------------
    Selection of variables
----------------------------------------------------------------------------"""

## Variable Y
Y = data_train['dtH2']

## Variable X
select_vars = ['insee', 'ech', 'ddH10_rose4']

select_scales = ['tH2',
                 'tH2_VGrad_2.100',
                 'tH2_YGrad',
                 'capeinsSOL0',
                 'ddH10_rose4',
                 'ffH10',
                 'flir1SOL0',
                 'fllat1SOL0',
                 'flsen1SOL0',
                 'flvis1SOL0',
                 'hcoulimSOL0',
                 'huH2',
                 'iwcSOL0',
                 'nbSOL0_HMoy',
                 'nH20',
                 'ntSOL0_HMoy',
                 'pMER0',
                 'rr1SOL0',
                 'rrH20',
                 'tpwHPA850',
                 'ux1H10',
                 'vapcSOL0',
                 'vx1H10']


## X Train
Xtrain, Xtest = utils.Select_Variables(data_train,
                                       data_test,
                                       select_vars,
                                       select_scales,
                                       max_pct_na = 0.3)

"""----------------------------------------------------------------------------
    GRADIENT BOOSTING
----------------------------------------------------------------------------"""

gradboost = GradientBoostingRegressor(loss = 'ls',
                                      learning_rate = 0.1,
                                      n_estimators = 500,
                                      max_depth = 10,
                                      criterion = 'friedman_mse')


## fitting gradian boosting
gbfit = gradboost.fit(Xtrain, Y)

## Prediction
dtH2 = gbfit.predict(Xtest)[:]
tH2_obs = data_test['tH2'] + dtH2

"""----------------------------------------------------------------------------
    DATA ANSWER
----------------------------------------------------------------------------"""

## CREATE ANSWER
dfAnswer = data_test[['date', 'insee', 'ech']]
dfAnswer['tH2_obs'] = pd.Series(tH2_obs, index = data_test.index)
## Sort
dfAnswer = dfAnswer.sort_values(['ech', 'date', 'insee'])


"""----------------------------------------------------------------------------
    SUBMISSION
----------------------------------------------------------------------------"""

## Today format
name_script = re.findall('/([^/]+)\.py', __file__)[0]
today = datetime.now().strftime('%Y%m%d_%H%M')

dfAnswer.to_csv(path_submit + '{}__{}.csv'.format(name_script, today),
                sep = ';',
                decimal = ',',
                index = False)

