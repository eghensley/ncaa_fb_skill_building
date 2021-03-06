#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:47:07 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import lightgbm as lgb
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

 
np.random.seed(42)
data = pd.read_csv('train_ou_data.csv')
features = list(data)[1:]
#x_feat = features[:-1]
y = data['y']
juice = data['juice']
x_feat = ['totalbasset', 'totalvs_top10', 'shareBDF', 'shareMOR', 'homeawaydiff', 'shareCGV', 'fieldeffect', 'diffsos', 'diffconsistency', 'difffut_sos', 'shareBIL', 'totalDES', 'difflast5', 'shareHOW', 'totalseas_sos', 'shareSAG', 'totalsos', 'shareMAS', 'totalfut_sos', 'diffMAS', 'sharePIG', 'diffSAG', 'shareDOK', 'diffBRN', 'shareDES', 'totalPIG', 'diffluck', 'totalluck', 'totallast5', 'shareARG', 'totalMAR', 'totalSAG', 'shareMAR', 'shareLAZ', 'totalARG', 'totallast10', 'totalCGV', 'totalBIL', 'diffBDF', 'diffseas_sos', 'diffCGV', 'totalpredictive', 'diffDOK', 'diffbasset', 'totalconsistency', 'shareBRN', 'totalBDF', 'sharebasset', 'diffMAR', 'diffvs_top10', 'diffpredictive', 'difflast10', 'totalMAS', 'diffHOW', 'totalBRN', 'totalHOW', 'diffDES', 'diffLAZ', 'diffBIL', 'diffMOR', 'totalMOR', 'diffPIG', 'totalDOK', 'diffARG', 'totalLAZ']
x_feat = x_feat[:64]
x = data[x_feat]
scores = ['accuracy', 'roc_auc', 'f1_weighted', 'neg_log_loss']
N_FEATURES_OPTIONS = range(10, 210, 10)

pipe = Pipeline([
    ('preprocess', StandardScaler()),
    ('reduce_dim', PCA(random_state = 1108, n_components=17,whiten=True,svd_solver='full')),
    ('classify', lgb.LGBMClassifier(random_state = 86, objective = 'binary_logloss', n_estimators = 150, verbosity = 2, learning_rate = .021544346900318846))
])


param_grid = [
    {
        'classify__num_leaves': N_FEATURES_OPTIONS,     
    }
]


grid = GridSearchCV(pipe, cv=StratifiedKFold(n_splits = 50, shuffle = True, random_state = 1108), n_jobs=1, param_grid=param_grid, refit = False, scoring = scores, verbose = 3)
grid.fit(x, y.astype(int))


bestacc = 0.51087361749720395
bestf1 = 0
bestrocauc = 0
bestlogloss = -0.69741058838214331

results = grid.cv_results_
plt.figure(figsize=(10, 10))
plt.title("GridSearchCV evaluating using multiple scorers simultaneously",
          fontsize=16)

plt.xlabel("n features")
plt.ylabel("Score")
plt.grid()

ax = plt.axes()
ax.set_xlim(min(N_FEATURES_OPTIONS), max(N_FEATURES_OPTIONS)*3)
ax.set_ylim(.4, .8)

ax.axhline(y = bestacc, color = 'g', linestyle = ':')
ax.axhline(y = bestf1, color = 'k', linestyle = ':')
ax.axhline(y = bestrocauc, color = 'y', linestyle = ':')
ax.axhline(y = -1*bestlogloss, color = 'r', linestyle = ':')

# Get the regular numpy array from the MaskedArray
X_axis = np.array(results['param_classify__num_leaves'].data, dtype=float)

for scorer, color in zip(sorted(scores), ['g', 'k', 'r', 'y']):
    if scorer != 'neg_log_loss':
        for sample, style in (('train', '--'), ('test', '-')):
            sample_score_mean = results['mean_%s_%s' % (sample, scorer)]
            sample_score_std = results['std_%s_%s' % (sample, scorer)]
            ax.fill_between(X_axis, sample_score_mean - sample_score_std,
                            sample_score_mean + sample_score_std,
                            alpha=0.1 if sample == 'test' else 0, color=color)
            ax.plot(X_axis, sample_score_mean, style, color=color,
                    alpha=1 if sample == 'test' else 0.7,
                    label="%s (%s)" % (scorer, sample))
        best_index = np.nonzero(results['rank_test_%s' % scorer] == 1)[0][0]
        best_score = results['mean_test_%s' % scorer][best_index]
    
        # Plot a dotted vertical line at the best score for that scorer marked by x
        ax.plot([X_axis[best_index], ] * 2, [0, best_score],
                linestyle='-.', color=color, marker='x', markeredgewidth=3, ms=8)
    
        # Annotate the best score for that scorer
        ax.annotate("%0.2f" % best_score,
                    (X_axis[best_index], best_score + 0.005))
    
    elif scorer == 'neg_log_loss':
        for sample, style in (('train', '--'), ('test', '-')):
            samplemean = results['mean_%s_%s' % (sample, scorer)]
            sample_score_mean = []
            for each in samplemean:
                sample_score_mean.append(each * -1)
            sample_score_mean = np.array(sample_score_mean)
            samplestd = results['std_%s_%s' % (sample, scorer)]
            sample_score_std = []
            for each in samplestd:
                sample_score_std.append(each * -1)
            sample_score_std = np.array(sample_score_std)
            ax.fill_between(X_axis, sample_score_mean - sample_score_std,
                            sample_score_mean + sample_score_std,
                            alpha=0.1 if sample == 'test' else 0, color=color)
            ax.plot(X_axis, sample_score_mean, style, color=color,
                    alpha=1 if sample == 'test' else 0.7,
                    label="%s (%s)" % (scorer, sample))            

        best_index = np.nonzero(results['rank_test_%s' % scorer] == 1)[0][0]
        best_score = results['mean_test_%s' % scorer][best_index]
    
        # Plot a dotted vertical line at the best score for that scorer marked by x
        ax.plot([X_axis[best_index], ] * 2, [0, best_score*-1],
                linestyle='-.', color=color, marker='x', markeredgewidth=3, ms=8)
    
        # Annotate the best score for that scorer
        ax.annotate("%0.2f" % best_score,
                    (X_axis[best_index], best_score + 0.005))

