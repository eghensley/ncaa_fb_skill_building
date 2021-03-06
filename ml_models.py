#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:27:37 2017

@author: eric.hensleyibm.com
"""

#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 4)),
#    ('c_classify', KNeighborsClassifier(weights = 'distance', p = 1, n_neighbors = 100))
#])

#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
#    ('c_classify', SVC(random_state = 46, kernel = 'linear', probability = True, C = .1))
#])

#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
#    ('c_classify', SVC(random_state = 46, kernel = 'rbf', probability = True, C = .1, gamma = 10))
#])


#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
#    ('c_classify', SVC(random_state = 46, kernel = 'poly', probability = True, C = .1, degree = 2, gamma = .1))
#])


#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)), # can drop to 2 if too intensive
#    ('c_classify', GaussianProcessClassifier(1.0 * RBF(1.0)))
#])


#pipe = Pipeline([
#    ('a_preprocess', StandardScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 32)),
#    ('c_classify', lgb.LGBMClassifier(random_state = 46, learning_rate = .43939, n_estimators = 100, num_leaves= 750, max_depth = 20))
#])

#