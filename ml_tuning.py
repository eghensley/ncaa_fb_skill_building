#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:55:19 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelBinarizer
import pandas as pd
import lightgbm as lgb
from sklearn.utils import resample

data = pd.read_csv('train_ml_data.csv')
df_majority = data[data.y==1]
df_minority = data[data.y==0]
df_minority_upsampled = resample(df_minority, 
                                 replace=True,     # sample with replacement
                                 n_samples=len(df_majority.y),    # to match majority class
                                 random_state=123) # reproducible results
df_upsampled = pd.concat([df_majority, df_minority_upsampled])
y = df_upsampled['y']
y = LabelBinarizer().fit_transform(y)
x_feat = ['totalbasset', 'totalvs_top10', 'shareBDF', 'shareMOR', 'homeawaydiff', 'shareCGV', 'fieldeffect', 'diffsos', 'diffconsistency', 'difffut_sos', 'shareBIL', 'totalDES', 'difflast5', 'shareHOW', 'totalseas_sos', 'shareSAG', 'totalsos', 'shareMAS', 'totalfut_sos', 'diffMAS', 'sharePIG', 'diffSAG', 'shareDOK', 'diffBRN', 'shareDES', 'totalPIG', 'diffluck', 'totalluck', 'totallast5', 'shareARG', 'totalMAR', 'totalSAG', 'shareMAR', 'shareLAZ', 'totalARG', 'totallast10', 'totalCGV', 'totalBIL', 'diffBDF', 'diffseas_sos', 'diffCGV', 'totalpredictive', 'diffDOK', 'diffbasset', 'totalconsistency', 'shareBRN', 'totalBDF', 'sharebasset', 'diffMAR', 'diffvs_top10', 'diffpredictive', 'difflast10', 'totalMAS', 'diffHOW', 'totalBRN', 'totalHOW', 'diffDES', 'diffLAZ', 'diffBIL', 'diffMOR', 'totalMOR', 'diffPIG', 'totalDOK', 'diffARG', 'totalLAZ']
x = df_upsampled[x_feat]
#x,xx,y,yy = train_test_split(x,y,train_size = .7, test_size = .3, random_state = 86, stratify = y)
y = np.ravel(y)

pipe = Pipeline([
    ('a_preprocess', StandardScaler()),
    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 32)),
    ('c_classify', lgb.LGBMClassifier(random_state = 46, learning_rate = .43939, n_estimators = 100, num_leaves= 750, max_depth = 20))
])
2**20
param_b = [75, 750, 7500, 75000]
param_a = ['tree']
param_a_names = param_a
param_grid = [
    {
        'c_classify__num_leaves': param_b,
    },
]

scorelist = ['accuracy', 'f1_weighted', 'roc_auc', 'neg_log_loss']
grid = GridSearchCV(pipe, cv=KFold(n_splits = 10, shuffle = True, random_state = 86), refit = False, n_jobs=-1, param_grid=param_grid, verbose = 4, scoring = scorelist)
grid.fit(x, y)

for score in scorelist[:-1]:  
    scores_raw = (np.array(grid.cv_results_['mean_test_%s' % (score)]))
    max_score = max(scores_raw)
    scores = scores_raw.reshape(-1, len(param_b))
    bar_offsets = (np.arange(len(param_b)) *
                   (len(param_a) + 1) + .5)
    plt.figure()
    plt.figure(figsize=(10, 10))
    COLORS = 'bgrcmykbgrcmyk'
    for i, (label, reducer_scores) in enumerate(zip(param_a_names, scores)):
        plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])
        if max_score in reducer_scores:
            plt.axhline(y=max_score, linestyle=':', color=COLORS[i])
    plt.title("Comparing feature reduction techniques")
    plt.xlabel('Reduced number of features')
    plt.xticks(bar_offsets + len(param_a) / 2, param_b)
    plt.ylabel('Digit classification %s'%(score))
    plt.ylim((min(scores_raw)*.95, max(scores_raw)*1.05))
    plt.legend(loc='lower left')


fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)    
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
for i, (label, reducer_scores) in enumerate(zip(param_a_names, scores)):
    ax1.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])
ax1.set_title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(param_a) / 2, param_b)
ax1.set_ylabel('Combination Score')
ax1.set_ylim((min(scores_raw)*.95, max(scores_raw)*1.1))
plt.legend(loc='lower left')
logloss_raw = np.array(grid.cv_results_['mean_test_neg_log_loss'])*-1
logloss = logloss_raw.reshape(-1, len(param_b))
ax2 = ax1.twinx()
for i, log in enumerate(logloss):
    ax2.plot(bar_offsets + len(param_a) / 2, log, color = COLORS[i])
ax2.set_ylabel('Log Loss Score')
ax2.set_ylim((min(logloss_raw)*.9, max(logloss_raw)))
fig.tight_layout()
plt.show()


