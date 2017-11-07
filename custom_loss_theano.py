#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:39:01 2017

@author: eric.hensleyibm.com
"""

import numpy as np
#from sklearn.preprocessing import LabelBinarizer
#from sklearn.utils import check_consistent_length, check_array

def logloss_theano(y_true, y_pred, sample_weight = None, eps=1e-15, labels=None):
    
#    y_pred = check_array(y_pred, ensure_2d=False)
#    check_consistent_length(y_pred, y_true)
#
#    lb = LabelBinarizer()
#
#    if labels is not None:
#        lb.fit(labels)
#    else:
#        try:
#            lb.fit(y_true)
#        except ValueError:
#            lb.fit(y_true.astype(int))
#
#    if len(lb.classes_) == 1:
#        if labels is None:
#            raise ValueError('y_true contains only one label ({0}). Please '
#                             'provide the true labels explicitly through the '
#                             'labels argument.'.format(lb.classes_[0]))
#        else:
#            raise ValueError('The labels array needs to contain at least two '
#                             'labels for log_loss, '
#                             'got {0}.'.format(lb.classes_))
#
#    transformed_labels = lb.transform(y_true)
#
#    if transformed_labels.shape[1] == 1:
#        transformed_labels = np.append(1 - transformed_labels,
#                                       transformed_labels, axis=1)
    y_true = y_true.astype(int)
    # Clipping
    if sample_weight != None:
        y_pred_weighted = []
        for each in range(0, len(np.array(sample_weight))):
            y_pred_weighted.append([y_pred[each][0]+float(np.array(sample_weight)[each])/100, y_pred[each][1]-float(np.array(sample_weight)[each])/100])
        y_pred = np.clip(y_pred_weighted, eps, 1 - eps)
    elif sample_weight == None:
        y_pred = np.clip(y_pred, eps, 1-eps)
    # If y_pred is of single dimension, assume y_true to be binary
    # and then check.
    if y_pred.ndim == 1:
        y_pred = y_pred[:, np.newaxis]
    if y_pred.shape[1] == 1:
        y_pred = np.append(1 - y_pred, y_pred, axis=1)

    # Check if dimensions are consistent.
    transformed_labels = check_array(transformed_labels)
    if len(lb.classes_) != y_pred.shape[1]:
        if labels is None:
            raise ValueError("y_true and y_pred contain different number of "
                             "classes {0}, {1}. Please provide the true "
                             "labels explicitly through the labels argument. "
                             "Classes found in "
                             "y_true: {2}".format(transformed_labels.shape[1],
                                                  y_pred.shape[1],
                                                  lb.classes_))
        else:
            raise ValueError('The number of classes in labels is different '
                             'from that in y_pred. Classes found in '
                             'labels: {0}'.format(lb.classes_))

    # Renormalize
    y_pred /= y_pred.sum(axis=1)[:, np.newaxis]
    loss = -(transformed_labels * np.log(y_pred)).sum(axis=1)

    return loss