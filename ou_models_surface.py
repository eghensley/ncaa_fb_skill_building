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


#
#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 14)),
#    ('c_classify', QuadraticDiscriminantAnalysis())
#])
#


#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 28)),
#    ('c_classify', GaussianNB())
#])


#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 6)),
#    ('c_classify', RandomForestClassifier(random_state = 46, max_features = None, max_depth = 6, min_samples_split = 23, n_estimators = 40))
#])



#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 12)),
#    ('c_classify', MLPClassifier(random_state = 46, activation = 'tanh', solver = 'lbfgs', hidden_layer_sizes = (50, 200,)))
#])


#