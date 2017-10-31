#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:57:10 2017

@author: eric.hensleyibm.com
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.feature_selection import RFECV
from yellowbrick.features.rankd import Rank1D, Rank2D
from yellowbrick.features.radviz import RadViz
from yellowbrick.features.pcoords import ParallelCoordinates
from yellowbrick.features.jointplot import JointPlotVisualizer
from yellowbrick.features.pca import PCADecomposition
from yellowbrick.features.scatter import ScatterVisualizer
from numpy import ravel
data = pd.read_csv('ncaadata.csv')

features = list(data)
x_feat = features[:-1]
classes = ['over', 'under']

x = data[x_feat].as_matrix()
y = ravel(data['y'].as_matrix())

visualizer = Rank1D(features=features, algorithm='shapiro')
visualizer.fit(x, y)
visualizer.transform(x) 
visualizer.poof()



visualizer = Rank2D(features=features, algorithm='covariance')
visualizer.fit(x, y)
visualizer.transform(x) 
visualizer.poof()




visualizer = Rank2D(features=features, algorithm='pearson')
visualizer.fit(x, y)
visualizer.transform(x) 
visualizer.poof()




visualizer = ParallelCoordinates(
    classes=classes, features=features,
    normalize='standard', sample=0.1,
)
visualizer.fit(x, y)
visualizer.transform(x) 
visualizer.poof()




from sklearn.ensemble import ExtraTreesClassifier
model = ExtraTreesClassifier()
model.fit(x, y.astype(int))
forrestimportance = model.feature_importances_





from sklearn.feature_selection import RFE
model = LogisticRegression()
rfe = RFE(model, 3)
rfe = rfe.fit(x, y.astype(int))
logimportance = rfe.ranking_



variables = pd.DataFrame()
variables['vsrs'] = x_feat
variables['forrest'] = forrestimportance
variables['log'] = logimportance




scoring_metric = 'roc_auc'
allfeaturelist = []
allscores = []
for k in [7, 10, 15, 20]: 
    thesefeatures = []
    lm = model
    rfecv = RFECV(estimator=lm, step=1, cv=KFold(k),
                  scoring=scoring_metric)
    rfecv.fit(x, y.astype(int))
    allscores.append(max(rfecv.grid_scores_))
    
    print("Optimal number of features : %d" % rfecv.n_features_)
    print("Score : %f" % max(rfecv.grid_scores_))  
    
    for var in range(0, len(x_feat)):
        if rfecv.support_[var] == True:
            thesefeatures.append(var)
    allfeaturelist.append(thesefeatures)   

inallfolds = []
for feat in allfeaturelist[0]:
    if feat in allfeaturelist[1] and feat in allfeaturelist[2]:
        inallfolds.append(feat)
for every in inallfolds:
    print x_feat[every]
    
for x in allfeaturelist[3]:
    print x_feat[x]


