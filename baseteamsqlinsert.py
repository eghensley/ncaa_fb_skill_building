#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:31:22 2017

@author: eric.hensleyibm.com
"""

def baseteamsqlinsert(passcode):
    import datetime
    from datetime import date
    from baseteamdata import baseteamdata
    import numpy as np
    
    
    import mysql.connector   
    cnx = mysql.connector.connect(user='root', password=passcode,
                                  host='127.0.0.1',
                                  database='ncaa') 
    
    cursor = cnx.cursor() 
    
    day = '26'
    month = '08'
    year = '03'
    start_date = ('%s/%s/%s') % (month, day, year)
    
    offseason = [1,2,3,4,5,6,7]
    
    start_date = date(2003, 8, 26)
    dates = []
    
    while 1 != 2:
        new_date = start_date + datetime.timedelta(days=7)
        if new_date != date(2017,10,3):
            urldate = '%s-%s-%s' % (new_date.year, new_date.month, new_date.day)
            if new_date.month not in offseason:
                dates.append(urldate)
            start_date = new_date
        else:
            break
    
    z = 0
    for week in dates:
        cnx = mysql.connector.connect(user='root', password=passcode,
                                  host='127.0.0.1',
                                  database='ncaa') 
    
        cursor = cnx.cursor()
        x = baseteamdata(week)
        baseinsert = []
        baseinsertx = None
        initialbaseinsert = None
        add_base = None
        x = np.array(x)  
        
        for each in x:
            baseinsert.append("('"+each[0]+"', '"+str(week)+"', "+str(each[1])+", "+str(each[2])+", "+str(each[3])+", "+str(each[4])+", "+str(each[5])+", "+str(each[6])+", "+str(each[7])+", "+str(each[8])+", "+str(each[9])+", "+str(each[10])+", "+str(each[11])+", "+str(each[12])+", "+str(each[13])+", "+str(each[14])+", "+str(each[15])+", "+str(each[16])+", "+str(each[17])+", "+str(each[18])+", "+str(each[19])+", "+str(each[20])+", "+str(each[21])+", "+str(each[22])+", "+str(each[23])+", "+str(each[24])+")")
            baseinsertx = ','.join(baseinsert)
            baselist = ['INSERT INTO baseratings VALUES', baseinsertx, ';']
            initialbaseinsert = ' '.join(baselist)  
            add_base = initialbaseinsert  
        cursor.execute('SET foreign_key_checks = 0;')
        cursor.execute(add_base)
        cnx.commit()
        cursor.execute('SET foreign_key_checks = 1;')
        cursor.close()
        cnx.close()
        print ('base data %s percent complete') % (str(float(z)/float(len(dates))*100))
        z += 1