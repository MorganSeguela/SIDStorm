# -*- coding: utf-8 -*-
"""-------------------------------------------------------
Created on Sun Nov 12 00:53:26 2017

@author: Cedric Bezy
-------------------------------------------------------"""

"""============================================================================
    Import Packages
============================================================================"""

import re
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor
from datetime import datetime

import utils_meteo as utils

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
    Echeance Classif
----------------------------------------------------------------------------"""

nclech = 2

echtrain, echtest, clustech = utils.MakeEchClustering(
        dfTrain = data_train.drop(["tH2_obs", "dtH2"], axis = 1),
        dfTest = data_test,
        nclust = nclech
)

data_train["ech_clust"] = echtrain
data_test["ech_clust"] = echtest

"""----------------------------------------------------------------------------
    Select Variables
----------------------------------------------------------------------------"""

categ_dict = {"insee": list(data_train["insee"].cat.categories),
              "ech_clust": list(data_train["ech_clust"].cat.categories)}

dfCateg = utils.ExpandGrid(categ_dict)


x_vars = ["tH2",
          "tH2_YGrad",
          "flvis1SOL0",
          "huH2",
          "tH2_VGrad_2.100",
          "tpwHPA850",
          "flsen1SOL0",
          "fllat1SOL0",
          "ux1H10",
          "vx1H10"]

y_vars = "dtH2"


ETR = ExtraTreesRegressor(n_estimators = 500,
                          criterion = "mse")

RFR = RandomForestRegressor(criterion = "mse",
                            n_estimators = 500,
                            min_samples_split = 2,
                            min_samples_leaf = 2)

ABR = AdaBoostRegressor(loss = 'linear',
                        n_estimators = 500,
                        learning_rate = 0.2)

GBR = GradientBoostingRegressor(loss = 'ls',
                                learning_rate = 0.2,
                                n_estimators = 500,
                                max_depth = 10,
                                criterion = 'friedman_mse')

message = 'Insee = {} ; ech: clust {} / {}'

"""----------------------------------------------------------------------------
    Select Variables
----------------------------------------------------------------------------"""

## Init
dfAnswer = pd.DataFrame()
## Boucle
for index, row in dfCateg.iterrows():
    ## Select Features
    iInsee = row["insee"]
    iEch = row["ech_clust"]
    print(message.format(str(iInsee), str(iEch), str(nclech-1)))
    
    ## Select Rows
    oktrain = (data_train["ech_clust"] == iEch) & (data_train["insee"] == iInsee)
    oktest = (data_test["ech_clust"] == iEch) & (data_test["insee"] == iInsee)
    iDfTrain = data_train[oktrain]
    iDfTest = data_test[oktest]
    
    ##----------------------------------
    ## MAKE DATA
    ##----------------------------------
    ## Xtrain and X test
    Xtrain, Xtest = utils.Select_Variables(dfTrain = iDfTrain,
                                             dfTest = iDfTest,
                                             variables = x_vars,
                                             center_floats = True,
                                             scale_floats = True,
                                             max_pct_na = 0.3)
    ## Ytrain
    Ytrain = iDfTrain[y_vars]
    ## save dfTrain
    itH2 = iDfTest["tH2"]
    iDfAns = iDfTest[["date", "insee", "ech"]]
    
    ##----------------------------------
    ## MAKE DATA
    ##----------------------------------
    print("ExtraTrees")
    dtH2_ET = ETR.fit(Xtrain, Ytrain).predict(Xtest)[:]
    print("RandomForest")
    dtH2_RF = RFR.fit(Xtrain, Ytrain).predict(Xtest)[:]
    print("AdaBoosting")
    dtH2_AB = ABR.fit(Xtrain, Ytrain).predict(Xtest)[:]
    print("Grandient Boosting")
    dtH2_GB = GBR.fit(Xtrain, Ytrain).predict(Xtest)[:]
    
    iDfAns.is_copy = False
    iDfAns["tH2_ET"] = itH2 + dtH2_ET
    iDfAns["tH2_RF"] = itH2 + dtH2_RF
    iDfAns["tH2_AB"] = itH2 + dtH2_AB
    iDfAns["tH2_GB"] = itH2 + dtH2_GB
    ##----------------------------------
    ## MAKE DATA
    ##----------------------------------
    dfAnswer = pd.concat([dfAnswer, iDfAns], axis = 0)
    continue


"""---------------------------------------------
    Submission
---------------------------------------------"""

## Answer
dfAnswer = dfAnswer.sort_values(["ech", "date", "insee"])
dfAnswer["ech"] = dfAnswer["ech"].astype("int")
dfAnswer["insee"] = dfAnswer["insee"].astype("int")

## Today format
today = datetime.now().strftime("%Y%m%d_%H%M")
name_script = re.findall("/([^/]+)\.py", __file__)[0]

dfAnswer.to_csv(path_submit + "{}__{}.csv".format(name_script, today),
                sep = ";",
                decimal = ",",
                index = False)


