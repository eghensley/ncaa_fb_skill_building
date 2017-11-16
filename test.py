#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 02:43:28 2017

@author: eric.hensleyibm.com
"""

from bringit import integrator
import json

test = integrator()
test.integrated_pipeline('IBM')

company = 'IBM'
rawdata = test.get_raw_data(text = 'charity or service', organization = company, language = 'english', accuracy_confidence = 'high')
test.post_data(rawdata, db_name = 'rawdata', company_name = company)
allstoreddata = test.pull_data(db_name = 'raw data', field = 'company', key = company)
for each in allstoreddata:
    watson_output = test.analyze_data(each)
    print(json.dumps(watson_output, indent=2))
    test.post_data(watson_output) 