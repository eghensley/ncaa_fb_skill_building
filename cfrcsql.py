#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:17:48 2017

@author: eric.hensleyibm.com
"""

def cfrcsqlinsert(passcode):
    import requests
    from lxml import html
    import mysql.connector 
    import datetime

    cnx = mysql.connector.connect(user='root', password=passcode,
                                  host='127.0.0.1',
                                  database='ncaa')    
    cursor = cnx.cursor() 
    
    uppercaseteamnames = ['AIR FORCE', 'AKRON', 'ALABAMA', 'APP STATE', 'ARIZONA', 'ARIZONA ST', 'ARKANSAS', 'ARKANSAS ST', 'ARMY', 'AUBURN', 'BYU', 'BALL STATE', 'BAYLOR', 'BOISE STATE', 'BOSTON COL', 'BOWLING GRN', 'BUFFALO', 'CALIFORNIA', 'CENTRAL FL', 'CENTRAL MICH', 'CHARLOTTE', 'CINCINNATI', 'CLEMSON', 'COASTAL CAR', 'COLORADO', 'COLORADO ST', 'CONNECTICUT', 'DUKE', 'E CAROLINA', 'E MICHIGAN', 'FLA ATLANTIC', 'FLORIDA', 'FLORIDA INTL', 'FLORIDA ST', 'FRESNO ST', 'GA SOUTHERN', 'GA TECH', 'GEORGIA', 'GEORGIA STATE', 'HAWAII', 'HOUSTON', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'IOWA STATE', 'KANSAS', 'KANSAS ST', 'KENT STATE', 'KENTUCKY', 'LA LAFAYETTE', 'LA MONROE', 'LA TECH', 'LSU', 'LOUISVILLE', 'MARSHALL', 'MARYLAND',  'U MASS', 'MEMPHIS', 'MIAMI (FL)', 'MIAMI (OH)', 'MICHIGAN', 'MICHIGAN ST', 'MIDDLE TENN', 'MINNESOTA', 'MISS STATE', 'MISSISSIPPI', 'MISSOURI', 'N CAROLINA', 'N ILLINOIS', 'N MEX STATE', 'NC STATE', 'NAVY', 'NEBRASKA', 'NEVADA', 'NEW MEXICO', 'NORTH TEXAS', 'NORTHWESTERN', 'NOTRE DAME', 'OHIO', 'OHIO STATE', 'OKLAHOMA', 'OKLAHOMA ST', 'OLD DOMINION', 'OREGON', 'OREGON ST', 'PENN STATE', 'PITTSBURGH', 'PURDUE', 'RICE', 'RUTGERS', 'SAN DIEGO ST',  'S ALABAMA', 'S CAROLINA', 'S FLORIDA', 'S METHODIST', 'S MISSISSIPPI','SAN JOSE ST', 'STANFORD', 'SYRACUSE', 'TX CHRISTIAN', 'TX EL PASO', 'TX-SAN ANT', 'TEMPLE', 'TENNESSEE', 'TEXAS', 'TEXAS A&M', 'TEXAS STATE', 'TEXAS TECH', 'TOLEDO', 'TROY', 'TULANE', 'TULSA', 'UAB', 'UCLA', 'UNLV', 'USC', 'UTAH', 'UTAH STATE', 'VA TECH', 'VANDERBILT', 'VIRGINIA', 'W KENTUCKY', 'W MICHIGAN', 'W VIRGINIA', 'WAKE FOREST', 'WASH STATE', 'WASHINGTON', 'WISCONSIN', 'WYOMING'] 
    cfrcnames = ['Air Force', 'Akron', 'Alabama', 'Appalachian State', 'Arizona', 'Arizona State', 'Arkansas', 'Arkansas State', 'Army', 'Auburn',  'Brigham Young', 'Ball State', 'Baylor', 'Boise State', 'Boston College', 'Bowling Green','Buffalo', 'California', 'Central Florida', 'Central Michigan', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Carolina', 'Colorado', 'Colorado State', 'Connecticut', 'Duke', 'East Carolina', 'Eastern Michigan', 'Florida', 'Florida Atlantic', 'Florida Int.', 'Florida State', 'Fresno State','Georgia Southern', 'Georgia Tech', 'Georgia',  'Georgia State', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas State', 'Kent State', 'Kentucky', 'La. Lafayette', 'La. Monroe', 'Louisiana Tech',  'LSU', 'Louisville', 'Marshall', 'Maryland', 'Massachusetts', 'Memphis', 'Miami (Fla.)', 'Miami (Ohio)', 'Michigan', 'Michigan State', 'Middle Tennessee', 'Minnesota', 'Mississippi State', 'Mississippi',  'Missouri',  'North Carolina', 'Northern Illinois',  'New Mexico State', 'North Carolina St.', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas',  'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma State', 'Old Dominion', 'Oregon', 'Oregon State', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'San Diego State', 'South Alabama', 'South Carolina', 'South Florida','SMU','Southern Miss', 'San Jose State', 'Stanford', 'Syracuse', 'TCU',  'Texas-El Paso', 'Texas-San Antonio', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech','Toledo', 'Troy', 'Tulane', 'Tulsa', 'UAB', 'UCLA', 'Nevada-Las Vegas','Southern Cal',  'Utah', 'Utah State',  'Virginia Tech',  'Vanderbilt', 'Virginia',  'Western Kentucky', 'Western Michigan',  'West Virginia', 'Wake Forest', 'Washington State', 'Washington', 'Wisconsin', 'Wyoming']
    urllist = ['pre-season-2014', '', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    
    cfrcteamsdict = {}
    for i in range(0, len(uppercaseteamnames)):
        cfrcteamsdict[cfrcnames[i]] = uppercaseteamnames[i]
    
    for j in urllist:
        usedate = None
        days_ahead = None
        url = None
        pageContent = None
        tree = None
        thisdate = None
        day = None
        month = None
        year = None
        d = None
        gamedate = None
        useday = None
        usemonth = None
        useyear = None
        
        cfrcinsertx = None
        cfrcinsert = []
        url = 'http://cfrc.com/ranking/billingsley-mov-%s/' % (j)
        pageContent=requests.get(url)
        tree = html.fromstring(pageContent.content)
        
        thisdate = str(tree.xpath('//body/div/div/div/div/article/header/p/text()')[0]).strip().split('on ')[1]
        day = thisdate.split(' ')[2][:-1]
        month = thisdate.split(' ')[1]
        year = thisdate.split(' ')[3]

        d = datetime.date(int(year), int(monthdict[month]), int(day))
        weekday = 5
        days_ahead = weekday - d.weekday()
        if days_ahead < 0:
            days_ahead = 7 + days_ahead
        gamedate = d + datetime.timedelta(days_ahead)
        if len(str(gamedate.day)) == 2:
            useday = str(gamedate.day)
        elif len(str(gamedate.day)) == 1:
            useday = '0'+str(gamedate.day)
        if len(str(gamedate.month)) == 2:
            usemonth = str(gamedate.month)
        elif len(str(gamedate.month)) == 1:
            usemonth = '0'+str(gamedate.month)
        useyear = str(gamedate.year)
        
        usedate = useyear+'-'+usemonth+'-'+useday
        if usedate == '2014-07-26':
            usedate = '2014-08-30'
        cfrcstats = []
        for i in range(2,132):
            try:
                namepath = '//*[@id="main"]/article/section/table/tr[%s]/td[4]/text()' % (i)
                name = (tree.xpath(namepath)[0])
                rankpath = '//*[@id="main"]/article/section/table/tr[%s]/td[7]/text()' % (i)
                rank = (tree.xpath(rankpath)[0])
                stattuple =(name, rank)
                cfrcstats.append(stattuple)
            except IndexError:
                pass
        if len(cfrcstats) > 0:
            for team in cfrcstats:
                    cfrcinsert.append("('"+cfrcteamsdict[team[0]]+"', '"+str(usedate)+"', "+str(team[1])+")")
            cfrcinsertx = ','.join(cfrcinsert)
            cfrclist = ['INSERT INTO cfrcratings VALUES', cfrcinsertx, ';']
            initialcfrcinsert = ' '.join(cfrclist)  
            add_cfrc = initialcfrcinsert  
            print usedate
            cursor.execute('SET foreign_key_checks = 0;')
            cursor.execute(add_cfrc)
            cnx.commit()
            cursor.execute('SET foreign_key_checks = 1;')
    cursor.close()
    cnx.close()        