plt.legend(loc="best")
plt.grid('off')
plt.show()


plt.figure(figsize=(10, 10))
plt.title("GridSearchCV evaluating using multiple scorers simultaneously",
          fontsize=16)

plt.xlabel("n features")
plt.ylabel("Score")
plt.grid()

ax = plt.axes()
ax.set_xlim(min(N_FEATURES_OPTIONS), max(N_FEATURES_OPTIONS))
ax.set_ylim(.47, .53)

ax.axhline(y = bestacc, color = 'g', linestyle = ':')
ax.axhline(y = bestf1, color = 'k', linestyle = ':')
ax.axhline(y = bestrocauc, color = 'y', linestyle = ':')
ax.axhline(y = -1*bestlogloss, color = 'r', linestyle = ':')

# Get the regular numpy array from the MaskedArray
X_axis = np.array(results['param_classify__num_leaves'].data, dtype=float)

for scorer, color in zip(sorted(scores), ['g', 'k', 'r', 'y']):
    if scorer != 'neg_log_loss':
        for sample, style in (('train', '--'), ('test', '-')):
            sample_score_mean = results['mean_%s_%s' % (sample, scorer)]
            sample_score_std = results['std_%s_%s' % (sample, scorer)]
            ax.fill_between(X_axis, sample_score_mean - sample_score_std,
                            sample_score_mean + sample_score_std,
                            alpha=0.1 if sample == 'test' else 0, color=color)
            ax.plot(X_axis, sample_score_mean, style, color=color,
                    alpha=1 if sample == 'test' else 0.7,
                    label="%s (%s)" % (scorer, sample))
        best_index = np.nonzero(results['rank_test_%s' % scorer] == 1)[0][0]
        best_score = results['mean_test_%s' % scorer][best_index]
    
        # Plot a dotted vertical line at the best score for that scorer marked by x
        ax.plot([X_axis[best_index], ] * 2, [0, best_score],
                linestyle='-.', color=color, marker='x', markeredgewidth=3, ms=8)
    
        # Annotate the best score for that scorer
        ax.annotate("%0.2f" % best_score,
                    (X_axis[best_index], best_score + 0.005))
    
    elif scorer == 'neg_log_loss':
        for sample, style in (('train', '--'), ('test', '-')):
            samplemean = results['mean_%s_%s' % (sample, scorer)]
            sample_score_mean = []
            for each in samplemean:
                sample_score_mean.append(each * -1)
            sample_score_mean = np.array(sample_score_mean)
            samplestd = results['std_%s_%s' % (sample, scorer)]
            sample_score_std = []
            for each in samplestd:
                sample_score_std.append(each * -1)
            sample_score_std = np.array(sample_score_std)
            ax.fill_between(X_axis, sample_score_mean - sample_score_std,
                            sample_score_mean + sample_score_std,
                            alpha=0.1 if sample == 'test' else 0, color=color)
            ax.plot(X_axis, sample_score_mean, style, color=color,
                    alpha=1 if sample == 'test' else 0.7,
                    label="%s (%s)" % (scorer, sample))            

        best_index = np.nonzero(results['rank_test_%s' % scorer] == 1)[0][0]
        best_score = results['mean_test_%s' % scorer][best_index]
    
        # Plot a dotted vertical line at the best score for that scorer marked by x
        ax.plot([X_axis[best_index], ] * 2, [0, best_score*-1],
                linestyle='-.', color=color, marker='x', markeredgewidth=3, ms=8)
    
        # Annotate the best score for that scorer
        ax.annotate("%0.2f" % best_score,
                    (X_axis[best_index], best_score + 0.005))

plt.legend(loc="best")
plt.grid('off')
plt.show()