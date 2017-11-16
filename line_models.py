# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:00:07 2017

@author: Eric
"""
#pipe = Pipeline([
#    ('a_preprocess', MinMaxScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
#    ('c_classify', KNeighborsClassifier(weights='distance', p=1, n_neighbors = 95))
#])


#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 1)),
#    ('c_classify', SVC(kernel = 'linear', probability = True, random_state = 46, C = .04))
#])



#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
#    ('c_classify', SVC(kernel = 'rbf', probability = True, random_state = 46, C = 1, gamma =1))
#])


#pipe = Pipeline([
#    ('a_preprocess', StandardScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 2)),
#    ('c_classify', SVC(kernel = 'poly', random_state = 46, degree = 2, C =.4, gamma = .05, probability = True))
#])



#pipe = Pipeline([
#    ('a_preprocess', RobustScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 1)),
#    ('c_classify', GaussianProcessClassifier(1.0 * RBF(1.0)))
#])


#pipe = Pipeline([
#    ('a_preprocess', StandardScaler()),
#    ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 11)),
#    ('c_classify', lgb.LGBMClassifier(random_state = 46, learning_rate = .243, n_estimators = 100, num_leaves = 18, max_depth = 10))
#])

#