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
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, QuantileTransformer, Normalizer
import pandas as pd
from sklearn.svm import LinearSVC

#pca but isomap was close 

data = pd.read_csv('train_ml_data.csv')
y = data['y']
x_feat = ['totalbasset', 'totalvs_top10', 'shareBDF', 'shareMOR', 'homeawaydiff', 'shareCGV', 'fieldeffect', 'diffsos', 'diffconsistency', 'difffut_sos', 'shareBIL', 'totalDES', 'difflast5', 'shareHOW', 'totalseas_sos', 'shareSAG', 'totalsos', 'shareMAS', 'totalfut_sos', 'diffMAS', 'sharePIG', 'diffSAG', 'shareDOK', 'diffBRN', 'shareDES', 'totalPIG', 'diffluck', 'totalluck', 'totallast5', 'shareARG', 'totalMAR', 'totalSAG', 'shareMAR', 'shareLAZ', 'totalARG', 'totallast10', 'totalCGV', 'totalBIL', 'diffBDF', 'diffseas_sos', 'diffCGV', 'totalpredictive', 'diffDOK', 'diffbasset', 'totalconsistency', 'shareBRN', 'totalBDF', 'sharebasset', 'diffMAR', 'diffvs_top10', 'diffpredictive', 'difflast10', 'totalMAS', 'diffHOW', 'totalBRN', 'totalHOW', 'diffDES', 'diffLAZ', 'diffBIL', 'diffMOR', 'totalMOR', 'diffPIG', 'totalDOK', 'diffARG', 'totalLAZ']
x = data[x_feat]
#SelectKBest(chi2, k=6).fit_transform(x,y)
#
#x = StandardScaler().fit_transform(x)
#x = MinMaxScaler().fit_transform(x)
pipe = Pipeline([
    ('preprocess', MinMaxScaler()),
    ('reduce_dim', PCA(iterated_power=7, random_state = 86)),
    ('classify', LinearSVC(random_state = 1108))
])

N_FEATURES_OPTIONS = range(2, 28)
C_OPTIONS = np.logspace(-3,3,8)
#N_FEATURES_OPTIONS = [StandardScaler(), MinMaxScaler(), RobustScaler(), QuantileTransformer(), Normalizer()]
param_grid = [
    {
        'reduce_dim__n_components': N_FEATURES_OPTIONS,
        'preprocess': [StandardScaler(), MinMaxScaler(), RobustScaler(), QuantileTransformer(random_state = 46), Normalizer()],
        'classify__C': C_OPTIONS,
    },
]


reducer_labels = ['StandardScaler', 'MinMaxScaler', 'RobustScaler', 'QuantileTransformer', 'Normalizer']

grid = GridSearchCV(pipe, cv=StratifiedKFold(n_splits = 50, shuffle = True, random_state = 86), n_jobs=-1, param_grid=param_grid, verbose = 4, scoring = ['neg_log_loss', 'accuracy'])
grid.fit(x, y)

#grid.cv_results_[mean_test_scre_accuracy]
mean_scores = np.array(grid.cv_results_['mean_test_score'])
# scores are in the order of param_grid iteration, which is alphabetical
mean_scores = mean_scores.reshape(len(C_OPTIONS), -1, len(N_FEATURES_OPTIONS))
# select score for best C
mean_scores = mean_scores.max(axis=0)
bar_offsets = (np.arange(len(N_FEATURES_OPTIONS)) *
               (len(reducer_labels) + 1) + .5)
list(mean_scores[0]).index(max(mean_scores[0]))
#max(mean_scores[0]) = .7471576446631597
plt.figure()
COLORS = 'bgrcmyk'
for i, (label, reducer_scores) in enumerate(zip(reducer_labels, mean_scores)):
    plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])

plt.title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(reducer_labels) / 2, N_FEATURES_OPTIONS)
plt.ylabel('Digit classification accuracy')
plt.ylim((.7, .8))
plt.legend(loc='upper right')
