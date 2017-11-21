#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:53:23 2017

@author: eric.hensleyibm.com
"""

target = 'line'


import pandas as pd
import tuned_ml_models 
import tuned_ou_models
import tuned_line_models
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, precision_score, recall_score, log_loss
import numpy as np
from gp import bayesian_optimisation

baselinescores = pd.read_csv('%s_test_scores.csv'%(target))
baselinescores = baselinescores[list(baselinescores)[1:]]
baselinescores = baselinescores.set_index('model')
traindata = pd.read_csv('train_%s_data.csv'%(target))
trainy = traindata['y']
x_feat = list(traindata)[1:66]
trainx = traindata[x_feat]
testdata = pd.read_csv('test_%s_data.csv'%(target))
testy = testdata['y']
testx = testdata[x_feat]

if target == 'line':
    tuned = tuned_line_models.allmodels()
elif target == 'ml':
    tuned = tuned_ml_models.allmodels()
elif target == 'ou':
    tuned = tuned_ou_models.allmodels()

scorelist = ['accuracy', 'f1_weighted', 'roc_auc', 'precision', 'recall', 'neg_log_loss']


print(baselinescores)

keeplist = []
names = []
models = []
acc = []
f1 = []
roc = []
prec = []
rec = []
logloss = []
combinationscore = []
for name, model in tuned:
    names.append(name)
    models.append(model)
for each in names:
    combinationscore.append(np.mean(baselinescores.loc[each]))

keeplist = []
for i, score in enumerate(combinationscore):
    if score > .5:
        keeplist.append(tuned[i])


def sample_loss(parameters):
    weights = []
    for each in parameters:
        weights.append(each)
    model = VotingClassifier(estimators = keeplist, weights = weights, voting = 'soft')
    model.fit(trainx, trainy)
    pred = model.predict(testx)
    acc = accuracy_score(testy, pred)
    print(acc)
    return acc
#    f1 = f1_score(testy, pred)
#    roc = roc_auc_score(testy, pred)
#    prec = precision_score(testy, pred)
#    rec = recall_score(testy, pred)
#    combination = np.mean([acc, f1, roc, prec, rec])
#    print(combination)
#    return combination

#start1  = [1,1,1,1,1,1]
#start2 = [1,2,3,4,5,6]
#weights = [start1, start2]
#for weight in weights:  
#    model = VotingClassifier(estimators = keeplist, weights = weight, voting = 'soft')
#    model.fit(trainx, trainy)
#    pred = model.predict(testx)
#    acc = accuracy_score(testy, pred)
#    f1 = f1_score(testy, pred)
#    roc = roc_auc_score(testy, pred)
#    prec = precision_score(testy, pred)
#    rec = recall_score(testy, pred)
#    combination = np.mean([acc, f1, roc, prec, rec])
#    print(combination)
    
    
    
bounds = np.array([[0, 5], [0, 5], [0, 5], [0, 5],[0, 5], [0, 5]])
start  = [[1,1,1,1,1,1]]

bayesian_optimisation(n_iters=30, 
                      sample_loss=sample_loss, 
                      bounds=bounds,
                      x0 = start)
            
        
scores = pd.DataFrame()
scores['threshold'] = threshold
scores['accuracy'] = acc
scores['f1'] = f1
scores['roc_auc'] = roc
scores['precision'] = prec
scores['recall'] = rec
scores['logloss'] = logloss

print(scores)