#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:22:40 2017

@author: eric.hensleyibm.com
"""

#pipe = Pipeline([
#    ('preprocess', RobustScaler()),
#    ('reduce_dim', PCA(random_state = 1108, n_components=3,whiten=True,svd_solver='full')),
#    ('classify', KNeighborsClassifier(weights = 'distance', p=2, n_neighbors = 70))
#])


#pipe = Pipeline([
#    ('preprocess', MinMaxScaler()),
#    ('reduce_dim', PCA(iterated_power=7, n_components = 3, random_state = 86)),
#    ('classify',   SVC(kernel="linear", C=0.025),)
#])