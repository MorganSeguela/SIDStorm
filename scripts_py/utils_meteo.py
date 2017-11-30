# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Created on Thu Nov  9 20:45:33 2017

@author: Cedric Bezy

This script contains useful fonctions for the "meteo" challenge.
----------------------------------------------------------------------------"""

"""============================================================================
    Import Packages
============================================================================"""

import os
import re
import pandas as pd
import pandas.api.types as pdtypes
from numpy import nan
from datetime import datetime
import itertools as itt
from scipy.cluster import hierarchy

"""============================================================================
    Dict Iness
============================================================================"""

dict_insee = {"06": {"insee": 6088001, "ville": "Nice"},
              "31": {"insee": 31069001, "ville": "Toulouse-Blagnac"},
              "33": {"insee": 33281001, "ville": "Bordeaux-Merignac"},
              "35": {"insee": 35281001, "ville": "Rennes"},
              "59": {"insee": 59343001, "ville": "Lille-Lesquin"},
              "67": {"insee": 67124001, "ville": "Strasbourg-Entzheim"},
              "75": {"insee": 75114001, "ville": "Paris-Montsouris"}}
  
"""============================================================================
    Functions for simple types
============================================================================"""
"""----------------------------------------------------
    Contains, begins by and ends_by
----------------------------------------------------"""
def Contains(pattern, x):
    """ Is a pattern contained in x string ? """
    ok = bool(re.search(str(pattern), str(x)))
    return ok

def BeginsBy(pattern, x):
    """ Does pattern begin x string ? """
    ok = Contains('^' + pattern, x)
    return ok

def EndsBy(pattern, x):
    """ Does pattern ends x string ? """
    ok = Contains(pattern + '$', x)
    return ok

"""----------------------------------------------------
    Convert String to Date and vice-versa
----------------------------------------------------"""

def StringToDate(s):
    """ Transform s to Date """
    ## formats
    fD = '[0-9][0-9]'
    fM = '[0-9][0-9]'
    fY = '[0-9][0-9][0-9][0-9]'
    ## events
    if Contains('{}/{}/{}'.format(fD, fM, fY), s):
        res = datetime.strptime(s, '%d/%m/%Y')
    elif Contains('{}-{}-{}'.format(fY, fM, fD), s):
        res = datetime.strptime(s, '%Y-%m-%d')
    else:
        res = nan
    ## results
    return res


def DateToString(date, tz = '%d/%m/%Y'):
    """ Transform a date to string """
    res = date.strftime(tz)
    return res


def ConvertStrDate(s, tz):
    """Change the format of a date-string"""
    date = StringToDate(s)
    res = DateToString(date)
    return res
    

def Today(tz):
    """Change the format of a date-string"""
    res = datetime.now().strftime(tz)
    return res

"""-------------------------------------
    Format of integers / numbers
-------------------------------------"""

def FormatInt(n, width):
    """
        Transform an integer into string of a given width.
        FormatInt(7, 3) = '007'
    """
    if isinstance(n, list) or isinstance(n, pd.Series):
        res = [str(int(i)).zfill(width) for i in n]
    else:
        res = str(int(n)).zfill(width)
    return res


def FormatFloat(x):
    if pd.isnull(x):
        res = nan
    elif Contains('[Ee]-1[0-9]+', str(x)):
        res = 0
    else:
        res = float(re.sub(',', '.', x))
    return res

"""============================================================================
    Dimensions
============================================================================"""

def nrow(x):
    return x.shape[0]

def ncol(x):
    return x.shape[1]

def to_categ_series(x, index, categories):
    xcat = pd.Categorical(x, categories = categories)
    xseries = pd.Series(xcat, index = index)
    return xseries
    


"""============================================================================
    Functions for Data
