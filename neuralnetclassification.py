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

##K.set_epsilon(1e-15)
#_EPSILON = K.epsilon()
#
#
#
#def _loss_tensor(juice):
#    def loss(y_true, y_pred, batch_size):
#        y_pred = y_pred + juice
#        y_pred = K.clip(y_pred, _EPSILON, 1.0-_EPSILON)
#        out = -(y_true * K.log(y_pred) + (1.0 - y_true) * K.log(1.0 - y_pred))
#        loss = K.mean(out, axis=-1)
#        return loss
#    return loss
##def _loss_tensor(y_true, y_pred):
##    y_pred = K.clip(y_pred, _EPSILON, 1.0-_EPSILON)
##    out = -(y_true * K.log(y_pred) + (1.0 - y_true) * K.log(1.0 - y_pred))
##    loss = K.mean(out, axis=-1)
##    return loss



np.random.seed(42)
data = pd.read_csv('train_line_data.csv')
features = list(data)[1:]
x_feat = features[:-1]
x = data[x_feat]
y = data['y']
juice = data['juice']
N_FEATURES_OPTIONS = range(5, 30)
allaccuracy = []
allroc = []
alllogloss = []
allf1 = []
for j in N_FEATURES_OPTIONS:
    score = None
    acc = []
    log_loss = []
    trainx, trainy, testx, testy, trainj, testj, model, pred = None, None, None, None, None, None, None, None
    for i in range(1,20):
        trainx, testx, trainy, testy, trainj, testj = train_test_split(x, y, juice, train_size = .9, random_state = i, stratify = y)
        trainx = StandardScaler().fit_transform(trainx)
        testx = StandardScaler().fit_transform(testx)
        trainx = PCA(random_state = 1108, n_components=j,whiten=True,svd_solver='full').fit_transform(trainx)
        testx = PCA(random_state = 1108, n_components=j,whiten=True,svd_solver='full').fit_transform(testx)
        trainj = np.array(trainj)
        testj = np.array(testj)
        y_juice = []
        batch_nbr = 0
        batch_sz = 32
        for every in range(0, len(np.array(testj))):
            ju = [testj[every]/200, -testj[every]/200]
            y_juice.append(ju)
        model = Sequential()
        model.add(Dense(j, input_shape=(j,), activation = 'relu'))
        model.add(Dropout(.8))
        model.add(Dense(1, activation = 'sigmoid'))
        model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
        model.fit(trainx, trainy, batch_size = 32, epochs = 75, verbose = 2)
        score = model.evaluate(testx, testy, batch_size = batch_sz, verbose = 2)
        acc.append(score[1])
        log_loss.append(score[0])
    allaccuracy.append(np.mean(acc))
    alllogloss.append(np.mean(log_loss))

   
    
    
    
    
    
fig, ax1 = plt.subplots()
plt.figure(figsize=(10, 10))
X_axis = N_FEATURES_OPTIONS
ax1.set_xlim(min(N_FEATURES_OPTIONS), max(N_FEATURES_OPTIONS))
ax1.set_ylim(.47, .53)
ax1.plot(X_axis, allaccuracy, linestyle = ':', color='g')
besaccindex = allaccuracy.index(max(allaccuracy))
bestacc = allaccuracy[besaccindex]
ax1.plot([X_axis[besaccindex], ] * 2, [0, bestacc],
                linestyle='-.', color='g', marker='x', markeredgewidth=3, ms=8)

ax2 = ax1.twinx()
ax2.set_ylim(.69, .7)
ax2.plot(X_axis, alllogloss, linestyle = '-', color='r')
besloglossindex = alllogloss.index(min(alllogloss))
bestlogloss = alllogloss[besloglossindex]
ax2.plot([X_axis[besloglossindex], ] * 2, [0, bestlogloss],
                linestyle='-.', color='r', marker='x', markeredgewidth=3, ms=8)
fig.tight_layout()
plt.show()
  
