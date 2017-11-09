#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 00:29:57 2017

@author: eric.hensleyibm.com
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score

 
np.random.seed(42)
data = pd.read_csv('train_line_data.csv')
features = list(data)[1:]
#x_feat = features[:-1]
y = data['y']
juice = data['juice']
x_feat = ['difffut_sos', 'totalconsistency', 'diffconsistency', 'diffsos', 'homeawaydiff', 'diffvs_top10', 'fieldeffect', 'shareDES', 'totalvs_top10', 'diffseas_sos', 'totalfut_sos', 'shareMAR', 'shareDOK', 'totalbasset', 'totalluck', 'totalsos', 'shareBIL', 'totalMAR', 'sharePIG', 'shareMAS', 'diffluck', 'totalseas_sos', 'totalBIL', 'difflast5', 'shareLAZ', 'totalHOW', 'totalDES', 'diffMAS', 'shareCGV', 'sharebasset', 'shareMOR', 'shareSAG', 'difflast10', 'diffBIL', 'totalCGV', 'shareHOW', 'diffCGV', 'shareARG', 'totalLAZ', 'shareBDF', 'diffLAZ', 'diffpredictive', 'diffMAR', 'totallast5', 'diffPIG', 'diffbasset', 'totalpredictive', 'shareBRN', 'diffDES', 'totalARG', 'diffDOK', 'totallast10', 'totalSAG', 'totalBDF', 'diffMOR', 'totalDOK', 'diffSAG', 'diffBDF', 'diffBRN', 'totalBRN', 'totalPIG', 'diffHOW', 'totalMAS', 'diffARG', 'totalMOR']
x_feat = x_feat[:64]
x = data[x_feat]

N_FEATURES_OPTIONS = range(100,2000,100)
progress = 0

allaccuracy = []
allroc = []
alllogloss = []
allf1 = []
allnewlogloss = []
for k in N_FEATURES_OPTIONS:
    score = None
    acc = []
    logloss = []
    newlogloss = []
    roc = []
    newloss, loss, lb, transformed_labels, y_pred_weighted = None, None, None, None, None
    trainx, trainy, testx, testy, trainj, testj, model, pred = None, None, None, None, None, None, None, None
    for i in range(1,40):
        trainx, testx, trainy, testy, trainj, testj = train_test_split(x, y, juice, train_size = .9, test_size = .1, random_state = i, stratify = y)
        trainx = StandardScaler().fit_transform(trainx)
        testx = StandardScaler().fit_transform(testx)
        trainx = PCA(random_state = 1108, n_components=17 ,whiten=True,svd_solver='full').fit_transform(trainx)
        testx = PCA(random_state = 1108, n_components=17 ,whiten=True,svd_solver='full').fit_transform(testx)
        trainj = np.array(trainj)
        testj = np.array(testj)
        y_juice = []
        for every in range(0, len(np.array(testj))):
            ju = [testj[every]/200, -testj[every]/200]
            y_juice.append(ju)
        model = lgb.LGBMClassifier(min_child_samples=155,random_state = 86, num_leaves = 29, objective = 'binary_logloss', n_estimators = k, verbosity = 2, learning_rate = .0094266845511788537/5)
        model.fit(trainx, trainy)
        progress += 1
        print(('%.2f percent complete') %  (float((float(progress)/(float(len(N_FEATURES_OPTIONS))*float(40)))*100)))
        pred = model.predict(testx)
        probpred = model.predict_proba(testx)
        print(('accuracy: %f') % (accuracy_score(testy, pred)))
        print(('log loss: %f') % (log_loss(testy, probpred)))
        print(('roc auc score: %f') % (roc_auc_score(testy, pred)))
        acc.append(accuracy_score(testy, pred))
        logloss.append(log_loss(testy, probpred))
        roc.append(roc_auc_score(pred, testy))
        y_pred_weighted = probpred - y_juice
        newloss = log_loss(testy, y_pred_weighted)
        print(('new log loss: %f') % (newloss))
        newlogloss.append(newloss)
    allaccuracy.append(np.mean(acc))
    alllogloss.append(np.mean(logloss))
    allnewlogloss.append(np.mean(newlogloss))
    allroc.append(np.mean(roc))



