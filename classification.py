#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 10:34:10 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import lightgbm as lgm
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import StratifiedKFold

np.random.seed(42)
data = pd.read_csv('ncaadata.csv')
features = list(data)[1:]
x_feat = features[:-1]
x = data[x_feat]
y = data['y']


scores = ['accuracy', 'roc_auc', 'f1_weighted', 'neg_log_loss']
pipe = Pipeline([
    ('preprocess', StandardScaler()),
    ('reduce_dim', PCA(random_state = 1108, n_components=16,whiten=True,svd_solver='full')),
    ('classify', lgm.LGBMClassifier())
])
N_FEATURES_OPTIONS = range(2, 40)
param_grid = [
    {
        'reduce_dim__n_components': N_FEATURES_OPTIONS, 
    }
]


#pipe.fit(x, y.astype(int))
grid = GridSearchCV(pipe, cv=StratifiedKFold(n_splits = 30, shuffle = True, random_state = 1108), n_jobs=1, param_grid=param_grid, refit = False, scoring = scores)
grid.fit(x, y.astype(int))


results = grid.cv_results_
plt.figure(figsize=(10, 10))
plt.title("GridSearchCV evaluating using multiple scorers simultaneously",
          fontsize=16)

plt.xlabel("n features")
plt.ylabel("Score")
plt.grid()

ax = plt.axes()
ax.set_xlim(2, 40)
ax.set_ylim(.45, .8)

# Get the regular numpy array from the MaskedArray
X_axis = np.array(results['param_reduce_dim__n_components'].data, dtype=float)

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

