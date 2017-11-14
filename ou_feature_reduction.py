#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:55:19 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd
from sklearn.svm import SVC


data = pd.read_csv('train_ou_data.csv')
y = data['y']
x_feat = ['totalbasset', 'totalvs_top10', 'shareBDF', 'shareMOR', 'homeawaydiff', 'shareCGV', 'fieldeffect', 'diffsos', 'diffconsistency', 'difffut_sos', 'shareBIL', 'totalDES', 'difflast5', 'shareHOW', 'totalseas_sos', 'shareSAG', 'totalsos', 'shareMAS', 'totalfut_sos', 'diffMAS', 'sharePIG', 'diffSAG', 'shareDOK', 'diffBRN', 'shareDES', 'totalPIG', 'diffluck', 'totalluck', 'totallast5', 'shareARG', 'totalMAR', 'totalSAG', 'shareMAR', 'shareLAZ', 'totalARG', 'totallast10', 'totalCGV', 'totalBIL', 'diffBDF', 'diffseas_sos', 'diffCGV', 'totalpredictive', 'diffDOK', 'diffbasset', 'totalconsistency', 'shareBRN', 'totalBDF', 'sharebasset', 'diffMAR', 'diffvs_top10', 'diffpredictive', 'difflast10', 'totalMAS', 'diffHOW', 'totalBRN', 'totalHOW', 'diffDES', 'diffLAZ', 'diffBIL', 'diffMOR', 'totalMOR', 'diffPIG', 'totalDOK', 'diffARG', 'totalLAZ']
x = data[x_feat]

#1 feature, standard scaler
# 5 features, robust scaler

pipe = Pipeline([
    ('preprocess', RobustScaler()),
    ('reduce_dim', PCA(iterated_power=7, random_state = 86, n_components = 5)),
    ('classify',   SVC(kernel="rbf", random_state = 1108, C = .001))
])

#N_FEATURES_OPTIONS = range(1, 7)
scalers = [StandardScaler()]
Cs = np.logspace(-3, 2, 10)
param_grid = [
    {
        'reduce_dim__n_components': [1],
        'preprocess': [StandardScaler()],
        'classify__C': Cs
    },
    {
        'reduce_dim__n_components': [5],
        'preprocess': [RobustScaler()],
        'classify__C': Cs
    },
]


#reducer_labels = ['StandardScaler', 'MinMaxScaler', 'RobustScaler']

grid = GridSearchCV(pipe, cv=StratifiedKFold(n_splits = 40, shuffle = True, random_state = 86), n_jobs=-1, param_grid=param_grid, verbose = 4)
grid.fit(x, y)

#grid.cv_results_[mean_test_scre_accuracy]
mean_scores = np.array(grid.cv_results_['mean_test_score'])
# scores are in the order of param_grid iteration, which is alphabetical
mean_scores = mean_scores.reshape(1, -1, len(Cs))
# select score for best C
mean_scores = mean_scores.max(axis=0)
bar_offsets = (np.arange(len(Cs)) *
               (len(scalers) + 1) + .5)
list(mean_scores[0]).index(max(mean_scores[0]))
#max(mean_scores[0]) = .7471576446631597
plt.figure()
COLORS = 'bgrcmyk'
for i, (label, reducer_scores) in enumerate(zip(scalers, mean_scores)):
    plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])

plt.title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(scalers) / 2, Cs)
plt.ylabel('Digit classification accuracy')
plt.ylim((.45, .55))
plt.legend(loc='upper right')