============================================================================"""

def ImportData(path):
    """
        Descr: 
            Import train and test data contained in a file.
            Define types of specifical variables.
        In:
            - path : string, a path of localisation of files.
        Out :
            Two dataframes with the same structure : dfTrain, dfTest
    """
    ## List of files
    path = re.sub(r'[/]+$', '', path) + '/'
    vfiles = [(path + f) for f in os.listdir(path) if Contains('train_[0-9]+', f)]
    
    ## Train
    dict_dtypes = {'ddH10_rose4': 'category',
                   'insee': 'int',
                   'ech': 'int',
                   'mois': 'category'}
    ##----------------------------------
    ## Importation of Training Data
    ##----------------------------------
    dfTrain = pd.DataFrame()
    for f in vfiles:
        iDf = pd.read_csv(f,
                          sep = ';',
                          decimal = ',',
                          dtype = dict_dtypes,
                          parse_dates = True)
        dfTrain = pd.concat([dfTrain, iDf],
                            ignore_index = True)
        continue
    ##----------------------------------
    ## Categories
    ##----------------------------------
    ## Categories Ech
    vech = list(dfTrain["ech"].unique())
    vech.sort()
    vech = FormatInt(vech, 2)
    ## Categories Insee
    vinsee = list(dfTrain["insee"].unique())
    vinsee.sort()
    vinsee = FormatInt(vinsee, 8)
    ## Categories Mois
    vmois = ["janvier", "février", "mars", "avril", "mai", "juin",
             "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    
    ##----------------------------------
    ## Train : change 
    ##----------------------------------
    ## Train : Echeance
    dfTrain["ech"] = FormatInt(dfTrain["ech"], 2)
    dfTrain["ech"] = pd.Categorical(dfTrain["ech"], categories = vech)
    ## Train : Insee
    dfTrain["insee"] = FormatInt(dfTrain["insee"], 8)
    dfTrain["insee"] = pd.Categorical(dfTrain["insee"], categories = vinsee)
    ## Train : mois
    dfTrain["mois"] = pd.Categorical(dfTrain["mois"], categories = vmois)
    
    ## Sort
    dfTrain = dfTrain.sort_values(["ech", "date", "insee"]).reset_index(drop = True)
    
    ## Creation of dtH2
    dfTrain['dtH2'] = dfTrain['tH2_obs'] - dfTrain['tH2']
    
    ##----------------------------------
    ## IMPORTATION OF DATA TEST
    ##----------------------------------
    dfTest =  pd.read_csv(path + 'data_test.csv',
                             sep = ';',
                             decimal = ',',
                             dtype = dict_dtypes,
                             parse_dates = True)
    ## Test : Echeance
    dfTest["ech"] = FormatInt(dfTest["ech"], 2)
    dfTest["ech"] = pd.Categorical(dfTest["ech"], categories = vech)
    ## Test : Insee
    dfTest["insee"] = FormatInt(dfTest["insee"], 8)
    dfTest["insee"] = pd.Categorical(dfTest["insee"], categories = vinsee)
    ## Test : Mois
    dfTest["mois"] = pd.Categorical(dfTest["mois"], categories = vmois)
    
    ## Sort
    dfTest = dfTest.sort_values(["ech", "date", "insee"]).reset_index(drop = True)
    
    ##----------------------------------
    ## Best submission
    ##----------------------------------
    dfBest =  pd.read_csv(path + 'best_submission.csv',
                          sep = ';',
                          decimal = ',',
                          dtype = dict_dtypes,
                          parse_dates = True)
    
    dfBest["ech"] = FormatInt(dfBest["ech"], 2)
    dfBest["ech"] = pd.Categorical(dfBest["ech"], categories = vech)
    dfBest["insee"] = FormatInt(dfBest["insee"], 8)
    dfBest["insee"] = pd.Categorical(dfBest["insee"], categories = vinsee)
    
    ## Sort
    dfBest = dfBest.sort_values(["ech", "date", "insee"]).reset_index(drop = True)
    ##----------------------------------
    ## Results
    ##----------------------------------
    return dfTrain, dfTest, dfBest



"""============================================================================
    Iterations and classif Ech
============================================================================"""
"""-------------------------------------------------

-------------------------------------------------"""

def Chunk(x, size, padval = None):
    """
        Descr: 
            Divise x in n iterations. Each iter has with a given size.
            n = ceiling(x / size)
        In:
            - x: a list
            - size: a integer, size of each iteration
            - padval: if x / size is not an integer, some values are added
                to complete x.
        Out :
            a list of n iterations. 
        Dependency:
            - itertools
    """
    x = itt.chain(iter(x), itt.repeat(padval))
    res = iter(lambda: tuple(itt.islice(x, size)), (padval,) * size)
    return list(res)


"""-------------------------------------------------

-------------------------------------------------"""

def ExpandGrid(dictvar):
    """
        Equivaut a la fonction "expand.grid" de R
    """
    ## longueur
    names = dictvar.keys()
    values = dictvar.values()
    ## make all possibilites with
    rows = list(itt.product(*values))
    ## make data frazme
    resDf = pd.DataFrame.from_records(rows, columns = names)
    return resDf


"""============================================================================
    Classif Ech
============================================================================"""

def Cluster_Ech(df, ech, nclust, dendro = False):
    """
        Make a classifier from ech, with Hierarchy Clustering
    """
    dfx = df.loc[:, df.dtypes == "float"]
    dfx = pd.concat([dfx, ech], axis = 1)
    dfMeans = dfx.groupby("ech").mean()
    matDist = hierarchy.linkage(dfMeans, 'ward', 'euclidean')
    ## Dendrogramme
    if dendro:
        hierarchy.dendrogram(matDist)
    ## Cut    
    clusters_ls = list(hierarchy.cut_tree(matDist, nclust)[:,0])
    groups = [i for i in range(nclust)]
    clust_cat = to_categ_series(clusters_ls,
                                index = ech.cat.categories,
                                categories = groups)
    ## Result
    return clust_cat


"""-------------------------------------------------

-------------------------------------------------"""

def MakeEchClustering(dfTrain, dfTest, nclust):
    """
    """
    cluster = Cluster_Ech(dfTrain, dfTrain["ech"], nclust, False)
    echtrain = dfTrain["ech"]
    echtest = dfTest["ech"]
    ## Echantillon
    for i in cluster.index:
        echtrain = echtrain.replace(i, cluster[i])
        echtest = echtest.replace(i, cluster[i])
        continue
    
    echtrain = echtrain.astype("category")
    echtest = echtest.astype("category")
    ## Result
    return echtrain, echtest, cluster


"""============================================================================
    Functions for Data
