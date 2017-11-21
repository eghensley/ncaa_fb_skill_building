# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:56:49 2017

@author: Eric
"""

import pandas as pd
import tuned_ml_models
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, precision_score, recall_score
from sklearn.preprocessing import LabelBinarizer
from sklearn.utils import resample
import numpy as np

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
trainx = df_upsampled[x_feat]
trainy = np.ravel(y)

testdata = pd.read_csv('test_ml_data.csv')
testy = testdata['y']
testx = testdata[x_feat]

tuned = tuned_ml_models.allmodels()
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

mlscores_resample = pd.DataFrame()
mlscores_resample['model'] = names
mlscores_resample['accuracy'] = acc
mlscores_resample['f1'] = f1
mlscores_resample['roc_auc'] = roc
mlscores_resample['precision'] = prec
mlscores_resample['recall'] = rec

mlscores_resample.to_csv('ml_test_scores.csv')