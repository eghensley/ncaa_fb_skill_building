#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:17:08 2017

@author: eric.hensleyibm.com
"""


from classificationdata import classificationdata
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from numpy import ravel
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
import lightgbm as lgb



data = classificationdata()
xvars = list(data)[:-1]

useset = data


application = 'binary'
leaves = [20, 30, 50, 100, 150] # < 2^(max_depth) 
depth = [3, 5, 7, 9]
learn = .01
mbin = [100, 200, 300]
mleaf = [50, 100, 200, 500]
rounds = [50, 100, 200]



parameterscores = pd.DataFrame()
end = len(leaves)*len(depth)*len(rounds)*len(mleaf)*len(mbin)*9
at = 0

for mb in mbin:
    for l in leaves:
        for d in depth:
                for nr in rounds:
                    for ml in mleaf:
                        modelaccuracy = []
                        modelroc = []
                        modelkappa = []
                        modelf1 = []
                        for i in [4, 35, 46, 71, 86, 88, 151, 1108, 2726]:    
                            at += 1
                            trainx, testx, trainy, testy = train_test_split(useset[xvars], useset['y'], test_size = .075, random_state = i)  
                            trainx = preprocessing.scale(trainx)
                            testx = preprocessing.scale(testx)
                            
                            train_data=lgb.Dataset(trainx,label=trainy)
                            param = {'objective': application, 'min_data_in_leaf': ml, 'num_leaves': l, 'max_depth': d, 'learning_rate': learn, 'max_bin': mb, 'metric' : ['auc', 'binary_logloss']}
                            model = lgb.train(param, train_data, nr)
                            pred = model.predict(testx)
                            for i in range(0,len(pred)):
                                if pred[i]>=.5:       # setting threshold to .5
                                   pred[i]=1
                                else:  
                                   pred[i]=0
                            accuracy = accuracy_score(testy.astype(int), pred)
                            roc = roc_auc_score(testy.astype(int), pred)
                            kappa = cohen_kappa_score(testy.astype(int), pred)
                            f1 = f1_score(testy.astype(int), pred)                        
                            modelaccuracy.append(accuracy)
                            modelroc.append(roc)
                            modelkappa.append(kappa)
                            modelf1.append(f1)
                            
                            print '%s complete' % ((float(at)/float(end))*100)
                        modelaverageaccuracy = sum(modelaccuracy)/len(modelaccuracy)
                        modelaverageroc = sum(modelroc)/len(modelroc)
                        modelaveragekappa = sum(modelkappa)/len(modelkappa)
                        modelaveragef1 = sum(modelf1)/len(modelf1)
                        parameterscores = parameterscores.append({'mbin':mb, 'leaves':l, 'depth':d, 'rounds':nr, 'mleaf':ml, 'accuracy':modelaverageaccuracy, 'roc':modelaverageroc, 'kappa':modelaveragekappa, 'f1':modelaveragef1}, ignore_index = True)
    







modelaccuracy = []
modelroc = []
modelkappa = []
modelf1 = []
for i in [4, 35, 46, 71, 86, 88, 151, 1108, 2726]:    
    trainx, testx, trainy, testy = train_test_split(useset[xvars], useset['y'], test_size = .075, random_state = i)  
    trainx = preprocessing.scale(trainx)
    testx = preprocessing.scale(testx)
    model = GaussianNB()
    model.fit(trainx, trainy.astype(int))
    pred = model.predict(testx)
    accuracy = accuracy_score(testy.astype(int), pred)
    roc = roc_auc_score(testy.astype(int), pred)
    kappa = cohen_kappa_score(testy.astype(int), pred)
    f1 = f1_score(testy.astype(int), pred)
    modelaccuracy.append(accuracy)
    modelroc.append(roc)
    modelkappa.append(kappa)
    modelf1.append(f1)
    
modelaverageaccuracy = sum(modelaccuracy)/len(modelaccuracy)
modelaverageroc = sum(modelroc)/len(modelroc)
modelaveragekappa = sum(modelkappa)/len(modelkappa)
modelaveragef1 = sum(modelf1)/len(modelf1)
parameterscores = parameterscores.append({'features':'baseline', 'estimators':'baseline', 'depth':'baseline', 'split':'baseline', 'accuracy':modelaverageaccuracy, 'roc':modelaverageroc, 'kappa':modelaveragekappa, 'f1':modelaveragef1}, ignore_index = True)






#accuracyparams = parameterscores[parameterscores['accuracy'] > parameterscores['accuracy'][60]]
rocparams = parameterscores[parameterscores['roc'] > parameterscores['roc'][18]]
kappaparams = parameterscores[parameterscores['kappa'] > parameterscores['kappa'][18]]
f1params = parameterscores[parameterscores['f1'] > parameterscores['f1'][18]]


allparams = pd.DataFrame()
#allparams=allparams.append(accuracyparams, ignore_index = True)
allparams=allparams.append(rocparams, ignore_index = True)
allparams=allparams.append(kappaparams, ignore_index = True)
allparams=allparams.append(f1params, ignore_index = True)


print allparams
