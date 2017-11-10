# -*- coding: utf-8 -*-
"""------------------------------------------
Created on Wed Nov  8 13:51:08 2017

@author: Cedric Bezy
-----------------------------------------"""

"""============================================================================
    Directories
============================================================================"""

## Directory of Projet
path_files = "D:/Ced/Documents/UNIVERSITE/Cours/2017_M2-SID/sidstorm_meteo/data_meteo/"

## Directory for input
path_output = "D:/Ced/Documents/UNIVERSITE/Cours/2017_M2-SID/sidstorm_meteo/data_cleaned/"

"""============================================================================
    Import Packages
============================================================================"""

import os
import re
import pandas as pd
import utils_sidstorm as utils
from shutil import copyfile

"""============================================================================
    Make Data
============================================================================"""

def CleanData(path):
    """
    """
    ## Directory
    allFiles_ls = os.listdir(path)
    """-----------------------------------------------
    Train File
    -----------------------------------------------"""
    format_train = r"^train_[0-9]+\.csv"
    trainFiles_ls = [f for f in allFiles_ls if bool(re.search(format_train, f))]
    
    trainDf = pd.DataFrame()
    for ifile in trainFiles_ls:
        ichemin = path + ifile
        iDf = pd.read_csv(ichemin,
                          sep = ";",
                          decimal = ",")
        trainDf = pd.concat([trainDf, iDf])
        continue
    
    ## Gestion des fichiers mal converties
    trainDf["insee"] = [utils.FormatInt(i, 8) for i in trainDf["insee"]]
    trainDf["ddH10_rose4"] = [float(x) for x in trainDf["ddH10_rose4"]]
    trainDf["flvis1SOL0"] = [float(x) for x in trainDf["flvis1SOL0"]]
    trainDf["date"] = [utils.StringToDate(x) for x in trainDf["date"]]
    ## Add dtH2
    trainDf["dtH2"] = trainDf["tH2_obs"] - trainDf["tH2"]
    
    
    trainDf = trainDf.sort_values(["date", "ech", "insee"])
    trainDf["date"] = [utils.DateToString(x, "%d/%m/%Y") for x in trainDf["date"]]
    trainDf.index = range(trainDf.shape[0])

    
    
    """-----------------------------------------------
        Test File
    -----------------------------------------------"""
    
    testDf = pd.read_csv(path_files + "test.csv",
                         sep = ";",
                         decimal = ",")
    
    ## Gestion des fichiers mal converties
    testDf["insee"] = [utils.FormatInt(i, 8) for i in testDf["insee"]]
    testDf["ddH10_rose4"] = [float(x) for x in testDf["ddH10_rose4"]]
    testDf["flvis1SOL0"] = [utils.FormatFloat(x) for x in testDf["flvis1SOL0"]]
    testDf["date"] = [utils.StringToDate(x) for x in testDf["date"]]
    
    # print(testDf.dtypes, "\n")
    testDf = testDf.sort_values(["date", "ech", "insee"])
    testDf["date"] = [utils.DateToString(x, "%d/%m/%Y") for x in testDf["date"]]
    testDf.index = range(testDf.shape[0])

    """-----------------------------------------------
        Test Answer File
    -----------------------------------------------"""
    
    answerDf = pd.read_csv(path_files + "test_answer_template.csv",
                           sep = ";",
                           decimal = ",")
    
    """-----------------------------------------------
        Result
    -----------------------------------------------"""
    return trainDf, testDf, answerDf

    
"""============================================================================
    Dict
============================================================================"""

dfTrain, dfTest, dfAnswer = CleanData(path_files)

dfTrain.to_csv(path_output + "data_train.csv",
               sep = ";",
               index = False)

dfTest.to_csv(path_output + "data_test.csv",
              sep = ";",
              index = False)

'''
dfAnswer.to_csv(path_output + "data_answer.csv",
               sep = ";",
               index = False,
               encoding='latin-1')
'''

copyfile(path_files + "test_answer_template.csv",
         path_output + "data_answer.csv")

