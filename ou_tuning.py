#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:55:19 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv('train_ou_data.csv')
y = data['y']
x_feat = ['totalbasset', 'totalvs_top10', 'shareBDF', 'shareMOR', 'homeawaydiff', 'shareCGV', 'fieldeffect', 'diffsos', 'diffconsistency', 'difffut_sos', 'shareBIL', 'totalDES', 'difflast5', 'shareHOW', 'totalseas_sos', 'shareSAG', 'totalsos', 'shareMAS', 'totalfut_sos', 'diffMAS', 'sharePIG', 'diffSAG', 'shareDOK', 'diffBRN', 'shareDES', 'totalPIG', 'diffluck', 'totalluck', 'totallast5', 'shareARG', 'totalMAR', 'totalSAG', 'shareMAR', 'shareLAZ', 'totalARG', 'totallast10', 'totalCGV', 'totalBIL', 'diffBDF', 'diffseas_sos', 'diffCGV', 'totalpredictive', 'diffDOK', 'diffbasset', 'totalconsistency', 'shareBRN', 'totalBDF', 'sharebasset', 'diffMAR', 'diffvs_top10', 'diffpredictive', 'difflast10', 'totalMAS', 'diffHOW', 'totalBRN', 'totalHOW', 'diffDES', 'diffLAZ', 'diffBIL', 'diffMOR', 'totalMOR', 'diffPIG', 'totalDOK', 'diffARG', 'totalLAZ']
x = data[x_feat]

pipe = Pipeline([
    ('a_preprocess', MinMaxScaler()),
    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
    ('c_classify', KNeighborsClassifier())
])

param_b = range(1, 6)
param_a = [StandardScaler(), MinMaxScaler(), RobustScaler()]
param_a_names = ['standard scaler', 'min max scaler', 'robust scaler']
param_grid = [
    {
        'a_preprocess': param_a,
        'b_reduce__n_components': param_b,
    },
]

scorelist = ['accuracy', 'f1_weighted', 'roc_auc', 'neg_log_loss']
grid = GridSearchCV(pipe, cv=KFold(n_splits = 10, shuffle = True, random_state = 86), refit = False, n_jobs=-1, param_grid=param_grid, verbose = 4, scoring = scorelist)
grid.fit(x, y)

for score in scorelist[:-1]:  
    scores_raw = (np.array(grid.cv_results_['mean_test_%s' % (score)]))
    scores = scores_raw.reshape(-1, len(param_b))
    bar_offsets = (np.arange(len(param_b)) *
                   (len(param_a) + 1) + .5)
    plt.figure()
    COLORS = 'bgrcmyk'
    for i, (label, reducer_scores) in enumerate(zip(param_a_names, scores)):
        plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])
    
    plt.title("Comparing feature reduction techniques")
    plt.xlabel('Reduced number of features')
    plt.xticks(bar_offsets + len(param_a) / 2, param_b)
    plt.ylabel('Digit classification accuracy')
    plt.ylim((min(scores_raw)*.95, max(scores_raw)*1.05))
    plt.legend(loc='best')


fig, ax1 = plt.subplots()    
scorecompilation = []
for score in scorelist:  
    if score != 'neg_log_loss':
        scores_raw = (np.array(grid.cv_results_['mean_test_%s' % (score)]))
        scorecompilation.append(scores_raw)
x1,x2,x3 = scorecompilation
meanscores = []
for i in range(0, len(x1)):
    meanscores.append(np.mean([x1[i], x2[i], x3[i]]))
meanscores = np.array(meanscores)    
meanscores = meanscores.reshape(-1, len(param_b))
bar_offsets = (np.arange(len(param_b)) *
               (len(param_a) + 1) + .5)
#plt.figure()
COLORS = 'bgrcmyk'
for i, (label, reducer_scores) in enumerate(zip(param_a_names, scores)):
    ax1.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])
ax1.set_title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(param_a) / 2, param_b)
ax1.set_ylabel('Combination Score')
ax1.set_ylim((min(scores_raw)*.95, max(scores_raw)*1.5))
plt.legend(loc='best')
logloss_raw = np.array(grid.cv_results_['mean_test_neg_log_loss'])*-1
logloss = logloss_raw.reshape(-1, len(param_b))
ax2 = ax1.twinx()
for i, log in enumerate(logloss):
    ax2.plot(bar_offsets + len(param_a) / 2, log, color = COLORS[i])
ax2.set_ylabel('Log Loss Score')
ax2.set_ylim((min(logloss_raw)*.9, max(logloss_raw)))
fig.tight_layout()
plt.show()

