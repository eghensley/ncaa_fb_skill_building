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
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection




def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def radar_factory(num_vars, frame='polygon'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    def draw_poly_patch(self):
        # rotate theta such that the first axis is at the top
        verts = unit_poly_verts(theta + np.pi / 2)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def __init__(self, *args, **kwargs):
            super(RadarAxes, self).__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta + np.pi / 2)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta



class tuned_line_models(object):
    def lin_svc(self):
        pipe = Pipeline([
            ('a_preprocess', RobustScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 1)),
            ('c_classify', SVC(kernel = 'linear', probability = True, random_state = 46, C = .04))
        ])
        return [pipe, 'SVC-lin']

    def rbf_svc(self):
        pipe = Pipeline([
            ('a_preprocess', RobustScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
            ('c_classify', SVC(kernel = 'rbf', probability = True, random_state = 46, C = 1, gamma =1))
        ])
        return [pipe, 'SVC-rbf']

    def poly_svc(self):
        pipe = Pipeline([
            ('a_preprocess', StandardScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 2)),
            ('c_classify', SVC(kernel = 'poly', random_state = 46, degree = 2, C =.4, gamma = .05, probability = True))
        ])
        return [pipe, 'SVC-poly']

    def GausProc(self):
        pipe = Pipeline([
            ('a_preprocess', RobustScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 1)),
            ('c_classify', GaussianProcessClassifier(1.0 * RBF(1.0)))
        ])
        return [pipe, 'Gauss']

    def light_gbc(self):
        pipe = Pipeline([
            ('a_preprocess', StandardScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 11)),
            ('c_classify', lgb.LGBMClassifier(random_state = 46, learning_rate = .243, n_estimators = 100, num_leaves = 18, max_depth = 10))
        ])
        return [pipe, 'LGBC']

    def knn(self):
        pipe = Pipeline([
            ('a_preprocess', MinMaxScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 3)),
            ('c_classify', KNeighborsClassifier(weights='distance', p=1, n_neighbors = 95))
        ])
        return [pipe, 'KNN']

    def QDA(self):
        pipe = Pipeline([
            ('a_preprocess', StandardScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 10)),
            ('c_classify', QuadraticDiscriminantAnalysis())
        ])
        return [pipe, 'QDA']

    def naive_bayes(self):
        pipe = Pipeline([
            ('a_preprocess', StandardScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 12)),
            ('c_classify', GaussianNB())
        ])
        return [pipe, 'naiive bayes']

    def RandomForrest(self):
        pipe = Pipeline([
            ('a_preprocess', StandardScaler()),
            ('b_reduce', PCA(iterated_power=7, random_state = 86, n_components = 9)),
            ('c_classify', RandomForestClassifier(random_state = 46, max_features = None, max_depth = 15, min_samples_split = 45))
        ])
        return [pipe, 'Random Forrest']
    
    def allmodels(self):
        models = [self.lin_svc(), self.rbf_svc(), self.poly_svc(), self.GausProc(), self.light_gbc(), self.knn(), self.QDA(), self.naive_bayes(), self.RandomForrest()]
        return models