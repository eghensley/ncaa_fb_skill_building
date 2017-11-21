# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:56:49 2017

@author: Eric
"""

import pandas as pd
import tuned_ou_models
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, precision_score, recall_score

traindata = pd.read_csv('train_ou_data.csv')
trainy = traindata['y']
x_feat = list(traindata)[1:66]
trainx = traindata[x_feat]

testdata = pd.read_csv('test_ou_data.csv')
testy = testdata['y']
testx = testdata[x_feat]

tuned = tuned_ou_models.allmodels()
hard_voting = VotingClassifier(estimators = tuned, voting='hard')
soft_voting = VotingClassifier(estimators = tuned, voting = 'soft')

names = []
models = []
names.append('soft_voting')
models.append(soft_voting)
names.append('hard_voting')
models.append(hard_voting)
for name, model in tuned:
    names.append(name)
    models.append(model)
names.append('Dummy')
models.append(DummyClassifier())


scorelist = ['accuracy', 'f1_weighted', 'roc_auc', 'precision', 'recall']

acc = []
f1 = []
roc = []
prec = []
rec = []

for model in models:
    model.fit(trainx, trainy)
    pred = model.predict(testx)
    acc.append(accuracy_score(testy, pred))
    f1.append(f1_score(testy, pred))
    roc.append(roc_auc_score(testy, pred))
    prec.append(precision_score(testy, pred))
    rec.append(recall_score(testy, pred))

ouscores = pd.DataFrame()
ouscores['model'] = names
ouscores['accuracy'] = acc
ouscores['f1'] = f1
ouscores['roc_auc'] = roc
ouscores['precision'] = prec
ouscores['recall'] = rec


ouscores.to_csv('ou_test_scores.csv')