#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:57:20 2017

@author: eric.hensleyibm.com
"""


import requests
from lxml import html
import re
import pandas as pd
import numpy as np
import unicodedata
import mysql.connector   
import datetime




passcode = 'ibm1234'

cnx = mysql.connector.connect(user='root', password=passcode,
                          host='127.0.0.1',
                          database='ncaa')    
cursor = cnx.cursor()    

teamnames = ['Air Force', 'Akron', 'Alabama', 'App State', 'Arizona', 'Arizona St', 'Arkansas', 'Arkansas St', 'Army', 'Auburn', 'BYU', 'Ball State', 'Baylor', 'Boise State', 'Boston Col', 'Bowling Grn', 'Buffalo', 'California', 'Central FL', 'Central Mich', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado St', 'Connecticut', 'Duke', 'E Carolina', 'E Michigan', 'Fla Atlantic', 'Florida', 'Florida Intl', 'Florida St', 'Fresno St', 'GA Southern', 'GA Tech', 'Georgia', 'Georgia State', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas St', 'Kent State', 'Kentucky', 'LA Lafayette', 'LA Monroe', 'LA Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland', 'Memphis', 'Miami (FL)', 'Miami (OH)', 'Michigan', 'Michigan St', 'Middle Tenn', 'Minnesota', 'Miss State', 'Mississippi', 'Missouri', 'N Carolina', 'N Illinois', 'N Mex State', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma St', 'Old Dominion', 'Oregon', 'Oregon St', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'S Alabama', 'S Carolina', 'S Florida', 'S Methodist', 'S Mississippi', 'San Diego St', 'San Jose St', 'Stanford', 'Syracuse', 'TX Christian', 'TX El Paso', 'TX-San Ant', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'U Mass', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah State', 'VA Tech', 'Vanderbilt', 'Virginia', 'W Kentucky', 'W Michigan', 'W Virginia', 'Wake Forest', 'Wash State', 'Washington', 'Wisconsin', 'Wyoming', 'W Kentucky', 'Middle Tenn', 'San Jose St', 'LA Lafayette', 'LA Monroe']
teamlist = ['Air Force', 'Akron', 'Alabama', 'Appalachian St', 'Arizona', 'Arizona St', 'Arkansas', 'Arkansas St', 'Army','Auburn', 'BYU', 'Ball St', 'Baylor', 'Boise St', 'Boston College', 'Bowling Green', 'Buffalo', 'California', 'UCF','C Michigan', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado St', 'Connecticut', 'Duke','East Carolina','E Michigan',  'FL Atlantic', 'Florida', 'Florida Intl', 'Florida St', 'Fresno St', 'Ga Southern',  'Georgia Tech','Georgia', 'Georgia St', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa St', 'Kansas', 'Kansas St', 'Kent', 'Kentucky', 'ULL', 'ULM', 'Louisiana Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland','Memphis', 'Miami FL', 'Miami OH', 'Michigan', 'Michigan St', 'MTSU', 'Minnesota', 'Mississippi St', 'Mississippi', 'Missouri', 'North Carolina', 'N Illinois', 'New Mexico St', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio St', 'Oklahoma', 'Oklahoma St', 'Old Dominion', 'Oregon', 'Oregon St', 'Penn St', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'South Alabama', 'South Carolina', 'South Florida',  'SMU', 'Southern Miss', 'San Diego St', 'San Jose St', 'Stanford', 'Syracuse', 'TCU', 'UTEP', 'UT San Antonio', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas St', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'Massachusetts', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah St', 'Virginia Tech', 'Vanderbilt', 'Virginia',  'WKU', 'W Michigan', 'West Virginia', 'Wake Forest',  'Washington St', 'Washington',  'Wisconsin', 'Wyoming', 'W Kentucky', 'Middle Tenn St', 'San Jos\xe9 State', 'LA Lafayette', 'LA Monroe']

espnlist = ['Air Force', 'Akron', 'Alabama', 'Appalachian State', 'Arizona', 'Arizona State', 'Arkansas', 'Arkansas St', 'Army','Auburn', 'BYU', 'Ball State', 'Baylor', 'Boise State', 'Boston College', 'Bowling Green', 'Buffalo', 'California', 'UCF','Central Michigan', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado State', 'Connecticut', 'Duke','East Carolina','E Michigan',  'FL Atlantic', 'Florida', 'Florida Intl', 'Florida State', 'Fresno State', 'Ga Southern',  'Georgia Tech','Georgia', 'Georgia St', "Hawai'i", 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas State', 'Kent State', 'Kentucky', 'ULL', 'ULM', 'Louisiana Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland','Memphis', 'Miami', 'Miami OH', 'Michigan', 'Michigan State', 'MTSU', 'Minnesota', 'Mississippi State', 'Ole Miss', 'Missouri', 'North Carolina', 'Northern Illinois', 'New Mexico St', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma State', 'Old Dominion', 'Oregon', 'Oregon State', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'South Alabama', 'South Carolina', 'South Florida',  'SMU', 'Southern Mississippi', 'San Diego State', 'San Jose State', 'Stanford', 'Syracuse', 'TCU', 'UTEP', 'UT San Antonio', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'Massachusetts', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah State', 'Virginia Tech', 'Vanderbilt', 'Virginia',  'Western Kentucky', 'Western Michigan', 'West Virginia', 'Wake Forest',  'Washington State', 'Washington',  'Wisconsin', 'Wyoming']

teamsdict = {}
for i in range(0, len(teamnames)):
    teamsdict[teamlist[i]] = teamnames[i]
espndict = {}
for i in range(0, len(espnlist)):
    espndict[espnlist[i]] = teamnames[i]

year = '2017'
for qwerty in range(8, 12):
    
    url = None
    pageContent = None
    tree = None
    apteams = None
    uspoll = None
    playoffpoll = None
    bcspoll = None

    url = 'http://www.espn.com/college-football/rankings/_/week/%s/year/%s/seasontype/2'%(qwerty+1, year)
    pageContent=requests.get(url)
    tree = html.fromstring(pageContent.content)
    
    if tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[1]/h2[1]/text()')[0] == 'AP Top 25':
        apteams = tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[1]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')
    elif tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[1]/h2[1]/text()')[0] == 'Coaches Poll':
        uspoll = tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[2]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')
    elif tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[1]/h2[1]/text()')[0] == 'College Football Playoff Rankings':
        playoffpoll = tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[1]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')
    elif tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[1]/h2[1]/text()')[0] == 'BCS Standings':
        bcspoll = tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[1]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')

    if tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[2]/h2[1]/text()')[0] == 'AP Top 25':
        apteams = tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[2]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')
    elif tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[2]/h2[1]/text()')[0] == 'Coaches Poll':
        uspoll = tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[2]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')
    elif tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[2]/h2[1]/text()')[0] == 'BCS Standings':
        bcspoll = tree.xpath('//section[@class="col-b"]/div[3]/div[1]/div[2]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')
    
    if apteams == None:
        if tree.xpath('//section[@class="col-b"]/div[3]/div[2]/div[1]/h2[1]/text()')[0] == 'AP Top 25':
            apteams = tree.xpath('//section[@class="col-b"]/div[3]/div[2]/div[1]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()')
    if uspoll == None:
        if tree.xpath('//section[@class="col-b"]/div[3]/div[2]/div[1]/h2[1]/text()')[0] == 'Coaches Poll':
            uspoll = tree.xpath('//section[@class="col-b"]/div[3]/div[2]/div[1]/div[1]/table/tbody/tr/td[2]/a[2]/span/text()') 
    
    monthdict = {'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12', 'January':'01'}


    url = None
    pageContent = None
    tree = None
    rankingabbrev = None
    headers = None
    rankabbrev = None
    date = None
    month = None
    day = None
    yearx = None
    
    url = 'https://www.masseyratings.com/cf/arch/compare%s-%s.htm'%(year, qwerty)
    pageContent=requests.get(url)
    
    
    tree = html.fromstring(pageContent.content)
    rankingabbrev = tree.xpath('//html/body/pre/font/text()')[0].split(' ')
    headers = []
    rankabbrev = []
    

    if year == '2017':
        if qwerty != 0:
            month, day, yearx = tree.xpath('//html/body/table/tr/td/table/tr/td/h4/text()')[0].split(' ')[1:4]
            month = monthdict[month]
            day = day[:-1]
            if len(day) == 1:
                day = '0'+day
            date = yearx+'-'+month+'-'+day
        else:
            date = '2017-09-01'  
            
            
            
    d = None
    daysahead = None
    
    d = datetime.date(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
    daysahead = 5 - d.weekday()
    if daysahead == 0:
        daysahead = 7
    if daysahead == -1:
        daysahead = 6
    date = d + datetime.timedelta(daysahead)
    
    yearx = str(date.year)
    month = str(date.month)
    if len(month) == 1:
        month = '0'+month
    day = str(date.day)
    if len(day) == 1:
        day = '0'+day        
    date = yearx+'-'+month+'-'+day        
    
    
    for each in rankingabbrev:
        if each.split(',')[0] != '' and each.split(',')[0] != 'Team' and each.split(',')[0] != 'Conf' and each.split(',')[0] != 'Record':
                headers.append(each.split(',')[0])
                if each.split(',')[0] != 'Rank':
                    rankabbrev.append(each.split(',')[0])
    
    teamsandrankings = None
    rawteams = None
    masseyteams = None
    start = None
    endcontent = None
    startcontent = None
    rawratings = None
    ratings = None         
    teamsandrankings = tree.xpath('//html/body/pre/a/text()')[:len(rankabbrev)]
    rawteams = tree.xpath('//html/body/pre/a/text()')[len(rankabbrev):]
    
    masseyteams = []
    for each in rawteams:
        try:
            masseyteams.append(teamsdict[each])
        except KeyError:
#                print each
            pass
    
    start = [m.start() for m in re.finditer('Mean Median St.Dev', str(pageContent.content))]
    endcontent = [m.start() for m in re.finditer('----------', str(pageContent.content))]
    startcontent = str(pageContent.content)[start[0]:endcontent[0]]
    rawratings = startcontent.split(' ')
    ratings = []
    for every in rawratings:
        try:
            every.split('.')[1]
        except IndexError:
            try:
                ratings.append(int(every))
            except ValueError:
                try:
                    ratings.append(int(every.split('<')[0]))
                except ValueError:
                    try:
                        ratings.append(int(every.split('>')[1]))
                    except IndexError:
                        pass
                    except ValueError:
                        try:
                            ratings.append(int(every.split('>')[1].split('<')[0]))
                        except ValueError:
                            pass
    
    playofflist = None
    bcslist = None
    playoffcol = None
    bcscol = None
    playoffspotx = None
    bcsspotx = None
    bcsspot = None
    playoffspot = None
    aplist = None
    apcol = None
    uscol = None
    grid = None
    usspot = None
    apspot = None
    idices = None
    usspotx = None
    apspotx = None
    dataset = None
    
    aplist = []
    for team in apteams:
        try:
            aplist.append(espndict[team])
        except KeyError:
            aplist.append(espndict[unicodedata.normalize('NFKD', team).encode('ascii','ignore')])
    uslist = []
    for team in uspoll:
        try:
            uslist.append(espndict[team])
        except KeyError:
            uslist.append(espndict[unicodedata.normalize('NFKD', team).encode('ascii','ignore')])
    apcol = []
    for team in masseyteams:
        if team in aplist:
            apcol.append(aplist.index(team)+1)
        else:
            apcol.append(None)
    uscol = []
    for team in masseyteams:
        if team in uslist:
            uscol.append(uslist.index(team)+1)
        else:
            uscol.append(None)        
            
    grid = pd.DataFrame(columns = rankabbrev)
    grid['AP'] = np.array(apcol)
    grid['USA'] = np.array(uscol)  
    usspot = list(grid).index('USA')
    apspot = list(grid).index('AP')  
    indices = [i for i, x in enumerate(headers) if x == "Rank"]
    usspotx = headers.index('USA')
    apspotx = headers.index('AP')
      
    if playoffpoll != None or 'CFP' in headers:    
        playofflist = []
        for team in playoffpoll:
            playofflist.append(espndict[team])         
        playoffcol = []
        for team in masseyteams:
            if team in playofflist:
                playoffcol.append(playofflist.index(team)+1)
            else:
                playoffcol.append(None)   
        grid['CFP'] = np.array(playoffcol)   
        playoffspot = list(grid).index('CFP')   
        playoffspotx = headers.index('CFP')

    if bcspoll != None or 'BSC' in headers:    
        bcslist = []
        for team in bcspoll:
            try:
                bcslist.append(espndict[team])      
            except KeyError:
                bcslist.append(espndict[unicodedata.normalize('NFKD', team).encode('ascii','ignore')])
        bcscol = []
        for team in masseyteams:
            if team in bcslist:
                bcscol.append(bcslist.index(team)+1)
            else:
                bcscol.append(None)   
        if 'BCS' in headers:
            grid['BCS'] = np.array(bcscol)   
            bcsspot = list(grid).index('BCS') 
            bcsspotx = headers.index('BCS')       

ratings[:109]

    dataset = pd.DataFrame()
    stop = 0
    dbrow = 0
    dataspot = 0
    while stop != 1:
        line = []
        hcol = 0
        end = 0
        while end != 1: 
            if year == '2017' and qwerty >= 1 and qwerty < 7 and hcol in [headers.index('ENG')]  and dbrow == masseyteams.index('UAB'):
                line.append(None)
                hcol += 1 
            elif year == '2017' and qwerty == 7 and hcol in [headers.index('RME')]  and dbrow == masseyteams.index('Northwestern'):
                line.append(None)
                hcol += 1                     
       
                    
#            if year == '2017':
#                if qwerty== 8:
                    
            elif hcol == usspotx:
                    try:
                        if ratings[dataspot] == grid['USA'][dbrow]:
                            line.append(ratings[dataspot])
                            hcol += 1
                            dataspot += 1
                        elif grid['USA'][dbrow] == None:
                            line.append(None)
                            hcol += 1
                        else:
                            try:
                                if ratings[dataspot] == grid['USA'][dbrow]-1 or ratings[dataspot] == grid['USA'][dbrow]+1:
                                    line.append(ratings[dataspot])
                                    hcol += 1
                                    dataspot += 1
                            except TypeError:
                                if grid['USA'][dbrow] == None:
                                    line.append(None)
                                    hcol +=1
                                else:
                                    end = 1
                    except IndexError:
                        if len(grid) == len(dataset)+1:
                            if  len(line)+1 == len(list(grid)) or  len(line)+2 == len(list(grid)):
                               line.append(None)
                            elif len(line) + 3 == len(list(grid)):
                                line.append(None)
                                hcol += 1
                               
                               
                               
                               
            elif hcol == apspotx:
                try:
                    if ratings[dataspot] == grid['AP'][dbrow]:
                        line.append(ratings[dataspot])
                        hcol +=1
                        dataspot += 1
                    elif grid['AP'][dbrow] == None:
                        line.append(None)
                        hcol += 1
                    else:
                        try:
                            if ratings[dataspot] == grid['AP'][dbrow]-1 or ratings[dataspot] == grid['AP'][dbrow]+1:
                                line.append(ratings[dataspot])
                                hcol += 1
                                dataspot += 1
                        except TypeError:
                            if grid['AP'][dbrow] == None:
                                line.append(None)
                                hcol +=1
                            else:
                                end = 1
                except IndexError:
                    if len(grid) == len(dataset)+1:
                        if len(line)+1 == len(list(grid)) or len(line)+2 == len(list(grid)): 
                            line.append(None)
                        elif len(line) + 4 == len(list(grid)):
                            line.append(None)
                            hcol += 1
                        elif len(line) + 5 == len(list(grid)):
                            line.append(None)
                            hcol += 1
                        elif len(line) + 3 == len(list(grid)):
                            line.append(None)
                            hcol += 1                                
                            
                            
                            
            elif playoffspotx != None and hcol == playoffspotx:
                try:
                    if ratings[dataspot] == grid['CFP'][dbrow]:
                        line.append(ratings[dataspot])
                        hcol +=1
                        dataspot += 1
                    elif grid['CFP'][dbrow] == None:
                        line.append(None)
                        hcol += 1
                    else:
                        try:
                            if ratings[dataspot] == grid['CFP'][dbrow]-1 or ratings[dataspot] == grid['CFP'][dbrow]+1:
                                line.append(ratings[dataspot])
                                hcol += 1
                                dataspot += 1
                        except TypeError:
                            if grid['CFP'][dbrow] == None:
                                line.append(None)
                                hcol +=1
                            else:
                                end = 1
                except IndexError:
                    if len(grid) == len(dataset)+1:
                        if len(line)+1 == len(list(grid)) or len(line)+2 == len(list(grid)): 
                            line.append(None)     
                            
                            
                            
                            
            elif bcsspotx != None and hcol == bcsspotx:
                if year in ['2010', '2009', '2008'] and qwerty >= 7:
                    if qwerty >= 10:
                        if grid['BCS'][dbrow] != None:
                            line.append(None)
                            hcol += 1
                            dataspot += 1
                        elif grid['BCS'][dbrow] == None:
                            line.append(None)
                            hcol += 1
                    else:
                        line.append(None)
                        hcol += 1
                        dataspot += 1                            
                else:
                    try:
                        if ratings[dataspot] == grid['BCS'][dbrow]:
                            line.append(ratings[dataspot])
                            hcol +=1
                            dataspot += 1
                        elif grid['BCS'][dbrow] == None:
                            line.append(None)
                            hcol += 1
                        else:
                            try:
                                if ratings[dataspot] == grid['BCS'][dbrow]-1 or ratings[dataspot] == grid['BCS'][dbrow]+1:
                                    line.append(ratings[dataspot])
                                    hcol += 1
                                    dataspot += 1
                            except TypeError:
                                if grid['BCS'][dbrow] == None:
                                    line.append(None)
                                    hcol +=1
                                else:
                                    end = 1
                    except IndexError:
                        if len(grid) == len(dataset)+1:
                            if len(line)+1 == len(list(grid)) or len(line)+2 == len(list(grid)):
                                line.append(None)    
                            elif len(line) + 5  == len(list(grid)):
                                line.append(None)
                                hcol += 1
                            elif len(line) + 4 == len(list(grid)):
                                line.append(None)
                                hcol += 1

           
            else:
                line.append(ratings[dataspot])
                dataspot += 1
                hcol += 1                
            if len(line) == len(list(grid)):
                end = 1   
        rowentries = {}
        for v in range(0, len(list(grid))):
            rowentries[rankabbrev[v]] = line[v]
        dataset = dataset.append(rowentries, ignore_index = True)    
        dbrow += 1
        if len(grid) == len(dataset):
            stop = 1
        print(1)
    sqllabels = None            
    sqlstaging = None 
    sqldb = None
    masseylist = None
    masseyinsert = None
    masseyinsertx = None
    add_massey = None
    initialmasseyinsert = None
    print(2)   
#    if len(masseyteams) == len(dataset):        
#        sqllabels = ['Team', 'PIR', 'OSC', 'UCC', 'KPK', 'COF', 'LAZ', 'RWP', 'ACU', 'PAY', 'JTR', 'MTN', 'RT', 'DII', 'ASH', 'FMG', 'RUD', 'MGS', 'ARG', 'SOR', 'WLK', 'SEL', 'HEN', 'HAT', 'MAS', 'HKB', 'DOL', 'MvG', 'KEE', 'FAS', 'SAG', 'BIH', 'HOW', 'GRS', 'ENG', 'JRT', 'STH', 'PGH', 'RTH', 'HNL', 'KH', 'EZ', 'WOB', 'ABC', 'ISR', 'JNK', 'AND', 'COL', 'BOW', 'YCM', 'PCP', 'SOL', 'WOL', 'EFI', 'BSS', 'KRA', 'WIL', 'LOG', 'BWE', 'BBT', 'RTP', 'RFL', 'WWP', 'KLK', 'REW', 'DUN', 'KEL', 'DP', 'BIL', 'ONV', 'KNT', 'MCK', 'BMC', 'SP', 'LSW', 'GLD', 'WEL', 'BCM', 'MCL', 'LSD', 'MAR', 'DOI', 'DOK', 'TRP', 'VRN', 'INP', 'MJS', 'CSL', 'DEZ', 'RME', 'DWI', 'DES', 'KEN', 'MOR', 'DCI', 'CTW', 'FPI', 'PPP', 'MRK', 'TFG', 'MDS', 'BAS', 'GRR', 'BRN', 'GBE', 'RSL', 'PIG', 'SFX', 'FEI', 'CGV', 'KAM', 'CFP', 'S&P', 'RBA', 'NOL', 'PFZ', 'MGN', 'TPR', 'BDF', 'D1A', 'ATC', 'CMV', 'MVP', 'NUT', 'RTB']
#        sqlstaging = pd.DataFrame(columns = sqllabels)
#        sqlstaging['Team'] = masseyteams
#        
#        num = 0
#        for each in sqllabels:
#            if each in list(dataset):
#                sqlstaging[each] = dataset[each]
#                num += 1
#        sqlstaging.fillna('Null', inplace = True)                    
#        sqldb = np.array(sqlstaging) 
#
#    for team in sqldb:
#        masseyinsert = []
#        masseyinsert.append("('"+team[0]+"', '"+str(date)+"', "+str(team[1])+', '+str(team[2])+', '+str(team[3])+', '+str(team[4])+', '+str(team[5])+', '+str(team[6])+', '+str(team[7])+', '+str(team[8])+', '+str(team[9])+', '+str(team[10])+', '+str(team[11])+', '+str(team[12])+', '+str(team[13])+', '+str(team[14])+', '+str(team[15])+', '+str(team[16])+', '+str(team[17])+', '+str(team[18])+', '+str(team[19])+', '+str(team[20])+', '+str(team[21])+', '+str(team[22])+', '+str(team[23])+', '+str(team[24])+', '+str(team[25])+', '+str(team[26])+', '+str(team[27])+', '+str(team[28])+', '+str(team[29])+', '+str(team[30])+', '+str(team[31])+', '+str(team[32])+', '+str(team[33])+', '+str(team[34])+', '+str(team[35])+', '+str(team[36])+', '+str(team[37])+', '+str(team[38])+', '+str(team[39])+', '+str(team[40])+', '+str(team[41])+', '+str(team[42])+', '+str(team[43])+', '+str(team[44])+', '+str(team[45])+', '+str(team[46])+', '+str(team[47])+', '+str(team[48])+', '+str(team[49])+', '+str(team[50])+', '+str(team[51])+', '+str(team[52])+', '+str(team[53])+', '+str(team[54])+', '+str(team[55])+', '+str(team[56])+', '+str(team[57])+', '+str(team[58])+', '+str(team[59])+', '+str(team[60])+', '+str(team[61])+', '+str(team[62])+', '+str(team[63])+', '+str(team[64])+', '+str(team[65])+', '+str(team[66])+', '+str(team[67])+', '+str(team[68])+', '+str(team[69])+', '+str(team[70])+', '+str(team[71])+', '+str(team[72])+', '+str(team[73])+', '+str(team[74])+', '+str(team[75])+', '+str(team[76])+', '+str(team[77])+', '+str(team[78])+', '+str(team[79])+', '+str(team[80])+', '+str(team[81])+', '+str(team[82])+', '+str(team[83])+', '+str(team[84])+', '+str(team[85])+', '+str(team[86])+', '+str(team[87])+', '+str(team[88])+', '+str(team[89])+', '+str(team[90])+', '+str(team[91])+', '+str(team[92])+', '+str(team[93])+', '+str(team[94])+', '+str(team[95])+', '+str(team[96])+', '+str(team[97])+', '+str(team[98])+', '+str(team[99])+', '+str(team[100])+', '+str(team[101])+', '+str(team[102])+', '+str(team[103])+', '+str(team[104])+', '+str(team[105])+', '+str(team[106])+', '+str(team[107])+', '+str(team[108])+', '+str(team[109])+', '+str(team[110])+', '+str(team[111])+', '+str(team[112])+', '+str(team[113])+', '+str(team[114])+', '+str(team[115])+', '+str(team[116])+', '+str(team[117])+', '+str(team[118])+', '+str(team[119])+', '+str(team[120])+', '+str(team[121])+', '+str(team[122])+', '+str(team[123])+', '+str(team[124])+")")
#        masseyinsertx = ','.join(masseyinsert)
#        masseylist = ['INSERT INTO masseyratings VALUES', masseyinsertx, ';']
#        initialmasseyinsert = ' '.join(masseylist)  
#        add_massey = initialmasseyinsert  
#        cursor.execute('SET foreign_key_checks = 0;')
#        cursor.execute(add_massey)
#    cnx.commit()
#    cursor.execute('SET foreign_key_checks = 1;')
    print(3)

cursor.close()
cnx.close()     