============================================================================"""
"""-------------------------------------
    Replace NAs
-------------------------------------"""

def Replace_Na(x):
    """
        X is a series.
        If x contains floats, missing values are replaced by its mean.
    """
    if (x.dtype == 'float'):
        res = x.fillna(x.mean(skipna = True))
    else:
        res = x
    return res

"""-------------------------------------
    Center / Scale
-------------------------------------"""
        
def Scale_Floats(x, center = True, scale = True):
    """
        X is a floating series.
        If 'center' is True:
            x is centered: x = x - mean(x)
        If 'scale' is True:
            x is scaled: x = x / std(x)
    """
    if (x.dtype == 'float'):
        if (center):
            moy = x.mean(axis = 0, skipna = True)
            x = x - moy
        if (scale):
            stderr = x.std(axis = 0, skipna = True)
            x = x / stderr
    return x

"""-------------------------------------
    Select 
-------------------------------------"""
        
def Select_Variables(dfTrain,
                     dfTest,
                     variables = [],
                     center_floats = True,
                     scale_floats = True,
                     max_pct_na = 0.3):
    """
        Descr: 
            To do machine learning, we need to have two data (train and test)
            with the same structure.
            Some variables must be centered and scaled. In this case,
            test's variables must be scaled with train's features,
            in order to not to slant prediction.
        In:
            - dfTrain : dataframe for training
            - dfTest : dataframe for tests
            - variables : list of UNCHANGED variables to select.
            - scales : list of centered-and-scaled float variables to select.
                If one of those variables is not a float, its unchanged !
                
        Note :
            If a name in 'variables' or 'scales' does not exists in dfTrain or
            dfTest, then a error will be returned !
            
        Out :
            Two dataframes with the same structure : resTrain, resTest
    """
    msgerr = "'{}' is not contained in {} !"
    ## Init
    resTrain = pd.DataFrame(index = dfTrain.index)
    resTest = pd.DataFrame(index = dfTest.index)
    ## Boucle
    for ivar in variables:
        ## Errors
        if not (ivar in list(dfTrain)):
            raise ValueError(msgerr.format(ivar, 'dfTrain'))
        elif not (ivar in list(dfTest)):
            raise ValueError(msgerr.format(ivar, 'dfTest'))
        xtrain = dfTrain[ivar]
        xtest = dfTest[ivar]
        ## if differents types : error
        if (xtrain.dtype != xtest.dtype):
            raise ValueError('''Variable {} is not of the same type in
                             dfTrain and in dfTest !'''.format(ivar))
        ## if too many missing values
        pct_na_train = xtrain.isnull().mean()
        pct_na_test = xtest.isnull().mean()
        
        if (pct_na_train <= max_pct_na and pct_na_test <= max_pct_na):
            ## Tests on types
            is_num = pdtypes.is_numeric_dtype(xtrain)
            is_str = pdtypes.is_categorical_dtype(xtrain) or pdtypes.is_string_dtype(xtrain)
            ## IF FLOAT
            if is_num:
                ## Mean Features
                moy = xtrain.mean()
                stderr = xtrain.std()
                ## Dont take useless variables
                ## having no variation, or too much NA
                if (stderr != 0):
                    xtrain = xtrain.fillna(moy)
                    xtest = xtest.fillna(xtest.mean())
                    if center_floats:
                        xtrain -= moy
                        xtest -= moy
                    if scale_floats:
                        xtrain /= stderr
                        xtest /= stderr
                    ## Add to Data
                    resTrain[ivar] = pd.Series(xtrain, index = dfTrain.index)
                    resTest[ivar] = pd.Series(xtest, index = dfTest.index)  
            ## IF CATEG
            elif is_str:
                iDummTrain = pd.get_dummies(xtrain, prefix = ivar)
                iDummTest = pd.get_dummies(xtest, prefix = ivar)
                resTrain = pd.concat([resTrain, iDummTrain], axis = 1)
                resTest = pd.concat([resTest, iDummTest], axis = 1)
        continue
    
    ## Results
    return resTrain, resTest

    
    
"""============================================================================
    Submit Prediction
============================================================================"""

def Submit(dfAnswer, name_file, path):
    ## Today format
    path = re.sub(r'[/]+$', '', path) + '/'
    ## Today format
    today = datetime.now().strftime("%Y%m%d_%H%M")
    ## dfAnswer
    dfAnswer = dfAnswer.sort_values(["ech", "date", "insee"])
    dfAnswer["ech"] = dfAnswer["ech"].astype("int")
    dfAnswer["insee"] = dfAnswer["insee"].astype("int")
    
    dfAnswer.to_csv(path + "{}__{}.csv".format(name_file, today),
                    sep = ";",
                    decimal = ",",
                    index = False)
    return None

    


    
    
    
    
    