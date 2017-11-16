#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:55:19 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tuned_line_models import tuned_line_models
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from tuned_line_models import radar_factory
tuned = tuned_line_models().allmodels()
names = []
models = []
for model, name in tuned:
    names.append(name)
    models.append(model)
names.append('Dummy')
models.append(DummyClassifier())
data = pd.read_csv('train_line_data.csv')
y = data['y']
x_feat = list(data)[1:66]
x = data[x_feat]

scorelist = ['accuracy', 'f1_weighted', 'roc_auc', 'neg_log_loss', 'precision', 'recall']
params = [{'classifier':models}]
pipe = Pipeline([('classifier',DummyClassifier())])
grid = GridSearchCV(pipe, cv=KFold(n_splits = 50, shuffle = True, random_state = 86), param_grid = params, n_jobs=-1, refit = False, verbose = 4, scoring = scorelist)
grid.fit(x, y)

results = grid.cv_results_
scores = pd.DataFrame(columns = scorelist)
for metric in scorelist:
    score = results['mean_test_%s'%(metric)]
    scores[metric] = score    
scores = np.array(scores)




