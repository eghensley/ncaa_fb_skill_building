#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 12:31:14 2017

@author: eric.hensleyibm.com
"""


def odds2007sql(passcode):
    import requests
    from lxml import html
    import datetime
    from datetime import date
    import unicodedata
    import mysql.connector   
    cnx = mysql.connector.connect(user='root', password=passcode,
                                  host='127.0.0.1',
                                  database='ncaa')    
    cursor = cnx.cursor() 
    offseason = [1,2,3,4,5,6,7]
    
    start_date = date(2007, 8, 31)
    dates = []
    
    while 1 != 2:
        new_date = start_date + datetime.timedelta(days=1)
        if new_date != date(2008,1,1):
            urldate = '%s-%s-%s' % (new_date.year, new_date.month, new_date.day)
            if new_date.month not in offseason:
                dates.append(urldate)
            start_date = new_date
        else:
            break
        
        
    uppercaseteamnames = ['KENT STATE','S MISSISSIPPI','CINCINNATI', 'WASHINGTON', 'MIDDLE TENN','FLORIDA INTL', 'ARIZONA', 'AIR FORCE', 'AKRON', 'ALABAMA', 'APP STATE', 'ARIZONA', 'ARIZONA ST', 'ARKANSAS', 'ARKANSAS ST', 'ARMY', 'AUBURN', 'BYU', 'BALL STATE', 'BAYLOR', 'BOISE STATE', 'BOSTON COL', 'BOWLING GRN', 'BUFFALO', 'CALIFORNIA', 'CENTRAL FL', 'CENTRAL MICH', 'CHARLOTTE', 'CINCINNATI', 'CLEMSON', 'COASTAL CAR', 'COLORADO', 'COLORADO ST', 'CONNECTICUT', 'DUKE', 'E CAROLINA', 'E MICHIGAN', 'FLA ATLANTIC', 'FLORIDA', 'FLORIDA INTL', 'FLORIDA ST', 'FRESNO ST', 'GA SOUTHERN', 'GA TECH', 'GEORGIA', 'GEORGIA STATE', 'HAWAII', 'HOUSTON', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'IOWA STATE', 'KANSAS', 'KANSAS ST', 'KENT STATE', 'KENTUCKY', 'LA LAFAYETTE', 'LA MONROE', 'LA TECH', 'LSU', 'LOUISVILLE', 'MARSHALL', 'MARYLAND',  'U MASS', 'MEMPHIS', 'MIAMI (FL)', 'MIAMI (OH)', 'MICHIGAN', 'MICHIGAN ST', 'MIDDLE TENN', 'MINNESOTA', 'MISS STATE', 'MISSISSIPPI', 'MISSOURI', 'N CAROLINA', 'N ILLINOIS', 'N MEX STATE', 'NC STATE', 'NAVY', 'NEBRASKA', 'NEVADA', 'NEW MEXICO', 'NORTH TEXAS', 'NORTHWESTERN', 'NOTRE DAME', 'OHIO', 'OHIO STATE', 'OKLAHOMA', 'OKLAHOMA ST', 'OLD DOMINION', 'OREGON', 'OREGON ST', 'PENN STATE', 'PITTSBURGH', 'PURDUE', 'RICE', 'RUTGERS', 'SAN DIEGO ST',  'S ALABAMA', 'S CAROLINA', 'S FLORIDA', 'S METHODIST', 'S MISSISSIPPI','SAN JOSE ST', 'STANFORD', 'SYRACUSE', 'TX CHRISTIAN', 'TX EL PASO', 'TX-SAN ANT', 'TEMPLE', 'TENNESSEE', 'TEXAS', 'TEXAS A&M', 'TEXAS STATE', 'TEXAS TECH', 'TOLEDO', 'TROY', 'TULANE', 'TULSA', 'UAB', 'UCLA', 'UNLV', 'USC', 'UTAH', 'UTAH STATE', 'VA TECH', 'VANDERBILT', 'VIRGINIA', 'W KENTUCKY', 'W MICHIGAN', 'W VIRGINIA', 'WAKE FOREST', 'WASH STATE', 'WASHINGTON', 'WISCONSIN', 'WYOMING']
    uppercaseoddsteams = ['KENT', 'SO MISSISSIPPI', 'CINCINNATI U', 'WASHINGTON U', 'MIDDLE TENN ST', 'FLORIDA INTL', 'ARIZONA U', 'AIR FORCE', 'AKRON', 'ALABAMA', 'APPALACHIAN ST', 'ARIZONA', 'ARIZONA STATE', 'ARKANSAS', 'ARKANSAS STATE', 'ARMY', 'AUBURN', 'BYU', 'BALL STATE', 'BAYLOR', 'BOISE STATE', 'BOSTON COLLEGE', 'BOWLING GREEN', 'BUFFALO U', 'CALIFORNIA', 'CENTRAL FLORIDA', 'CENTRAL MICHIGAN', 'CHARLOTTE', 'CINCINNATI', 'CLEMSON', 'COASTAL CAROLINA', 'COLORADO', 'COLORADO STATE', 'CONNECTICUT', 'DUKE', 'EAST CAROLINA', 'EASTERN MICHIGAN', 'FLORIDA ATLANTIC','FLORIDA', 'FLORIDA INTERNATIONAL', 'FLORIDA STATE', 'FRESNO STATE', 'GEORGIA SOUTHERN', 'GEORGIA TECH',  'GEORGIA', 'GEORGIA STATE', 'HAWAII', 'HOUSTON U', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'IOWA STATE', 'KANSAS', 'KANSAS STATE', 'KENT STATE', 'KENTUCKY', 'UL - LAFAYETTE', 'UL - MONROE', 'LOUISIANA TECH', 'LSU', 'LOUISVILLE', 'MARSHALL', 'MARYLAND', 'MASSACHUSETTS', 'MEMPHIS', 'MIAMI FLORIDA', 'MIAMI OHIO', 'MICHIGAN', 'MICHIGAN STATE', 'MID TENNESSEE STATE', 'MINNESOTA', 'MISSISSIPPI STATE', 'MISSISSIPPI', 'MISSOURI', 'NORTH CAROLINA', 'NORTHERN ILLINOIS',   'NEW MEXICO STATE', 'NORTH CAROLINA STATE',  'NAVY', 'NEBRASKA', 'NEVADA', 'NEW MEXICO', 'NORTH TEXAS', 'NORTHWESTERN', 'NOTRE DAME', 'OHIO', 'OHIO STATE', 'OKLAHOMA', 'OKLAHOMA STATE', 'OLD DOMINION', 'OREGON', 'OREGON STATE', 'PENN STATE', 'PITTSBURGH', 'PURDUE', 'RICE', 'RUTGERS', 'SAN DIEGO STATE', 'SOUTH ALABAMA',  'SOUTH CAROLINA', 'SOUTH FLORIDA',  'SMU', 'SOUTHERN MISS', 'SAN JOSE STATE', 'STANFORD', 'SYRACUSE', 'TCU',  'UTEP',  'TEX SAN ANTONIO',  'TEMPLE', 'TENNESSEE U', 'TEXAS', 'TEXAS AM', 'TEXAS STATE', 'TEXAS TECH', 'TOLEDO', 'TROY', 'TULANE', 'TULSA', 'UAB', 'UCLA', 'UNLV', 'USC', 'UTAH', 'UTAH STATE','VIRGINIA TECH', 'VANDERBILT', 'VIRGINIA', 'WESTERN KENTUCKY', 'WESTERN MICHIGAN',  'WEST VIRGINIA', 'WAKE FOREST',  'WASHINGTON STATE', 'WASHINGTON','WISCONSIN','WYOMING']
    
    oddsteamsdict = {}
    for i in range(0, len(uppercaseteamnames)):
        oddsteamsdict[uppercaseoddsteams[i]] = uppercaseteamnames[i]
    
    
    nonfbs = []
    for gameday in dates:
        url = None
        pageContent = None
        tree = None
        day = None
        month = None
        year = None
        if len(gameday.split('-')[2]) == 1:
            day = '0'+gameday.split('-')[2]
        elif len(gameday.split('-')[2]) == 2:
            day = gameday.split('-')[2]
        if len(gameday.split('-')[1]) == 1:
            month = '0'+gameday.split('-')[1]
        elif len(gameday.split('-')[1]) == 2:
            month = gameday.split('-')[1]
        year = gameday.split('-')[0]
        
        url = 'http://www.scoresandodds.com/grid_%s%s%s.html' % (year, month, day)
        pageContent=requests.get(url)
        tree = html.fromstring(pageContent.content)
        
        for sport in range(3, 10):
            root = '/html/body/div/div/div[2]/div/div[%s]/table' % (sport)
            end = 0
            gamex = 0
            sportpath = root+'/thead/tr[1]/td[1]/span[1]/text()'
            if len(tree.xpath(sportpath)) > 0 and tree.xpath(sportpath)[0] == 'NCAA FB':
                while end == 0:
                    gamex += 1
                    gamepath ='/tbody[%s]' % (gamex)
                    team1path = '/tr[2]'
                    team2path = '/tr[3]'
                    teamnamepath = '/td[1]/span[2]/text()'
                    overunderpath = '/td[4]/text()'
                    linepath = '/td[4]/b/text()'
                    linejuicepath = '/td[4]/text()'
                    moneylinepath = '/td[5]/text()'
                    scorepath = '/td[6]/text()'
                    favorite = None
                    moneyline1path = None
                    moneyline2path = None
                    namepath1 = None
                    name1 = None
                    namepath2 = None
                    moneyline1 = None
                    moneyline2 = None
                    team1fav = None
                    team2fav = None
                    line = None
                    juicepath = None
                    juice = None
                    oupath = None
                    overunder = None
                    game = []
                    fbsgame = 'yes'
                    overunderjuice = None
                    
                    namepath1 = root+gamepath+team1path+teamnamepath
                    namepath2 = root+gamepath+team2path+teamnamepath
            
                    if len(tree.xpath(namepath1)) == 0 and len(tree.xpath(namepath2)) == 0:
                        end = 1
                    if end == 0:
                        try:
                            try:
                                name1 = oddsteamsdict[str(unicodedata.normalize('NFKD', tree.xpath(namepath1)[0]).encode('ascii', 'ignore')).upper()]
                            except TypeError:
                                name1 = oddsteamsdict[str(tree.xpath(namepath1)[0]).upper()]
                            namepath2 = root+gamepath+team2path+teamnamepath
                            try:
                                name2 = oddsteamsdict[str(unicodedata.normalize('NFKD', tree.xpath(namepath2)[0]).encode('ascii', 'ignore')).upper()]
                            except TypeError:
                                name2 = oddsteamsdict[str(tree.xpath(namepath2)[0]).upper()]
                        except KeyError:
                            fbsgame = 'no'
                        if fbsgame == 'yes':
                            moneyline1path = root+gamepath+team1path+moneylinepath
                            moneyline2path = root+gamepath+team2path+moneylinepath
                            try:
                                moneyline1 = float(unicodedata.normalize('NFKD', tree.xpath(moneyline1path)[0]).encode('ascii', 'ignore'))
                            except ValueError:
                                if unicodedata.normalize('NFKD', tree.xpath(moneyline1path)[0]).encode('ascii', 'ignore') == '\n \n':
                                    moneyline1 = "Null"
                                elif unicodedata.normalize('NFKD', tree.xpath(moneyline1path)[0]).encode('ascii', 'ignore') == '\nEVEN \n':
                                    moneyline1 = 100
                            try:
                                moneyline2 = float(unicodedata.normalize('NFKD', tree.xpath(moneyline2path)[0]).encode('ascii', 'ignore'))
                            except ValueError:
                                if unicodedata.normalize('NFKD', tree.xpath(moneyline2path)[0]).encode('ascii', 'ignore') == '\n \n':
                                    moneyline2 = "Null"
                                elif unicodedata.normalize('NFKD', tree.xpath(moneyline2path)[0]).encode('ascii', 'ignore') == '\nEVEN \n':
                                    moneyline2 = 100
                                    
                            score1path = root+gamepath+team1path+scorepath
                            score2path = root+gamepath+team2path+scorepath
                            try:
                                score1 = int(str(unicodedata.normalize('NFKD',  tree.xpath(score1path)[0]).encode('ascii', 'ignore')).split(' ')[0])
                                score2 = int(str(unicodedata.normalize('NFKD',  tree.xpath(score2path)[0]).encode('ascii', 'ignore')).split(' ')[0])
                            except ValueError:
                                if str(unicodedata.normalize('NFKD',  tree.xpath(score1path)[0]).encode('ascii', 'ignore')) == '\n cancelled \n' or str(unicodedata.normalize('NFKD',  tree.xpath(score2path)[0]).encode('ascii', 'ignore')) == '\n cancelled \n':
                                    score1, score2 = "Null", "Null"
                            team1fav = root+gamepath+team1path+linepath
                            team2fav = root+gamepath+team2path+linepath   
                            if len(tree.xpath(team1fav)) == 0 and len(tree.xpath(team2fav)) == 1:
                                favorite = 2
                            elif len(tree.xpath(team1fav)) == 1 and len(tree.xpath(team2fav)) == 0:
                                favorite = 1
                            
                            if favorite == 1:
                                try:
                                    line = float(tree.xpath(team1fav)[0])
                                except ValueError:
                                    if tree.xpath(team1fav)[0] == 'PK':
                                        line = 0
                                juicepath = root+gamepath+team1path+linejuicepath
                                try:
                                    juice = float(unicodedata.normalize('NFKD', tree.xpath(juicepath)[1]).encode('ascii', 'ignore'))
                                except ValueError:
                                    juice = 0
                                oupath = root+gamepath+team2path+overunderpath
                                try:
                                    overunder = float(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore'))
                                    overunderjuice = 0
                                except ValueError:
                                    if len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')) == 2 and len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')) == 1:
                                        overunder = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')[0])
                                        overunderjuice = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')[1])
                                    elif len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')) == 1 and len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')) == 2:
                                        overunder = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')[0])
                                        overunderjuice = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')[1])*(-1)                                     
                                    elif len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')) == 1 and len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')) == 1 and unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore') == '\n \n' :
                                        overunder = 'Null'
                                        overunderjuice = 'Null'
                                game = [gameday, name1, name2, line, juice, overunder, overunderjuice, moneyline1, moneyline2, score1, score2]
                            elif favorite == 2:
                                try:
                                    line = float(tree.xpath(team2fav)[0])
                                except ValueError:
                                    if tree.xpath(team2fav)[0] == 'PK':
                                        line = 0
                                juicepath = root+gamepath+team2path+linejuicepath
                                try:
                                    juice = float(unicodedata.normalize('NFKD', tree.xpath(juicepath)[1]).encode('ascii', 'ignore'))
                                except ValueError:
                                    juice = 0
                                oupath = root+gamepath+team1path+overunderpath
                                try:
                                    overunder = float(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore'))
                                    overunderjuice = 0
                                except ValueError:
                                    if len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')) == 2 and len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')) == 1:
                                        overunder = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')[0])
                                        overunderjuice = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')[1])
                                    elif len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')) == 1 and len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')) == 2:
                                        overunder = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')[0])
                                        overunderjuice = float(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')[1])*(-1)                                     
                                    elif len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('o')) == 1 and len(str(unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore')).split('u')) == 1 and unicodedata.normalize('NFKD', tree.xpath(oupath)[0]).encode('ascii', 'ignore') == '\n \n':
                                        overunder = 'Null'
                                        overunderjuice = 'Null'
                                game = [gameday, name2, name1, line, juice, overunder, overunderjuice, moneyline2, moneyline1, score2, score1]
                            print game
                            oddsinsert = []
                            oddsinsertx = None
                            oddslist = []
                            initialoddsinsert = None
                            add_odds = None
                            oddsinsert.append("('"+game[0]+"', '"+str(game[1])+"', '"+str(game[2])+"', "+str(game[3])+", "+str(game[4])+", "+str(game[5])+", "+str(game[6])+", "+str(game[7])+", "+str(game[8])+", "+str(game[9])+", "+str(game[10])+")")
                            oddsinsertx = ','.join(oddsinsert)
                            oddslist = ['INSERT INTO oddsdata VALUES', oddsinsertx, ';']
                            initialoddsinsert = ' '.join(oddslist)  
                            add_odds = initialoddsinsert  
                            cursor.execute('SET foreign_key_checks = 0;')
                            cursor.execute(add_odds)
                            cnx.commit()
                            cursor.execute('SET foreign_key_checks = 1;')
                        else:
                            error = (tree.xpath(namepath1)[0], tree.xpath(namepath2)[0], url)
                            nonfbs.append(error)
                    else:
                        pass
                else:
                    pass
    cursor.close()
    cnx.close()