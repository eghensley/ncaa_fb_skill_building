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
from sklearn.neighbors import KNeighborsClassifier

#pca but isomap was close 

data = pd.read_csv('train_line_data.csv')
y = data['y']
x_feat = ['totalbasset', 'totalvs_top10', 'shareBDF', 'shareMOR', 'homeawaydiff', 'shareCGV', 'fieldeffect', 'diffsos', 'diffconsistency', 'difffut_sos', 'shareBIL', 'totalDES', 'difflast5', 'shareHOW', 'totalseas_sos', 'shareSAG', 'totalsos', 'shareMAS', 'totalfut_sos', 'diffMAS', 'sharePIG', 'diffSAG', 'shareDOK', 'diffBRN', 'shareDES', 'totalPIG', 'diffluck', 'totalluck', 'totallast5', 'shareARG', 'totalMAR', 'totalSAG', 'shareMAR', 'shareLAZ', 'totalARG', 'totallast10', 'totalCGV', 'totalBIL', 'diffBDF', 'diffseas_sos', 'diffCGV', 'totalpredictive', 'diffDOK', 'diffbasset', 'totalconsistency', 'shareBRN', 'totalBDF', 'sharebasset', 'diffMAR', 'diffvs_top10', 'diffpredictive', 'difflast10', 'totalMAS', 'diffHOW', 'totalBRN', 'totalHOW', 'diffDES', 'diffLAZ', 'diffBIL', 'diffMOR', 'totalMOR', 'diffPIG', 'totalDOK', 'diffARG', 'totalLAZ']
x = data[x_feat]

pipe = Pipeline([
    ('preprocess', MinMaxScaler()),
    ('reduce_dim', PCA(iterated_power=7, random_state = 86)),
    ('classify', KNeighborsClassifier())
])

N_FEATURES_OPTIONS = range(1, 40, 3)
scalers = [StandardScaler(), MinMaxScaler(), RobustScaler()]
param_grid = [
    {
        'reduce_dim__n_components': N_FEATURES_OPTIONS,
        'preprocess': scalers,
    },
]


reducer_labels = ['StandardScaler', 'MinMaxScaler', 'RobustScaler']

grid = GridSearchCV(pipe, cv=StratifiedKFold(n_splits = 40, shuffle = True, random_state = 86), n_jobs=-1, param_grid=param_grid, verbose = 4)
grid.fit(x, y)

mean_scores = np.array(grid.cv_results_['mean_test_score'])
mean_scores = mean_scores.reshape(1, -1, len(N_FEATURES_OPTIONS))
mean_scores = mean_scores.max(axis=0)
bar_offsets = (np.arange(len(N_FEATURES_OPTIONS)) *
               (len(reducer_labels) + 1) + .5)
list(mean_scores[0]).index(max(mean_scores[0]))
plt.figure()
COLORS = 'bgrcmyk'
for i, (label, reducer_scores) in enumerate(zip(reducer_labels, mean_scores)):
    plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])

plt.title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(reducer_labels) / 2, N_FEATURES_OPTIONS)
plt.ylabel('Digit classification accuracy')
plt.ylim((.45, .55))
plt.legend(loc='upper right')
