#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:35:33 2017

@author: eric.hensleyibm.com
"""

def datasetanalysis(x, y, scoring_metric):
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import KFold
    from sklearn.feature_selection import RFECV
    if y == 'share':
        score = x[3]/(x[3]+x[4])
        model = LinearRegression()
    elif y == 'diff':
        score = x[3]-x[4]
        model = LinearRegression()
    elif y == 'linediff':
        score = (x[3]-x[4])+x[5] 
        score = score.apply(lambda x: 1 if x>0 else x)
        score = score.apply(lambda x: -1 if x < 0 else x)
        model = LogisticRegression()
    skip = 0
    if y == 'linediff' and scoring_metric == 'neg_mean_squared_error':
        skip = 1
    if y == 'share' and scoring_metric == 'accuracy':
        skip = 1
    if y == 'diff' and scoring_metric == 'accuracy':
        skip = 1
    
    if skip == 0:
        allinputs = pd.DataFrame()
        variablename = 'homeaway'
        variablevalue = x[6]
        allinputs[variablename] = variablevalue
        for z in range(7,len(list(x)),2):
            variablename=None
            variablevalue=None
            variablename = 'sum%s' % (z)
            variablevalue = x[z]+x[z+1]
            allinputs[variablename] = variablevalue
            variablename=None
            variablevalue=None
            variablename = 'diff%s' % (z)
            variablevalue = x[z]-x[z+1]
            allinputs[variablename] = variablevalue
            variablename=None
            variablevalue=None
            variablename = 'share%s' % (z)
            variablevalue = x[z]/(x[z]+x[z+1])
            allinputs[variablename] = variablevalue
        
        for z in range(7,len(list(x)),2):
            variablename = 'share%s' % (z)
            allinputs[variablename]=allinputs[variablename].fillna(value=0)
            allinputs[variablename]=allinputs[variablename].apply(lambda x: 1 if str(x)=='inf' else x)
            allinputs[variablename]=allinputs[variablename].apply(lambda x: 0 if str(x)=='-inf' else x)
        
        xvar = list(allinputs)  
        fulldb = allinputs[xvar]
        fulldb['score'] = score
        fulldb = fulldb.dropna(how='any')
        
        allfeaturelist = []
        allscores = []
        for k in [3, 5, 7, 10]: 
            thesefeatures = []
            lm = model
            rfecv = RFECV(estimator=lm, step=1, cv=KFold(k),
                          scoring=scoring_metric)
            rfecv.fit(fulldb[xvar], fulldb['score'])
            allscores.append(max(rfecv.grid_scores_))
    #        print("Optimal number of features : %d" % rfecv.n_features_)
    #        print("Score : %f" % max(rfecv.grid_scores_))  
            for var in range(0, len(xvar)):
                if rfecv.support_[var] == True:
                    thesefeatures.append(var)
            allfeaturelist.append(thesefeatures)   
        inallfolds = []
        for feat in allfeaturelist[0]:
            if feat in allfeaturelist[1] and feat in allfeaturelist[2] and feat in allfeaturelist[3]:
                inallfolds.append(feat)
        cvscore = None
        cvscore = sum(allscores)/4
        inallfoldsnames = None
        inallfoldsnames = []
        for feat in inallfolds:
            inallfoldsnames.append(xvar[feat])
        numfeats = None
        numfeats = len(inallfolds)
        
        output = (cvscore, numfeats, inallfolds, inallfoldsnames)
        return output
            


