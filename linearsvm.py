# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 23:17:01 2017

@author: Eric
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
### SVC(C = .005, kernel = 'linear'), acc:  0.520410, roc: 0.519155, kappa:  0.038282, f1: 0.463038


data = classificationdata()
xvars = list(data)[:-1]

useset = data
#useset, holdoutset = train_test_split(data, test_size = .1, random_state = 1108)

#kernels = ['poly', 'rbf', 'sigmoid']
#Cs = [.01, .1, 1, 10]
#gammas = [.001, .01, .05, .1]


Cs = [.005, .01, .05]


end = len(Cs)*9
at = 0



parameterscores = pd.DataFrame()
k = 'linear'
for c in Cs:
    
    c = .0075
    modelaccuracy = []
    modelroc = []
    modelkappa = []
    modelf1 = []
    for i in [4, 35, 46, 71, 86, 88, 151, 1108, 2726]:    
        at += 1
        trainx, testx, trainy, testy = train_test_split(useset[xvars], useset['y'], test_size = .075, random_state = i)  
        trainx = preprocessing.scale(trainx)
        testx = preprocessing.scale(testx)
        model = SVC(random_state = i+1, C = c, kernel = k)
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
    parameterscores = parameterscores.append({'kernel':k, 'C':c, 'accuracy':modelaverageaccuracy, 'roc':modelaverageroc, 'kappa':modelaveragekappa, 'f1':modelaveragef1}, ignore_index = True)


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
parameterscores = parameterscores.append({'kernel':'baseline', 'C':'baseline', 'accuracy':modelaverageaccuracy, 'roc':modelaverageroc, 'kappa':modelaveragekappa, 'f1':modelaveragef1}, ignore_index = True)




accuracyparams = parameterscores[parameterscores['accuracy'] > parameterscores['accuracy'][15]]
rocparams = parameterscores[parameterscores['roc'] > parameterscores['roc'][15]]
kappaparams = parameterscores[parameterscores['kappa'] > parameterscores['kappa'][15]]
f1params = parameterscores[parameterscores['f1'] > parameterscores['f1'][15]]


allparams = pd.DataFrame()
allparams=allparams.append(accuracyparams, ignore_index = True)
allparams=allparams.append(rocparams, ignore_index = True)
allparams=allparams.append(kappaparams, ignore_index = True)
allparams=allparams.append(f1params, ignore_index = True)


print allparams