#xaxis = []
#for each in N_FEATURES_OPTIONS:
#    for every in range(2, 25):
#        xaxis.append((each, every))  
#metascores = []
#allscores = pd.DataFrame()
#for each in range(0, len(xaxis)):
#    feats = xaxis[each][0]
#    pc = xaxis[each][1]
#    accu = allaccuracy[each]
#    rocc = allroc[each]
#    newloggloss = allnewlogloss[each]
#    loggloss = alllogloss[each]
#    meta = accu+rocc-newloggloss-loggloss
#    metascores.append(meta)
#    allscores=allscores.append({'features':feats, 'pca':pc, 'accuracy':accu, 'rocauc':rocc, 'logloss':loggloss, 'newlogloss':newloggloss}, ignore_index = True)
#stop = 0    
#for each in N_FEATURES_OPTIONS:
#    for every in range(2, 25):
#        if stop == metascores.index(max(metascores)):
#            print(each,every)
#        stop+=1

#lgb.LGBMClassifier(random_state = 86, objective = 'binary_logloss', n_estimators = 100, verbosity = 2, learning_rate = .0094266845511788537) acc: .50881801125703552, log: .69520374140190733



fig, ax1 = plt.subplots()
plt.figure(figsize=(10, 10))
X_axis = N_FEATURES_OPTIONS
#ax1.set_xscale('log')
ax1.axhline(y = .50986032937252446)
ax1.set_xlim(min(N_FEATURES_OPTIONS), max(N_FEATURES_OPTIONS))
ax1.set_ylim(min(allaccuracy)*.99, max(allaccuracy)*1.01)
ax1.plot(X_axis, allaccuracy, linestyle = ':', color='g')
besaccindex = allaccuracy.index(max(allaccuracy))
bestacc = allaccuracy[besaccindex]
ax1.plot([X_axis[besaccindex], ] * 2, [0, bestacc],
                linestyle='-.', color='g', marker='x', markeredgewidth=3, ms=8)
ax1.plot(X_axis, allroc, linestyle = ':', color='b')
bestrocindex = allroc.index(max(allroc))
bestroc = allroc[bestrocindex]
ax1.plot([X_axis[bestrocindex], ] * 2, [0, bestroc],
                linestyle='-.', color='b', marker='x', markeredgewidth=3, ms=8)

ax2 = ax1.twinx()
ax2.axhline(y = .69449880255559981)
#ax2.set_xscale('log')
ax2.set_ylim(min(allnewlogloss)*.99, max(allnewlogloss)*1.01)
ax2.plot(X_axis, allnewlogloss, linestyle = '-', color='r')
bestnewloglossindex = allnewlogloss.index(min(allnewlogloss))
bestnewlogloss = allnewlogloss[bestnewloglossindex]
ax2.plot([X_axis[bestnewloglossindex], ] * 2, [0, bestnewlogloss],
                linestyle='-.', color='r', marker='x', markeredgewidth=3, ms=8)
ax2.plot(X_axis, alllogloss, linestyle = ':', color='k')
besloglossindex = alllogloss.index(min(alllogloss))
bestlogloss = alllogloss[besloglossindex]
ax2.plot([X_axis[besloglossindex], ] * 2, [0, bestlogloss],
                linestyle='-.', color='k', marker='x', markeredgewidth=3, ms=8)

fig.tight_layout()
plt.show()


N_FEATURES_OPTIONS[allaccuracy.index(max(allaccuracy))]
allaccuracy[allaccuracy.index(max(allaccuracy))]
alllogloss[allaccuracy.index(max(allaccuracy))]
