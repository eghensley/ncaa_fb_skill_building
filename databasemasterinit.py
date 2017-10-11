#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 18:25:58 2017

@author: eric.hensleyibm.com
"""

from resetsql import resetsql
from cfrcsql import cfrcsqlinsert
from bassetsql import bassetsqlinsert
from baseteamsqlinsert import baseteamsqlinsert
from odds2007sql import odds2007sql
from oddspost2007sql import oddspost2007sql
passcode = '*****'

print ('begin database initiation')
resetsql(passcode)
print ('...database initiated')
cfrcsqlinsert(passcode)
print('added cfrc rankings')
bassetsqlinsert(passcode)
print('added basset rankings')
odds2007sql(passcode)
print('added 2007 odds data')
for i in range(1,6):
    oddspost2007sql(passcode, i) 
    print('added %s percent of games since 2008') % (float(i)/6)
baseteamsqlinsert(passcode)
print('added base ncaa data')