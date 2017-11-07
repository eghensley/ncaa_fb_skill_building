#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:23:12 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import pandas as pd
from classificationdata import classificationdata
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

np.random.seed(42)
traindata = pd.read_csv('train_line_data.csv')
testdata = pd.read_csv('test_line_data.csv')
features = list(traindata)[1:]
x_feat = features[:-2]
train_x = traindata[x_feat]
train_y = traindata['y']
train_juice = traindata['juice']
testdata = classificationdata('test')
test_x = testdata[x_feat]
test_y = testdata['y']
test_juice = testdata['juice']

model = LogisticRegression()
model.fit(train_x, train_y)



confidence_threshold = .56
bank = 1000

bankhistory = []
pred = None
inputdata = None
prediction = None
gamejuice = None
realwinner = None
risk = None
odds = None
for game in range(0, 238):
#    game = 7
    gamejuice = np.array(test_juice)[game]
    inputdata = np.array(test_x)[game]
    inputdata = inputdata.reshape(1,-1)
    pred = model.predict_proba(inputdata)
    if pred[0][0] > confidence_threshold - float(gamejuice)/200:
        prediction = 0
        risk = 110 - gamejuice
        realwinner = np.array(test_y)[game]
        if realwinner == prediction:
            bank += 100
        elif realwinner != prediction:
            bank -= risk
        bankhistory.append(bank)
    elif pred[0][1] > confidence_threshold + float(gamejuice)/200:
        prediction = 1
        risk = 110 + gamejuice
        realwinner = np.array(test_y)[game]
        if realwinner == prediction:
            bank += 100
        elif realwinner != prediction:
            bank -= risk
        bankhistory.append(bank)

plt.plot(bankhistory)   