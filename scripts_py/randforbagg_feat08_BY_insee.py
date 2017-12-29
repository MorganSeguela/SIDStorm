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

categ_dict = {"insee": list(data_train["insee"].cat.categories)}

dfCateg = utils.ExpandGrid(categ_dict)


x_vars = [
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
nrep = 5
message = '{} ; Insee = {}'

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
                       n_estimators = 50)


dfAnsw_rfbagg = pd.DataFrame()
## Boucle
for index, row in dfCateg.iterrows():
    ##-------------------------------
    ## MAKE SUBDATA
    ##-------------------------------
    ## Select Features
    iInsee = row["insee"]
    print(message.format("RandomForest_Bagging", str(iInsee)))
    
    ## Select Rows
    oktrain = (data_train["insee"] == iInsee)
    oktest = (data_test["insee"] == iInsee)
    iDfTrain = data_train[oktrain]
    iDfTest = data_test[oktest]
    
    ##-------------------------------
    ## MAKE TRAIN AND TEST
    ##-------------------------------
    ## Xtrain and X test
    Xtrain, Xtest = utils.Select_Variables(dfTrain = iDfTrain,
                                           dfTest = iDfTest,
                                           variables = x_vars,
                                           center_floats = True,
                                           scale_floats = True,
                                           max_pct_na = 0.3)
    ## Ytrain
    Ytrain = iDfTrain[y_vars]
    
    ##-------------------------------
    ## SELECTION OF VARIABLES
    ##-------------------------------
    ## Simul a feat
    feats_fit = RFR.fit(Xtrain, Ytrain)
    feats_weight = pd.Series(feats_fit.feature_importances_,
                             index = Xtrain.columns)
    select_feats = feats_weight[feats_weight > 0.01]
    
    Xtrain = Xtrain[select_feats.index]
    Xtest = Xtest[select_feats.index]
    
    
    ##-------------------------------
    ## MAKE PREDICTION
    ##-------------------------------
    ## save dfTrain
    itH2 = iDfTest["tH2"]
    inseeAnsw = iDfTest[["date", "insee", "ech"]]
    inseeAnsw.is_copy = False
    
    ##-------------------------------
    ## MAKE PREDICTION
    ##-------------------------------
    imat_rfbagg = pd.DataFrame(copy = False)
    for i in range(nrep):
        print(i)
        bgfit = BGR.fit(Xtrain, Ytrain)
        imat_rfbagg[i] = pd.Series(bgfit.predict(Xtest)[:], index = Xtest.index)
        continue
    dtH2_rfbagg = imat_rfbagg.apply(np.mean, axis = 1)
    
    ##-------------------------------
    ## MAKE PREDICTION
    ##-------------------------------
    inseeAnsw["tH2_obs"] = itH2 + dtH2_rfbagg
    dfAnsw_rfbagg = pd.concat([dfAnsw_rfbagg, inseeAnsw], axis = 0)
    continue

##-------------------------------
## SUBMISSION
##-------------------------------

utils.Submit(dfAnsw_rfbagg,
             name_file = name_script,
             path = path_submit)





