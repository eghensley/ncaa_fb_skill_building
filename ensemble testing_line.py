# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:56:49 2017

@author: Eric
"""

import numpy as np
import pandas as pd
import tuned_line_models
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.utils import resample
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelBinarizer

data = pd.read_csv('train_line_data.csv')
y = data['y']
x_feat = list(data)[1:66]
x = data[x_feat]


tuned = tuned_line_models.allmodels()
hard_voting = VotingClassifier(estimators = tuned, voting='hard')
soft_voting = VotingClassifier(estimators = tuned, voting = 'soft')

names = []
models = []
names.append('soft_voting')
models.append(soft_voting)
for name, model in tuned:
    names.append(name)
    models.append(model)
names.append('Dummy')
models.append(DummyClassifier())
data = pd.read_csv('train_ml_data.csv')
y = data['y']
x_feat = list(data)[1:66]
x = data[x_feat]

scorelist = ['neg_log_loss', 'accuracy', 'f1_weighted', 'roc_auc', 'precision', 'recall']
params = [{'classifier':models}]
pipe = Pipeline([('classifier',DummyClassifier())])
grid = GridSearchCV(pipe, cv=KFold(n_splits = 10, shuffle = True, random_state = 86), param_grid = params, n_jobs=1, refit = False, verbose = 4, scoring = scorelist)
grid.fit(x, y)

results = grid.cv_results_
scores = pd.DataFrame(columns = scorelist)
for metric in scorelist:
    score = results['mean_test_%s'%(metric)]
    scores[metric] = score    
scores = np.array(scores)
scores.to_csv('ml ensemnle results.csv')

modelscores = pd.DataFrame(columns = names)
values = []
for i in range(0, len(names)):
    for j in scorelist:
        values.append(scores[j][i])

print values
values = np.array(values).reshape(len(names), len(scorelist))

import matplotlib.pyplot as plt
bar_offsets = (np.arange(len(scorelist)) *
               (len(names) + 1) + .5)
plt.figure()
plt.figure(figsize=(10, 10))
COLORS = 'bgrcmykbgrcmyk'
for i, (label, reducer_scores) in enumerate(zip(scorelist, values)):
    plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])

plt.title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(scorelist) / 2, names)
plt.ylabel('Digit classification %s'%(score))
plt.ylim(.4, .8)
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


