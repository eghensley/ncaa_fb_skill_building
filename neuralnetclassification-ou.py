#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 10:34:10 2017

@author: eric.hensleyibm.com
"""


from keras import backend as K
import os
import importlib

def set_keras_backend(backend):
    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        importlib.reload(K)
        assert K.backend() == backend

set_keras_backend("theano")


import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split

np.random.seed(42)
data = pd.read_csv('train_ou_data.csv')
features = list(data)[1:]
#x_feat = features[:-1]
y = data['y']
juice = data['juice']
x_feat = ['totalbasset', 'totalvs_top10', 'shareBDF', 'shareMOR', 'homeawaydiff', 'shareCGV', 'fieldeffect', 'diffsos', 'diffconsistency', 'difffut_sos', 'shareBIL', 'totalDES', 'difflast5', 'shareHOW', 'totalseas_sos', 'shareSAG', 'totalsos', 'shareMAS', 'totalfut_sos', 'diffMAS', 'sharePIG', 'diffSAG', 'shareDOK', 'diffBRN', 'shareDES', 'totalPIG', 'diffluck', 'totalluck', 'totallast5', 'shareARG', 'totalMAR', 'totalSAG', 'shareMAR', 'shareLAZ', 'totalARG', 'totallast10', 'totalCGV', 'totalBIL', 'diffBDF', 'diffseas_sos', 'diffCGV', 'totalpredictive', 'diffDOK', 'diffbasset', 'totalconsistency', 'shareBRN', 'totalBDF', 'sharebasset', 'diffMAR', 'diffvs_top10', 'diffpredictive', 'difflast10', 'totalMAS', 'diffHOW', 'totalBRN', 'totalHOW', 'diffDES', 'diffLAZ', 'diffBIL', 'diffMOR', 'totalMOR', 'diffPIG', 'totalDOK', 'diffARG', 'totalLAZ']
x = data[x_feat[:61]]


N_FEATURES_OPTIONS = range(2, 61)
progress = 0
allaccuracy = []
alllogloss = []
for j in N_FEATURES_OPTIONS:
    allroc = []
    allf1 = []
    allnewlogloss = []
    score = None
    acc = []
    log_loss = []
    trainx, trainy, testx, testy, trainj, testj, model, pred = None, None, None, None, None, None, None, None
    for i in range(1,26):
        trainx, testx, trainy, testy, trainj, testj = train_test_split(x, y, juice, train_size = .9, test_size = .1, random_state = i, stratify = y)
        trainx = StandardScaler().fit_transform(trainx)
        testx = StandardScaler().fit_transform(testx)
        trainx = PCA(random_state = 1108, n_components=j,whiten=True,svd_solver='full').fit_transform(trainx)
        testx = PCA(random_state = 1108, n_components=j,whiten=True,svd_solver='full').fit_transform(testx)
        trainj = np.array(trainj)
        testj = np.array(testj)
        y_juice = []
        for every in range(0, len(np.array(testj))):
            ju = [testj[every]/200, -testj[every]/200]
            y_juice.append(ju)
        model = Sequential()
        model.add(Dense(j, input_shape=(j,), activation = 'relu'))
        model.add(Dropout(.8))
        model.add(Dense(1, activation = 'sigmoid'))
        model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
        model.fit(trainx, trainy, batch_size = 64, epochs = 75, verbose = 1)
        score = model.evaluate(testx, testy, batch_size = 64, verbose = 1)
        print(('%.2f percent complete') %  (float((float(progress)/(float(len(N_FEATURES_OPTIONS))*float(20)))*100)))
        progress += 1
        acc.append(score[1])
        log_loss.append(score[0])
    allaccuracy.append(np.mean(acc))
    alllogloss.append(np.mean(log_loss))

   
# 1 layer, .8 dropout, relu, adam, 75 epochs, 64 batch size, 12 pca
# logloss: 0.69328712578300689
# acc: 0.51007567422242617
 
    
    
fig, ax1 = plt.subplots()
plt.figure(figsize=(10, 10))
X_axis = N_FEATURES_OPTIONS
ax1.set_xlim(min(N_FEATURES_OPTIONS), max(N_FEATURES_OPTIONS))
ax1.axhline(y=.51007567422242617)
ax1.set_ylim(.47, .53)
ax1.plot(X_axis, allaccuracy, linestyle = ':', color='g')
besaccindex = allaccuracy.index(max(allaccuracy))
bestacc = allaccuracy[besaccindex]
ax1.plot([X_axis[besaccindex], ] * 2, [0, bestacc],
                linestyle='-.', color='g', marker='x', markeredgewidth=3, ms=8)

ax2 = ax1.twinx()
ax2.set_ylim(.69, .7)
ax2.axhline(y=.69328712578300689)
ax2.plot(X_axis, alllogloss, linestyle = '-', color='r')
besloglossindex = alllogloss.index(min(alllogloss))
bestlogloss = alllogloss[besloglossindex]
ax2.plot([X_axis[besloglossindex], ] * 2, [0, bestlogloss],
                linestyle='-.', color='r', marker='x', markeredgewidth=3, ms=8)
fig.tight_layout()
plt.show()
  



N_FEATURES_OPTIONS[allaccuracy.index(max(allaccuracy))]
allaccuracy[allaccuracy.index(max(allaccuracy))]
alllogloss[allaccuracy.index(max(allaccuracy))]
#alllogloss[11]
#allaccuracy[11]