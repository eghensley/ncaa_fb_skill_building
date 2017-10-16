#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 10:40:54 2017

@author: eric.hensleyibm.com
"""


def classificationdata():
    from pulldata import pulldata
    import pandas as pd
    from sklearn import preprocessing
    import numpy as np
    
    
    min_max_scaler = preprocessing.MinMaxScaler()
    x = pulldata()
    
    x = x.dropna(how='any')
    
    rawvars  = [0,0,0,0,0,0,0,'basset', 0, 'predictive', 0, 'home', 0, 'away', 0, 'home_adv', 0, 'sos', 0, 'fut_sos', 0, 'seas_sos', 0 ,'last5', 0, 'last10', 0, 'luck', 0, 'consistency', 0, 'vs_top10']
    allinputs = pd.DataFrame()
    variablename = 'homeaway'
    variablevalue = x[6]
    allinputs[variablename] = variablevalue
    for z in range(7,len(list(x)),2):
        variablename=None
        variablevalue=None
        variablename = 'diff%s' % (rawvars[z])
        variablevalue = min_max_scaler.fit_transform(x[z].values.reshape(-1,1))-min_max_scaler.fit_transform(x[z+1].values.reshape(-1,1))
        allinputs[variablename] = variablevalue
        variablename=None
        variablevalue=None
        variablename = 'share%s' % (rawvars[z])
        variablevalue = (min_max_scaler.fit_transform(x[z].values.reshape(-1,1)))/(min_max_scaler.fit_transform(x[z].values.reshape(-1,1))+min_max_scaler.fit_transform(x[z+1].values.reshape(-1,1)))
        allinputs[variablename] = variablevalue
    
    for z in range(7,len(list(x)),2):
        variablename = 'share%s' % (rawvars[z])
        allinputs[variablename]=allinputs[variablename].fillna(value=.5)
        allinputs[variablename]=allinputs[variablename].apply(lambda x: 1 if str(x)=='inf' else x)
        allinputs[variablename]=allinputs[variablename].apply(lambda x: 0 if str(x)=='-inf' else x)
    
    homeranks = min_max_scaler.fit_transform(np.array(x[[11,12]]))
    awayranks = min_max_scaler.fit_transform(np.array(x[[13,14]]))
    homefieldranks = min_max_scaler.fit_transform(np.array(x[[15,16]]))
    homeoraway = np.array(x[6])
    
    homeawayrankdiff = []
    homeawayrankshare = []
    homefieldeffect = []
    
    for loc in range(0, len(homeoraway)):
        if homeoraway[loc] == 0:
            diff = None
            share = None
            field = None
            diff = homeranks[loc][0] - awayranks[loc][1]
            homeawayrankdiff.append(diff)
            share = homeranks[loc][0]/(homeranks[loc][0]+awayranks[loc][1])
            homeawayrankshare.append(share)
            field = homefieldranks[loc][0]
            homefieldeffect.append(field)
        elif homeoraway[loc] == 1:
            diff = None
            share = None
            field = None
            diff = awayranks[loc][0] - homeranks[loc][1]
            homeawayrankdiff.append(diff)
            share = awayranks[loc][0]/(homeranks[loc][1]+awayranks[loc][0])
            homeawayrankshare.append(share)
            field = homefieldranks[loc][1]*(-1)
            homefieldeffect.append(field)        
    
    allinputs['homeawaydiff'] = np.array(homeawayrankdiff)
    allinputs['homeawayshare'] = np.array(homeawayrankshare)
    allinputs['fieldeffect'] = np.array(homefieldeffect)
    
    binary = []
    for game in range(0, len(x[3])):
        t=1
        if (np.array(x[3])[game] - np.array(x[4])[game]) > np.array(x[5])[game]*-1:
            binary.append(1)
        elif (np.array(x[3])[game] - np.array(x[4])[game]) < np.array(x[5])[game]*-1:
            binary.append(0)
        elif (np.array(x[3])[game] - np.array(x[4])[game]) == np.array(x[5])[game]*-1:
            binary.append(None)
    
    classset = pd.DataFrame()
    for each in allinputs:
        classset[each] = allinputs[each]
    classvars = list(classset)
    classset['y'] = np.array(binary)
    classset = classset.dropna(how='any') 
    return classset
