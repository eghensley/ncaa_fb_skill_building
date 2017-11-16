#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:22:40 2017

@author: eric.hensleyibm.com
"""
#
#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
#    ('c_classify', KNeighborsClassifier(weights = 'distance', p = 1, n_neighbors = 15))
#])


#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
#    ('c_classify', SVC(kernel = 'linear', random_state = 1108, probability = True, C = .1))
#])

#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 1)),
#    ('c_classify', SVC(kernel = 'rbf', random_state = 1108, probability = True, C = 100, gamma = .1))
#])


#pipe = Pipeline([
#    ('a_preprocess', StandardScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 2)),
#    ('c_classify', SVC(kernel = 'poly', random_state = 1108, probability = True, C = 1, degree = 2, gamma = 3))
#])


#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 2)),
#    ('c_classify',  GaussianProcessClassifier(1.0 * RBF(1.0)))
#])


#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 2)),
#    ('c_classify', lgb.LGBMClassifier(max_depth = 4, num_leaves = 80, random_state = 46, n_estimators = 45, learning_rate = .0372))
#])

#