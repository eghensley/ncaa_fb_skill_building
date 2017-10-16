#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:17:24 2017

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

data = classificationdata()
xvars = list(data)[:-1]
data[xvars] = preprocessing.scale(data[xvars])

useset, holdoutset = train_test_split(data, test_size = .1, random_state = 1108)


modelscores = []
for i in [35, 46, 71, 86, 88]:
    trainx, testx, trainy, testy = train_test_split(useset[xvars], useset['y'], test_size = .1, random_state = i)
    trainx = preprocessing.scale(trainx)
    testx = preprocessing.scale(testx)
    model = GaussianNB()
    model.fit(trainx, trainy.astype(int))
    pred = model.predict(testx)
    score = accuracy_score(testy.astype(int), pred)
    modelscores.append(score)
modelaverage = sum(modelscores)/len(modelscores)