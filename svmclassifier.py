#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 16:18:41 2017

@author: eric.hensleyibm.com
"""

from classificationdata import classificationdata
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numpy import ravel
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

from sklearn.svm import SVC

### Bayes: 0.50316455696202533, 0.49936708860759493
### Log: .49786628733997157
### lin svm: 0.49644381223328593 SVC(C = 7.5, kernel = 'linear', gamma = 'auto')


data = classificationdata()
xvars = list(data)[:-1]

useset, holdoutset = train_test_split(data, test_size = .1, random_state = 1108)

#kernels = ['poly', 'rbf', 'sigmoid']
#Cs = [.01, .1, 1, 10]
#degrees = range(2,5)
#gammas = [.001, .01, .05, .1]


Cs = [5, 10, 20]
degrees = [3]
gammas = [.075, .1, .25]

parameterscores = pd.DataFrame()
end = len(Cs)*len(degrees)*len(gammas)*5
at = 0

for d in degrees:
#    for k in kernels:
        k = 'poly'
        for g in gammas:
            for c in Cs:
                modelaccuracy = []
                modelroc = []
                modelkappa = []
                modelf1 = []
                for i in [35, 46, 71, 86, 88]:    
                    at += 1
                    trainx, testx, trainy, testy = train_test_split(useset[xvars], useset['y'], test_size = .1, random_state = i)  
                    trainx = preprocessing.scale(trainx)
                    testx = preprocessing.scale(testx)
                    model = SVC(random_state = i+1, C = c, kernel = k, gamma = g, degree = d)
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
                    
                    print '%s complete' % ((float(at)/float(end))*100)
                modelaverageaccuracy = sum(modelaccuracy)/len(modelaccuracy)
                modelaverageroc = sum(modelroc)/len(modelroc)
                modelaveragekappa = sum(modelkappa)/len(modelkappa)
                modelaveragef1 = sum(modelf1)/len(modelf1)
                parameterscores = parameterscores.append({'kernel':k, 'C':c, 'gamma':g, 'degrees':d, 'accuracy':modelaverageaccuracy, 'roc':modelaverageroc, 'kappa':modelaveragekappa, 'f1':modelaveragef1}, ignore_index = True)

for i in [35, 46, 71, 86, 88]:    
    trainx, testx, trainy, testy = train_test_split(useset[xvars], useset['y'], test_size = .1, random_state = i)  
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
parameterscores = parameterscores.append({'kernel':'baseline', 'C':'baseline', 'gamma':'baseline', 'degrees':'baseline', 'accuracy':modelaverageaccuracy, 'roc':modelaverageroc, 'kappa':modelaveragekappa, 'f1':modelaveragef1}, ignore_index = True)






accuracyparams = parameterscores[parameterscores['accuracy'] > parameterscores['accuracy'][48]]
rocparams = parameterscores[parameterscores['roc'] > parameterscores['roc'][48]]
kappaparams = parameterscores[parameterscores['kappa'] > parameterscores['kappa'][48]]
f1params = parameterscores[parameterscores['f1'] > parameterscores['f1'][48]]


allparams = pd.DataFrame()
allparams=allparams.append(accuracyparams, ignore_index = True)
allparams=allparams.append(rocparams, ignore_index = True)
allparams=allparams.append(kappaparams, ignore_index = True)
allparams=allparams.append(f1params, ignore_index = True)


print allparams







    
model = SVC(C = 7.5, kernel = 'linear', gamma = 'auto')
xtrain = useset[xvars]
xtest = holdoutset[xvars]
ytrain = useset['y']
ytest = holdoutset['y']
xtrain = preprocessing.scale(xtrain)
xtest =  preprocessing.scale(xtest)
model.fit(xtrain, ytrain.astype(int))
prediction = model.predict(xtest)
finalaccuracyscore = accuracy_score(ytest.astype(int), prediction)