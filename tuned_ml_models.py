#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:32:19 2017

@author: eric.hensleyibm.com
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import lightgbm as lgb
from sklearn.neural_network import MLPClassifier


def lin_svc():
    pipe = Pipeline([
        ('a_preprocess', MinMaxScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
        ('c_classify', SVC(random_state = 46, kernel = 'linear', probability = True, C = .1))
    ])
    return ('SVC-lin', pipe)

def rbf_svc():
    pipe = Pipeline([
        ('a_preprocess', RobustScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
        ('c_classify', SVC(random_state = 46, kernel = 'rbf', probability = True, C = .1, gamma = 10))
    ])
    return ('SVC-rbf', pipe)

def poly_svc():
    pipe = Pipeline([
        ('a_preprocess', RobustScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
        ('c_classify', SVC(random_state = 46, kernel = 'poly', probability = True, C = .1, degree = 2, gamma = .1))
    ])
    return ('SVC-poly', pipe)

def GausProc():
    pipe = Pipeline([
        ('a_preprocess', MinMaxScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
        ('c_classify', GaussianNB())
    ])
    return ('Gauss', pipe)

def light_gbc():
    pipe = Pipeline([
        ('a_preprocess', StandardScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 32)),
        ('c_classify', lgb.LGBMClassifier(random_state = 46, learning_rate = .43939, n_estimators = 100, num_leaves= 750, max_depth = 20))
    ])
    return ('LGBC', pipe)

def knn():
    pipe = Pipeline([
        ('a_preprocess', MinMaxScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 5)),
        ('c_classify', KNeighborsClassifier(weights = 'uniform', p = 1, n_neighbors = 3))
    ])
    return ('KNN', pipe)

def QDA():
    pipe = Pipeline([
        ('a_preprocess', MinMaxScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 22)),
        ('c_classify', QuadraticDiscriminantAnalysis())
    ])
    return ('QDA', pipe)

def naive_bayes():
    pipe = Pipeline([
        ('a_preprocess', MinMaxScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
        ('c_classify', GaussianNB())
    ])
    return ('naiive bayes', pipe)

def RandomForrest():
    pipe = Pipeline([
        ('a_preprocess', RobustScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 20)),
        ('c_classify', RandomForestClassifier(random_state = 46, max_features = None, max_depth = 20, min_samples_split = 2))
    ])
    return ('Random Forrest', pipe)

def NeuralNet():
    pipe = Pipeline([
        ('a_preprocess', StandardScaler()),
        ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 44)),
        ('c_classify', MLPClassifier(random_state = 46, solver = 'adam', activation = 'tanh', hidden_layer_sizes = (125,175,)))
    ])
    return ('Neural Net', pipe)

def allmodels():
    models = [lin_svc(), rbf_svc(), poly_svc(), GausProc(), light_gbc(), knn(), QDA(), naive_bayes(), RandomForrest(), NeuralNet()]
    return models