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


### Bayes: 0.50316455696202533, 0.49936708860759493
### Log: .49786628733997157
data = classificationdata()
xvars = list(data)[:-1]
data[xvars] = preprocessing.scale(data[xvars])

useset, holdoutset = train_test_split(data, test_size = .1, random_state = 1108)

solvers = ['newton-cg', 'lbfgs', 'liblinear', 'sag']
parameterscores = []

for x in solvers:
    modelscores = []
    for i in [35, 46, 71, 86, 88]:
        trainx, testx, trainy, testy = train_test_split(useset[xvars], useset['y'], test_size = .1, random_state = i)  
        trainx = preprocessing.scale(trainx)
        testx = preprocessing.scale(testx)
        model = LogisticRegression(solver=x)
        model.fit(trainx, trainy.astype(int))
        pred = model.predict(testx)
        score = accuracy_score(testy.astype(int), pred)
        modelscores.append(score)
    modelaverage = sum(modelscores)/len(modelscores)
    parameterscores.append(modelaverage)
    
model = LogisticRegression(solver = 'newton-cg')
xtrain = useset[xvars]
xtest = holdoutset[xvars]
ytrain = useset['y']
ytest = holdoutset['y']
xtrain = preprocessing.scale(xtrain)
xtest =  preprocessing.scale(xtest)
model.fit(xtrain, ytrain.astype(int))
prediction = model.predict(xtest)
finalaccuracyscore = accuracy_score(ytest.astype(int), prediction)