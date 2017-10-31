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

for years in range(2008, 2018):
    year = str(years)
    for qwerty in range(0, 15):
        
        url = None
        pageContent = None
        tree = None
        apteams = None
        uspoll = None
        playoffpoll = None
        bcspoll = None
        
#        year = '2007'
#        qwerty = 1
        
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
        
        
        if year == '2007':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h3/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2007-08-30'
        elif year == '2008':
            if qwerty != 0 and qwerty < 11:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h3/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            elif qwerty != 0 and qwerty >= 11:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2008-08-28' 
        elif year == '2009':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2009-09-02'            
        elif year == '2010':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2010-09-02'         
        elif year == '2011':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2011-09-01'         
        if year == '2012':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2012-08-30'         
        if year == '2013':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2013-08-30'         
        if year == '2014':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2014-08-28'         
        if year == '2015':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2015-09-02'         
        if year == '2016':
            if qwerty != 0:
                month, day, yearx = tree.xpath('//html/body/table/tr/td/table/tr/td/h4/text()')[0].split(' ')[1:4]
                month = monthdict[month]
                day = day[:-1]
                if len(day) == 1:
                    day = '0'+day
                date = yearx+'-'+month+'-'+day
            else:
                date = '2016-09-01'
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
        
        start = [m.start() for m in re.finditer('Mean Median St.Dev', pageContent.content)]
        endcontent = [m.start() for m in re.finditer('----------', pageContent.content)]
        startcontent = pageContent.content[start[0]:endcontent[0]]
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


        dataset = pd.DataFrame()
        stop = 0
        dbrow = 0
        dataspot = 0
        while stop != 1:
            line = []
            hcol = 0
            end = 0
            while end != 1: 
                if url == 'https://www.masseyratings.com/cf/arch/compare2016-12.htm' and hcol == 86 and dbrow == 89:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-0.htm' and hcol == 48 and dbrow == 118:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2017-0.htm' and hcol == 4 and dbrow == 109:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2017-0.htm' and hcol == 47 and dbrow == 109:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2017-0.htm' and hcol == 4 and dbrow == 125:
                    line.append(None)
                    hcol += 1       
                elif url == 'https://www.masseyratings.com/cf/arch/compare2017-0.htm' and hcol == 46 and dbrow == 125:
                    line.append(None)
                    hcol += 1 
                elif url == 'https://www.masseyratings.com/cf/arch/compare2017-0.htm' and hcol == 47 and dbrow == 125:
                    line.append(None)
                    hcol += 1 
                elif url == 'https://www.masseyratings.com/cf/arch/compare2016-8.htm' and hcol == 76 and dbrow == 82:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-2.htm' and hcol == 29 and dbrow == 109:
                    line.append(None)
                    hcol+=1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-3.htm' and hcol == 46 and dbrow == 119:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-4.htm' and hcol == 48 and dbrow in [113, 114, 119, 122, 123]:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-4.htm' and hcol == 56 and dbrow == 122:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-5.htm' and hcol == 86 and dbrow in [101, 109, 112, 122, 124]:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-6.htm' and hcol in [47, 111] and dbrow == 121:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-7.htm' and hcol == 113 and dbrow in [110, 120]:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2015-8.htm' and hcol == 103 and dbrow in [106, 124]:
                    line.append(None)
                    hcol += 1
                elif 'INP' in headers and qwerty < 12 and year == '2015' and qwerty > 8 and hcol == headers.index('INP')+1 and dbrow == masseyteams.index('Charlotte'):
                    line.append(None)
                    hcol += 1
                elif year == '2014' and qwerty < 4 and 'KAM' in headers and hcol == headers.index('KAM') and dbrow in [masseyteams.index('Georgia State'), masseyteams.index('GA Southern'), masseyteams.index('App State'), masseyteams.index('Old Dominion')]:
                    line.append(None)
                    hcol += 1
                elif year == '2014' and qwerty < 6 and 'TFG' in headers and hcol == headers.index('TFG') and dbrow in [masseyteams.index('GA Southern'),masseyteams.index('App State'), masseyteams.index('Old Dominion')]:
                    line.append(None)
                    hcol += 1  
                elif year == '2014' and 'WMR' in headers and hcol == headers.index('WMR') and dbrow in [masseyteams.index('GA Southern'),masseyteams.index('App State'), masseyteams.index('Old Dominion')]:
                    line.append(None)
                    hcol += 1   
                elif url == 'https://www.masseyratings.com/cf/arch/compare2014-0.htm' and 'NUT' in headers and hcol == headers.index('NUT') and dbrow in [masseyteams.index('GA Southern'), masseyteams.index('App State'), masseyteams.index('Old Dominion')]:
                    line.append(None)
                    hcol += 1   
                elif url == 'https://www.masseyratings.com/cf/arch/compare2013-5.htm' and dbrow == 49 and hcol == headers.index('RME'):
                    line.append(None)
                    hcol += 1   
                elif url == 'https://www.masseyratings.com/cf/arch/compare2014-0.htm' and dbrow == 110 and hcol in [11,20,53]:
                    line.append(None)
                    hcol += 1
                elif url == 'https://www.masseyratings.com/cf/arch/compare2014-5.htm' and hcol == headers.index('TPR') and dbrow in [masseyteams.index('U Mass'), masseyteams.index('Georgia State'), masseyteams.index('Texas State'), masseyteams.index('S Alabama'), masseyteams.index('TX-San Ant')]:
                    line.append(None)
                    hcol += 1
                elif year == '2013' and qwerty > 5 and qwerty < 8 and hcol == headers.index('TPR') and dbrow in [masseyteams.index('U Mass'), masseyteams.index('Texas State'), masseyteams.index('S Alabama'), masseyteams.index('TX-San Ant')]:
                    line.append(None)
                    hcol += 1                                        
                elif year == '2013' and qwerty == 8 and dbrow == masseyteams.index('Georgia State') and hcol in [headers.index('TFG'), headers.index('KAM')]:
                    line.append(None)
                    hcol += 1  
                elif year == '2013' and qwerty == 8 and hcol == headers.index('CCI') and dbrow in [masseyteams.index('Miami (OH)'), masseyteams.index('W Michigan')]:
                    line.append(None)
                    hcol += 1  
                elif year == '2013' and qwerty == 9 and hcol == headers.index('MDS') and dbrow in [masseyteams.index('Georgia State'), masseyteams.index('N Mex State')]:
                    line.append(None)
                    hcol += 1                  
                elif year == '2013' and qwerty == 9 and hcol == headers.index('KAM') and dbrow == masseyteams.index('Georgia State'):
                    line.append(None)
                    hcol += 1                      
                elif year == '2013' and qwerty == 10 and hcol == headers.index('KAM') and dbrow == masseyteams.index('Georgia State'):
                    line.append(None)
                    hcol += 1                      
                elif year == '2013' and qwerty >= 11 and hcol == headers.index('KAM') and dbrow == masseyteams.index('Georgia State'):
                    line.append(None)
                    hcol += 1                       
                elif year == '2013' and qwerty == 12 and hcol == headers.index('FPI') and dbrow == masseyteams.index('Ball State'):
                    line.append(None)
                    hcol += 1                      
                elif year == '2013' and qwerty >= 12 and hcol == headers.index('MPA') and dbrow == masseyteams.index('Georgia State'):
                    line.append(None)
                    hcol += 1
                elif year == '2013' and qwerty == 13 and hcol == headers.index('WOL') and dbrow == masseyteams.index('Colorado St'):
                    line.append(None)
                    hcol += 1
                elif year == '2013' and qwerty == 14 and hcol == headers.index('WOL') and dbrow == masseyteams.index('Texas State'):
                    line.append(None)
                    hcol += 1
                elif year == '2012' and qwerty == 0 and hcol == headers.index('DEZ') and dbrow == masseyteams.index('S Alabama'):
                    line.append(None)
                    hcol += 1   
                elif year == '2012' and qwerty == 3 and hcol == headers.index('BAS') and dbrow in [masseyteams.index('Wake Forest'), masseyteams.index('Fla Atlantic')]:
                    line.append(None)
                    hcol += 1                                 
                elif year == '2012' and qwerty < 3 and hcol == headers.index('KAM') and dbrow in [masseyteams.index('Texas State'), masseyteams.index('TX-San Ant'), masseyteams.index('S Alabama'), masseyteams.index('U Mass')]:
                    line.append(None)
                    hcol += 1
                elif year == '2012' and qwerty >= 5 and hcol == headers.index('UPS') and dbrow in [masseyteams.index('Texas State'), masseyteams.index('TX-San Ant'), masseyteams.index('S Alabama'), masseyteams.index('U Mass')]:
                    line.append(None)
                    hcol += 1
                elif year == '2012' and qwerty == 5 and hcol == headers.index('TFG') and dbrow in [masseyteams.index('Texas State')]:
                    line.append(None)
                    hcol += 1
                elif year == '2012' and qwerty >= 5 and qwerty < 8 and hcol == headers.index('TFG') and dbrow in [masseyteams.index('TX-San Ant')]:
                    line.append(None)
                    hcol += 1
                elif year == '2008' and qwerty >= 6 and hcol == headers.index('AND') and dbrow in [masseyteams.index('W Kentucky')]:
                    line.append(None)
                    hcol += 1
                elif year == '2007' and qwerty == 0 and hcol in [headers.index('LAW'),headers.index('DOK'),headers.index('DES'),headers.index('PFZ'),headers.index('PIG'),headers.index('NUT'), headers.index('KAM'), headers.index('MOR'), headers.index('CGV'), headers.index('D1A'), headers.index('BMC'), headers.index('BIL'), headers.index('BDF'), headers.index('UCS'), headers.index('SOL'), headers.index('GM')]  and dbrow in [masseyteams.index('W Kentucky')]:
                    line.append(None)
                    hcol += 1    
                elif year == '2007' and qwerty == 1 and hcol in [headers.index('PIG'),headers.index('FIT'), headers.index('KAM'), headers.index('MOR'), headers.index('CGV'), headers.index('D1A'), headers.index('BMC'), headers.index('BIL'), headers.index('LYD'), headers.index('BDF'), headers.index('UCS'), headers.index('SOL')]  and dbrow in [masseyteams.index('W Kentucky')]:
                    line.append(None)
                    hcol += 1   
                elif year == '2007' and qwerty == 2 and hcol in [headers.index('D1A'),headers.index('PIG'),headers.index('FIT'), headers.index('GM'), headers.index('CGV'), headers.index('KAM'), headers.index('BDF'), headers.index('BMC'), headers.index('BIL'), headers.index('SOL'), headers.index('UCS'), headers.index('JNK')]  and dbrow in [masseyteams.index('W Kentucky')]:
                    line.append(None)
                    hcol += 1  
                elif year == '2007' and qwerty == 3 and hcol in [headers.index('FIT'), headers.index('BMC'), headers.index('CGV'), headers.index('KAM'), headers.index('D1A'), headers.index('GM'), headers.index('BDF'), headers.index('BIL'), headers.index('UCS'), headers.index('SOL')]  and dbrow in [masseyteams.index('W Kentucky')]:
                    line.append(None)
                    hcol += 1 
                elif year == '2007' and qwerty == 4 and hcol in [headers.index('FIT'), headers.index('BMC'), headers.index('UCS'), headers.index('KAM'), headers.index('CGV'), headers.index('D1A'), headers.index('SOL'), headers.index('BDF'), headers.index('BIL'), headers.index('GM'), headers.index('BOB'), headers.index('GRN')]  and dbrow in [masseyteams.index('W Kentucky')]:
                    line.append(None)
                    hcol += 1 
                elif year == '2007' and qwerty == 5 and hcol in [headers.index('FIT'), headers.index('BMC'), headers.index('D1A'), headers.index('SOL'), headers.index('MJS'), headers.index('WEL'), headers.index('BOB'), headers.index('UCS'), headers.index('CGV'), headers.index('KAM'), headers.index('BDF'), headers.index('BIL'), headers.index('GRN')]  and dbrow in [masseyteams.index('W Kentucky')]:
                    line.append(None)
                    hcol += 1 
                    
                    
                    
                elif year == '2007' and qwerty == 1 and hcol in [headers.index('DKC')]  and dbrow in [masseyteams.index('Utah State')]:
                    line.append(None)
                    hcol += 1                     
                elif year == '2007' and qwerty == 2 and hcol in [headers.index('DKC')]  and dbrow in [masseyteams.index('Temple')]:
                    line.append(None)
                    hcol += 1                       
                elif year == '2007' and qwerty == 3 and hcol in [headers.index('DEV')]  and dbrow in [masseyteams.index('Oregon St'), masseyteams.index('Tennessee'), masseyteams.index('Michigan'), masseyteams.index('Oklahoma St'), masseyteams.index('Troy'), masseyteams.index('New Mexico'), masseyteams.index('Virginia'), masseyteams.index('Ball State'), masseyteams.index('Fresno St'), masseyteams.index('Navy'), masseyteams.index('Connecticut'), masseyteams.index('Kent State'), masseyteams.index('Minnesota')]:
                    line.append(None)
                    hcol += 1                      
                elif year == '2007' and qwerty == 3 and hcol in [headers.index('DEV')]  and dbrow > 72:
                    line.append(None)
                    hcol += 1   
                elif year == '2007' and qwerty == 4 and hcol in [headers.index('DEV')]  and dbrow in [masseyteams.index('Oregon St'), masseyteams.index('Indiana'), masseyteams.index('Colorado'), masseyteams.index('Virginia'), masseyteams.index('Pittsburgh'), masseyteams.index('New Mexico')]:
                    line.append(None)
                    hcol += 1                      
                elif year == '2007' and qwerty == 4 and hcol in [headers.index('DEV')]  and dbrow > 65:
                    line.append(None)
                    hcol += 1  
                elif year == '2007' and qwerty == 5 and hcol in [headers.index('DEV')]  and dbrow < 60 and dbrow in [masseyteams.index('Bowling Grn'), masseyteams.index('Miss State')]:
                    line.append(None)
                    hcol += 1                      
                elif year == '2007' and qwerty == 5 and hcol in [headers.index('DEV')]  and dbrow >= 60 and dbrow not in [73, 75]:
                    line.append(None)
                    hcol += 1  
                elif year == '2008' and qwerty == 15 and hcol in [headers.index('AND'), headers.index('DEZ')]  and dbrow == 118:
                    line.append(None)
                    hcol += 1 
                elif year == '2017' and qwerty >= 1 and hcol in [headers.index('KAM'), headers.index('SOR')]  and dbrow == masseyteams.index('Coastal Car'):
                    line.append(None)
                    hcol += 1 
                elif year == '2017' and qwerty >= 1 and qwerty < 7 and hcol in [headers.index('ENG')]  and dbrow == masseyteams.index('UAB'):
                    line.append(None)
                    hcol += 1 
                elif year == '2017' and qwerty == 4 and hcol in [headers.index('RME')]  and dbrow == masseyteams.index('Northwestern'):
                    line.append(None)
                    hcol += 1 
                elif year == '2017' and qwerty == 7 and hcol in [headers.index('RME')]  and dbrow == masseyteams.index('Northwestern'):
                    line.append(None)
                    hcol += 1                     
                    
                    
                elif year == '2014' and qwerty < 8 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in [masseyteams.index('Auburn'), masseyteams.index('Mississippi'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Baylor'), masseyteams.index('Notre Dame'), masseyteams.index('Michigan St')]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in [masseyteams.index('Auburn'), masseyteams.index('Mississippi'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Baylor'), masseyteams.index('Notre Dame'), masseyteams.index('Michigan St')]:
                        hcol += 1
                        line.append(None)
                elif year == '2014' and qwerty >= 8 and qwerty < 10 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in [masseyteams.index('Auburn'), masseyteams.index('Mississippi'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Notre Dame'), masseyteams.index('Michigan St'), masseyteams.index('Oregon')]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in [masseyteams.index('Auburn'), masseyteams.index('Mississippi'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Oregon'), masseyteams.index('Notre Dame'), masseyteams.index('Michigan St')]:
                        hcol += 1
                        line.append(None)
                elif year == '2014' and qwerty == 10 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in [masseyteams.index('Auburn'), masseyteams.index('TX Christian'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Notre Dame'), masseyteams.index('Michigan St'), masseyteams.index('Oregon')]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in [masseyteams.index('Auburn'), masseyteams.index('TX Christian'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Oregon'), masseyteams.index('Notre Dame'), masseyteams.index('Michigan St')]:
                        hcol += 1
                        line.append(None)
                elif year == '2014' and qwerty == 11 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in [masseyteams.index('Arizona St'), masseyteams.index('Baylor'), masseyteams.index('TX Christian'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Ohio State'), masseyteams.index('Oregon')]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in [masseyteams.index('Arizona St'),masseyteams.index('Baylor'), masseyteams.index('TX Christian'), masseyteams.index('Miss State'), masseyteams.index('Florida St'), masseyteams.index('Alabama'), masseyteams.index('Ohio State'), masseyteams.index('Oregon')]:
                        hcol += 1
                        line.append(None)
                elif year == '2014' and qwerty >= 12 and qwerty < 14 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in [masseyteams.index('Alabama'), masseyteams.index('Oregon'), masseyteams.index('Miss State'), masseyteams.index('TX Christian'), masseyteams.index('Florida St'), masseyteams.index('Baylor'), masseyteams.index('Ohio State'), masseyteams.index('Georgia')]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in [masseyteams.index('Alabama'), masseyteams.index('Oregon'), masseyteams.index('Miss State'), masseyteams.index('TX Christian'), masseyteams.index('Florida St'), masseyteams.index('Baylor'), masseyteams.index('Ohio State'), masseyteams.index('Georgia')]:
                        hcol += 1
                        line.append(None)
                elif year == '2014' and qwerty >= 14 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in [masseyteams.index('Alabama'), masseyteams.index('Oregon'), masseyteams.index('Michigan St'), masseyteams.index('TX Christian'), masseyteams.index('Florida St'), masseyteams.index('Baylor'), masseyteams.index('Ohio State'), masseyteams.index('Arizona')]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in [masseyteams.index('Alabama'), masseyteams.index('Oregon'), masseyteams.index('Michigan St'), masseyteams.index('TX Christian'), masseyteams.index('Florida St'), masseyteams.index('Baylor'), masseyteams.index('Ohio State'), masseyteams.index('Arizona')]:
                        hcol += 1
                        line.append(None)
                elif year == '2013' and qwerty < 4 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in range(0, 22) or dbrow == 24 or dbrow == 26 or dbrow == 34:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in range(0, 22) and dbrow != 24 and dbrow != 26 and dbrow != 34:
                        hcol += 1
                        line.append(None)
                elif year == '2013' and qwerty == 4 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in range(0, 19) or dbrow == 20 or dbrow == 22 or dbrow == 23 or dbrow == 25 or dbrow == 27 or dbrow == 30:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in range(0, 19) and dbrow != 20 and dbrow != 22 and dbrow != 23 and dbrow != 25 and dbrow != 27 and dbrow != 30:
                        hcol += 1
                        line.append(None)
                elif year == '2013' and qwerty == 5 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in range(0, 18) or dbrow == 19 or dbrow == 21 or dbrow == 26 or dbrow == 28 or dbrow == 30 or dbrow == 33 or dbrow == 36:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in range(0, 18) and dbrow != 19 and dbrow != 21 and dbrow != 26 and dbrow != 28 and dbrow != 30 and dbrow != 33 and dbrow != 36:
                        hcol += 1
                        line.append(None)
                elif year == '2013' and qwerty == 6 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in range(0, 19) or dbrow == 20 or dbrow == 23 or dbrow == 26 or dbrow == 27 or dbrow == 33 or dbrow == 35:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in range(0, 19) and dbrow != 20 and dbrow != 23 and dbrow != 26 and dbrow != 27 and dbrow != 33 and dbrow != 35:
                        hcol += 1
                        line.append(None)
                elif year == '2013' and qwerty == 7 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in range(0, 20) or dbrow in [23, 28, 30, 31, 38]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in range(0, 20) and dbrow not in [23, 28, 30, 31, 38]:
                        hcol += 1
                        line.append(None)
                elif year == '2013' and qwerty == 8 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in range(0, 18) or dbrow in [19, 20, 23, 24, 25, 31, 33]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in range(0, 18) and dbrow not in [19, 20, 23, 24, 25, 31, 33]:
                        hcol += 1
                        line.append(None)     
                elif year == '2013' and qwerty == 9 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow in range(0, 12) or dbrow in [13,14,16,17,18,19,20,22,23,24,31,34,35]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                    elif dbrow not in range(0, 12) and dbrow not in [13,14,16,17,18,19,20,22,23,24,31,34,35]:
                        hcol += 1
                        line.append(None)                        
                elif year == '2013' and qwerty == 10 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow == 19:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 23:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2013' and qwerty == 11 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2013' and qwerty == 12 and hcol == headers.index('LEG'):
                    if uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                    
                elif year == '2013' and qwerty == 13 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow == 21:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 24:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2013' and qwerty == 14 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow == 20:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 26:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2012' and qwerty == 3 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow == 31:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 26:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2012' and qwerty == 4 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow == 22 or dbrow == 26 or dbrow == 29 or dbrow == 35:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 20 or dbrow == 21 or dbrow == 32 or dbrow == 33 or dbrow == 41:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2012' and qwerty == 5 and 'LEG' in headers and hcol == headers.index('LEG'):
                    if dbrow == 15 or dbrow == 24:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 14 or dbrow == 35:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2012' and qwerty == 6 and hcol == headers.index('LEG'):
                    if uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2012' and qwerty == 7 and hcol == headers.index('LEG'):
                    if dbrow == 23 or dbrow == 24:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                             
                elif year == '2012' and qwerty == 8 and hcol == headers.index('LEG'):
                    if dbrow == 25 or dbrow == 28:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 19 or dbrow == 49:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2012' and qwerty == 9 and hcol == headers.index('LEG'):
                    if dbrow == 31:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 22:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2012' and qwerty == 10 and hcol == headers.index('LEG'):
                    if dbrow == 33:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 39:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)         
                elif year == '2012' and qwerty == 11 and hcol == headers.index('LEG'):
                    if dbrow == 22 or dbrow == 27:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 19 or dbrow == 21:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)          
                elif year == '2012' and qwerty == 12 and hcol == headers.index('LEG'):
                    if dbrow == 22 or dbrow == 28:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 34 or dbrow == 27:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)         
                elif year == '2012' and qwerty == 13 and hcol == headers.index('LEG'):
                    if dbrow == 16 or dbrow == 26 or dbrow == 27:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 19 or dbrow == 22 or dbrow == 33:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2012' and qwerty == 14 and hcol == headers.index('LEG'):
                    if dbrow == 29 or dbrow == 38:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 18 or dbrow == 24:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2011' and qwerty == 5 and hcol == headers.index('LEG'):
                    if dbrow == 32:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 34:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2011' and qwerty == 6 and hcol == headers.index('LEG'):
                    if dbrow == 25 or dbrow == 29:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 26 or dbrow == 30:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2011' and qwerty == 7 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2011' and qwerty == 8 and hcol == headers.index('LEG'):
                    if dbrow == 27:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 28:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)   
                elif year == '2011' and qwerty >= 9  and qwerty < 11 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2011' and qwerty == 11 and hcol == headers.index('LEG'):
                    if dbrow == 29 or dbrow == 30:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 21 or dbrow == 27 or dbrow == 33:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 12 and hcol == headers.index('LEG'):
                    if dbrow == 29:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 36:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 13 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2011' and qwerty == 14 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2010' and qwerty == 4 and hcol == headers.index('LEG'):
                    if dbrow == 31:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 22:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2010' and qwerty == 5 and hcol == headers.index('LEG'):
                    if dbrow in [35, 36]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 15 or dbrow == 26 or dbrow == 19:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2010' and qwerty == 6 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2010' and qwerty == 7 and hcol == headers.index('LEG'):
                    if dbrow == 23 or dbrow == 20:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 22 or dbrow == 31:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2010' and qwerty == 8 and hcol == headers.index('LEG'):
                    if dbrow == 23:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 28:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2010' and qwerty == 9 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2010' and qwerty == 10 and hcol == headers.index('LEG'):
                    if dbrow == 28 or dbrow == 35:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 22 or dbrow == 32:
                        hcol += 1
                        line.append(None) 
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2010' and qwerty == 11 and hcol == headers.index('LEG'):
                    if dbrow == 24 or dbrow == 18:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 22 or dbrow == 23:
                        hcol += 1
                        line.append(None) 
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2010' and qwerty == 12 and hcol == headers.index('LEG'):
                    if apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2010' and qwerty == 13 and hcol == headers.index('LEG'):
                    if dbrow == 52:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 30:
                        hcol += 1
                        line.append(None) 
                    elif grid['BCS'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['BCS'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2010' and qwerty == 14 and hcol == headers.index('LEG'):
                    if dbrow == 32:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 23:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2009' and qwerty == 5 and hcol == headers.index('LEG'):
                    if dbrow == 30 or dbrow == 16:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow == 22 or dbrow == 26:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2009' and qwerty == 6 and hcol == headers.index('LEG'):
                    if dbrow in [21, 22, 30]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow in [20, 23, 38]:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2009' and qwerty == 7 and hcol == headers.index('LEG'):
                    if dbrow in [29]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow in [28]:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                 
                elif year == '2009' and qwerty == 8 and hcol == headers.index('LEG'):
                    if dbrow in [24]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow in [20]:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2009' and qwerty == 9 and hcol == headers.index('LEG'):
                    if dbrow in [24, 25, 32, 31]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow in [14, 20, 23, 26]:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2009' and qwerty == 10 and hcol == headers.index('LEG'):
                    if dbrow in [28, 32]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow in [24, 13]:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2009' and qwerty == 11 and hcol == headers.index('LEG'):
                    if dbrow in [28]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                    elif dbrow in [31, 21]:
                        hcol += 1
                        line.append(None) 
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2009' and qwerty == 12 and hcol == headers.index('LEG'):                      
                    if dbrow in [19]:
                        hcol += 1
                        line.append(None) 
                    elif dbrow in [25]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2009' and qwerty == 13 and hcol == headers.index('LEG'):                      
                    if dbrow in [17, 27]:
                        hcol += 1
                        line.append(None) 
                    elif dbrow in [26, 31]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2009' and qwerty == 14 and hcol == headers.index('LEG'):                      
                    if dbrow in [27, 36]:
                        hcol += 1
                        line.append(None) 
                    elif dbrow in [26, 41]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)          
                elif year == '2008' and qwerty == 4 and hcol == headers.index('LEG'):                      
                    if dbrow in [14, 23, 39]:
                        hcol += 1
                        line.append(None) 
                    elif dbrow in [16, 22, 27]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2008' and qwerty == 5 and hcol == headers.index('LEG'):                      
                    if dbrow in [14]:
                        hcol += 1
                        line.append(None) 
                    elif dbrow in [20]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 6 and hcol == headers.index('LEG'):
                    if uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2008' and qwerty == 7 and hcol == headers.index('LEG'):
                    if dbrow == 14:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 25:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2008' and qwerty == 8 and hcol == headers.index('LEG'):
                    if dbrow == 14:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 23:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)         
                elif year == '2008' and qwerty == 9 and hcol == headers.index('LEG'):
                    if dbrow in [20, 40]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [42, 49]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)          
                elif year == '2008' and qwerty == 10 and hcol == headers.index('LEG'):
                    if dbrow in [25, 39]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [27, 33]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)          
                elif year == '2008' and qwerty == 11 and hcol == headers.index('LEG'):
                    if dbrow in [18]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [22]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                 
                elif year == '2008' and qwerty == 12 and hcol == headers.index('LEG'):
                    if dbrow in [35]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [22]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2008' and qwerty == 13 and hcol == headers.index('LEG'):
                    if uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 14 and hcol == headers.index('LEG'):
                    if dbrow in [23]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [29]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2008' and qwerty == 15 and hcol == headers.index('LEG'):
                    if dbrow in [20]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [24]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2009' and qwerty == 15 and hcol == headers.index('LEG'):
                    if dbrow in [23, 25]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [18, 35]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 




                        
        
        
        
        
        
                elif year == '2013' and qwerty <= 8 and 'HAR' in headers and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2013' and qwerty >= 9 and qwerty < 11 and 'HAR' in headers and hcol == headers.index('HAR'):
                    if dbrow == 27:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 12:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2013' and qwerty == 11 and hcol == headers.index('HAR'):
                    if grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                      
                elif year == '2013' and qwerty == 12 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2013' and qwerty >= 13 and hcol == headers.index('HAR'):
                    if grid['BCS'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['BCS'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2012' and qwerty == 6 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2012' and qwerty == 7 and hcol == headers.index('HAR'):
                    if dbrow == 19:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 18:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)     
                elif year == '2012' and qwerty == 8 and hcol == headers.index('HAR'):
                    if dbrow == 21:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 28:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2012' and qwerty == 9 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2012' and qwerty == 10 and hcol == headers.index('HAR'):
                    if dbrow == 39:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 20:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2012' and qwerty == 11 and hcol == headers.index('HAR'):
                    if dbrow == 19:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 27:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2012' and qwerty == 12 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2012' and qwerty == 13 and hcol == headers.index('HAR'):
                    if dbrow == 33:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 16:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                           
                elif year == '2012' and qwerty == 14 and hcol == headers.index('HAR'):
                    if dbrow == 24:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 38:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 6 and hcol == headers.index('HAR'):
                    if dbrow == 22 or dbrow == 30:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 25:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 7 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 8 and hcol == headers.index('HAR'):
                    if dbrow == 26:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 28:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['BCS'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['BCS'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 9 and hcol == headers.index('HAR'):
                    if dbrow == 23:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 31:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['BCS'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['BCS'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 10 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 11 and hcol == headers.index('HAR'):
                    if dbrow == 33 or dbrow == 20:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 32 or dbrow == 30:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['BCS'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['BCS'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2011' and qwerty == 12 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2011' and qwerty == 13 and hcol == headers.index('HAR'):
                    if dbrow == 30:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 20:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2011' and qwerty == 14 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2010' and qwerty == 7 and hcol == headers.index('HAR'):
                    if dbrow == 22:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 23 or dbrow == 26:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2010' and qwerty == 8 and hcol == headers.index('HAR'):
                    if dbrow == 21:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 23:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)
                elif year == '2010' and qwerty == 9 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2010' and qwerty == 10 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2010' and qwerty == 11 and hcol == headers.index('HAR'):
                    if dbrow == 18:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 24:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2010' and qwerty == 12 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2010' and qwerty >= 13 and hcol == headers.index('HAR'):
                    if grid['BCS'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['BCS'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 
                elif year == '2009' and qwerty in [4,5] and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2009' and qwerty == 6 and hcol == headers.index('HAR'):
                    if dbrow == 25:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 21:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2009' and qwerty == 7 and hcol == headers.index('HAR'):
                    if dbrow == 25:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 29:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2009' and qwerty in [8,9] and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                elif year == '2009' and qwerty == 10 and hcol == headers.index('HAR'):
                    if dbrow == 24:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 28:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2009' and qwerty == 11 and hcol == headers.index('HAR'):
                    if dbrow == 29:
                        hcol += 1
                        line.append(None)                                                 
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2009' and qwerty == 12 and hcol == headers.index('HAR'):
                    if dbrow == 19:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 22:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2009' and qwerty >= 13 and hcol == headers.index('HAR'):
                    if grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2008' and qwerty == 5 and hcol == headers.index('HAR'):
                    if grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)  
                elif year == '2008' and qwerty == 6 and hcol == headers.index('HAR'):
                    if dbrow == 20:
                        hcol += 1
                        line.append(None)
                    elif dbrow == 25:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 7 and hcol == headers.index('HAR'):
                    if grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                          
                elif year == '2008' and qwerty == 8 and hcol == headers.index('HAR'):
                    if grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 9 and hcol == headers.index('HAR'):
                    if dbrow == 40:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [24, 27]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 10 and hcol == headers.index('HAR'):
                    if dbrow == 25:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [27]:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                   
                    elif grid['USA'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['USA'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                elif year == '2008' and qwerty == 11 and hcol == headers.index('HAR'):
                    if dbrow in [18]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [22]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 12 and hcol == headers.index('HAR'):
                    if dbrow in [22]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [25]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 13 and hcol == headers.index('HAR'):
                    if dbrow in [25]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [27]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 14 and hcol == headers.index('HAR'):
                    if grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                                                  
                elif year == '2007' and qwerty == 4 and hcol == headers.index('HAR'):
                    if dbrow in [21]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [12]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                           
                elif year == '2007' and qwerty == 5 and hcol == headers.index('HAR'):
                    if dbrow in [19]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [29]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif uscol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif uscol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                         
                elif year == '2008' and qwerty == 15 and hcol == headers.index('HAR'):
                    if grid['AP'][dbrow] == None:
                        hcol += 1
                        line.append(None)
                    elif grid['AP'][dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None)                        
                        
                        





                elif year == '2007' and qwerty == 5 and hcol == headers.index('MCS'):
                    if dbrow in [24]:
                        hcol += 1
                        line.append(None)
                    elif dbrow in [38]:
                        hcol += 1
                        line.append(None)
                        dataspot += 1
                    elif apcol[dbrow] == None:
                        hcol += 1
                        line.append(None)   
                    elif apcol[dbrow] != None:
                        hcol += 1
                        dataspot += 1
                        line.append(None) 

                        
                        
                        
                        
                        
                        
                elif url == 'https://www.masseyratings.com/cf/arch/compare2013-3.htm' and dbrow == 102 and hcol == 46:
                    hcol += 1
                    line.append(None)
                elif url == 'https://www.masseyratings.com/cf/arch/compare2013-4.htm' and dbrow in [masseyteams.index('Northwestern'), masseyteams.index('Notre Dame')] and hcol == headers.index('RME'):
                    hcol += 1
                    line.append(None)
                elif year == '2013' and qwerty < 9 and 'KAM' in headers and hcol == headers.index('KAM') and dbrow == masseyteams.index('Georgia State'):
                    hcol += 1
                    line.append(None)
                elif year == '2013' and qwerty < 9 and 'TFG' in headers and hcol == headers.index('TFG') and dbrow == masseyteams.index('Georgia State'):
                    hcol += 1
                    line.append(None)     
                elif year == '2013' and qwerty == 9 and hcol in [headers.index('KAM'), headers.index('MDS')] and dbrow == masseyteams.index('Georgia State'):
                    hcol += 1
                    line.append(None)  
                elif year == '2013' and qwerty == 9 and hcol == headers.index('MDS') and dbrow == masseyteams.index('N Mex State'):
                    hcol += 1
                    line.append(None) 
                elif url == 'https://www.masseyratings.com/cf/arch/compare2014-14.htm' and dbrow == 37 and hcol == 60:
                    hcol +=1
                    line.append(None)
                elif url == 'https://www.masseyratings.com/cf/arch/compare2013-2.htm' and dbrow == 1 and hcol == headers.index('ARG'):
                    hcol += 1
                    line.append(None)
                    
                    

                elif hcol in indices:
                    if url == 'https://www.masseyratings.com/cf/arch/compare2016-7.htm' and hcol == 90 and dbrow == 78:
                        line.append(None)
                        hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2012-12.htm' and dbrow == 8:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2011-4.htm' and dbrow == 109:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2010-0.htm' and dbrow == 82:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2010-1.htm' and dbrow == 60:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2010-2.htm' and dbrow == 62:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2009-1.htm' and dbrow == 103:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2009-10.htm' and dbrow == 88:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2008-4.htm' and dbrow == 105:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2007-1.htm' and dbrow == 52:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2007-2.htm' and dbrow == 79:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2011-2.htm' and dbrow == 10:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2011-11.htm' and dbrow == 73:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2012-13.htm' and dbrow == 83:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2012-2.htm' and dbrow == 51:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2012-2.htm' and dbrow == 52:
                        if ratings[dataspot] == dbrow -1:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2015-4.htm' and dbrow == 96:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-0.htm' and dbrow == 47:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2014-13.htm' and dbrow == 109:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2014-6.htm' and dbrow == 88:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2014-4.htm' and dbrow == 125:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2015-0.htm' and dbrow == 106:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-2.htm' and dbrow == 67:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-14.htm' and dbrow == 111:
                        if ratings[dataspot] == dbrow:
                            dataspot += 1
                            hcol += 1
                    elif ratings[dataspot] == dbrow+1:
                        dataspot += 1
                        hcol += 1
                    else:
                        end = 1
                        
                        
                        
                        
                        
                elif hcol == usspotx:
                    if url == 'https://www.masseyratings.com/cf/arch/compare2013-5.htm' and dbrow == 16:
                            line.append(None)
                            hcol += 1
                            dataspot += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-5.htm' and dbrow == 20:
                            line.append(grid['USA'][dbrow])
                            hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-5.htm' and dbrow == 21:
                            line.append(grid['USA'][dbrow])
                            hcol += 1
                            dataspot += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-5.htm' and dbrow == 26:
                            line.append(grid['USA'][dbrow])
                            hcol += 1
                            dataspot += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-5.htm'and dbrow == 15:
                            line.append(grid['USA'][dbrow])
                            hcol +=1
                            dataspot +=1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2013-5.htm'and dbrow == 2:
                            line.append(grid['USA'][dbrow])
                            hcol +=1
                            dataspot +=1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2015-11.htm' and hcol == 89 and dbrow == 20:
                        line.append(25)
                        hcol += 1
                    elif url == 'https://www.masseyratings.com/cf/arch/compare2007-4.htm' and hcol == 72 and dbrow == 12:
                        line.append(25)
                        hcol += 1
                    else:
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
                        if qwerty == 10 and dbrow == 23 and year == '2010':
                            line.append(None)
                            hcol += 1
                        elif year in ['2009', '2008'] and qwerty >= 10:
                            line.append(None)
                            hcol += 1
                            dataspot += 1
                        elif qwerty >= 10:
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
                            if year == '2011' and qwerty == 13:
                                if grid['BCS'][dbrow] != None and dbrow != 33 or dbrow == 23:
                                    line.append(ratings[dataspot])
                                    hcol +=1
                                    dataspot += 1   
                                elif grid['BCS'][dbrow] == None or dbrow == 33:
                                    line.append(None)
                                    hcol +=1
                            elif ratings[dataspot] == grid['BCS'][dbrow]:
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
           



        sqllabels = None            
        sqlstaging = None 
        sqldb = None
        masseylist = None
        masseyinsert = None
        masseyinsertx = None
        add_massey = None
        initialmasseyinsert = None
        if len(masseyteams) == len(dataset):        
            sqllabels = ['Team', 'PIR', 'OSC', 'UCC', 'KPK', 'COF', 'LAZ', 'RWP', 'ACU', 'PAY', 'JTR', 'MTN', 'RT', 'DII', 'ASH', 'FMG', 'RUD', 'MGS', 'ARG', 'SOR', 'WLK', 'SEL', 'HEN', 'HAT', 'MAS', 'HKB', 'DOL', 'MvG', 'KEE', 'FAS', 'SAG', 'BIH', 'HOW', 'GRS', 'ENG', 'JRT', 'STH', 'PGH', 'RTH', 'HNL', 'KH', 'EZ', 'WOB', 'ABC', 'ISR', 'JNK', 'AND', 'COL', 'BOW', 'YCM', 'PCP', 'SOL', 'WOL', 'EFI', 'BSS', 'KRA', 'WIL', 'LOG', 'BWE', 'BBT', 'RTP', 'RFL', 'WWP', 'KLK', 'REW', 'DUN', 'KEL', 'DP', 'BIL', 'ONV', 'KNT', 'MCK', 'BMC', 'SP', 'LSW', 'GLD', 'WEL', 'BCM', 'MCL', 'LSD', 'MAR', 'DOI', 'DOK', 'TRP', 'VRN', 'INP', 'MJS', 'CSL', 'DEZ', 'RME', 'DWI', 'DES', 'KEN', 'MOR', 'DCI', 'CTW', 'FPI', 'PPP', 'MRK', 'TFG', 'MDS', 'BAS', 'GRR', 'BRN', 'GBE', 'RSL', 'PIG', 'SFX', 'FEI', 'CGV', 'KAM', 'CFP', 'S&P', 'RBA', 'NOL', 'PFZ', 'MGN', 'TPR', 'BDF', 'D1A', 'ATC', 'CMV', 'MVP', 'NUT', 'RTB']
            sqlstaging = pd.DataFrame(columns = sqllabels)
            sqlstaging['Team'] = masseyteams
            
            num = 0
            for each in sqllabels:
                if each in list(dataset):
                    sqlstaging[each] = dataset[each]
                    num += 1
            sqlstaging.fillna('Null', inplace = True)                    
            sqldb = np.array(sqlstaging) 

        for team in sqldb:
            masseyinsert = []
            masseyinsert.append("('"+team[0]+"', '"+str(date)+"', "+str(team[1])+', '+str(team[2])+', '+str(team[3])+', '+str(team[4])+', '+str(team[5])+', '+str(team[6])+', '+str(team[7])+', '+str(team[8])+', '+str(team[9])+', '+str(team[10])+', '+str(team[11])+', '+str(team[12])+', '+str(team[13])+', '+str(team[14])+', '+str(team[15])+', '+str(team[16])+', '+str(team[17])+', '+str(team[18])+', '+str(team[19])+', '+str(team[20])+', '+str(team[21])+', '+str(team[22])+', '+str(team[23])+', '+str(team[24])+', '+str(team[25])+', '+str(team[26])+', '+str(team[27])+', '+str(team[28])+', '+str(team[29])+', '+str(team[30])+', '+str(team[31])+', '+str(team[32])+', '+str(team[33])+', '+str(team[34])+', '+str(team[35])+', '+str(team[36])+', '+str(team[37])+', '+str(team[38])+', '+str(team[39])+', '+str(team[40])+', '+str(team[41])+', '+str(team[42])+', '+str(team[43])+', '+str(team[44])+', '+str(team[45])+', '+str(team[46])+', '+str(team[47])+', '+str(team[48])+', '+str(team[49])+', '+str(team[50])+', '+str(team[51])+', '+str(team[52])+', '+str(team[53])+', '+str(team[54])+', '+str(team[55])+', '+str(team[56])+', '+str(team[57])+', '+str(team[58])+', '+str(team[59])+', '+str(team[60])+', '+str(team[61])+', '+str(team[62])+', '+str(team[63])+', '+str(team[64])+', '+str(team[65])+', '+str(team[66])+', '+str(team[67])+', '+str(team[68])+', '+str(team[69])+', '+str(team[70])+', '+str(team[71])+', '+str(team[72])+', '+str(team[73])+', '+str(team[74])+', '+str(team[75])+', '+str(team[76])+', '+str(team[77])+', '+str(team[78])+', '+str(team[79])+', '+str(team[80])+', '+str(team[81])+', '+str(team[82])+', '+str(team[83])+', '+str(team[84])+', '+str(team[85])+', '+str(team[86])+', '+str(team[87])+', '+str(team[88])+', '+str(team[89])+', '+str(team[90])+', '+str(team[91])+', '+str(team[92])+', '+str(team[93])+', '+str(team[94])+', '+str(team[95])+', '+str(team[96])+', '+str(team[97])+', '+str(team[98])+', '+str(team[99])+', '+str(team[100])+', '+str(team[101])+', '+str(team[102])+', '+str(team[103])+', '+str(team[104])+', '+str(team[105])+', '+str(team[106])+', '+str(team[107])+', '+str(team[108])+', '+str(team[109])+', '+str(team[110])+', '+str(team[111])+', '+str(team[112])+', '+str(team[113])+', '+str(team[114])+', '+str(team[115])+', '+str(team[116])+', '+str(team[117])+', '+str(team[118])+', '+str(team[119])+', '+str(team[120])+', '+str(team[121])+', '+str(team[122])+', '+str(team[123])+', '+str(team[124])+")")
            masseyinsertx = ','.join(masseyinsert)
            masseylist = ['INSERT INTO masseyratings VALUES', masseyinsertx, ';']
            initialmasseyinsert = ' '.join(masseylist)  
            add_massey = initialmasseyinsert  
            cursor.execute('SET foreign_key_checks = 0;')
            cursor.execute(add_massey)
        cnx.commit()
        cursor.execute('SET foreign_key_checks = 1;')
        print date

cursor.close()
cnx.close()     

    
#insertlist = []
#for x in range(1, len(sqldb[0])):
#    bv = '+str(team[%s])+'% (x)
#    print bv
#    insertlist.append(bv)
#gh = "', '".join(insertlist)
#print gh