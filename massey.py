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


teamnames = ['Air Force', 'Akron', 'Alabama', 'App State', 'Arizona', 'Arizona St', 'Arkansas', 'Arkansas St', 'Army', 'Auburn', 'BYU', 'Ball State', 'Baylor', 'Boise State', 'Boston Col', 'Bowling Grn', 'Buffalo', 'California', 'Central FL', 'Central Mich', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado St', 'Connecticut', 'Duke', 'E Carolina', 'E Michigan', 'Fla Atlantic', 'Florida', 'Florida Intl', 'Florida St', 'Fresno St', 'GA Southern', 'GA Tech', 'Georgia', 'Georgia State', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas St', 'Kent State', 'Kentucky', 'LA Lafayette', 'LA Monroe', 'LA Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland', 'Memphis', 'Miami (FL)', 'Miami (OH)', 'Michigan', 'Michigan St', 'Middle Tenn', 'Minnesota', 'Miss State', 'Mississippi', 'Missouri', 'N Carolina', 'N Illinois', 'N Mex State', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma St', 'Old Dominion', 'Oregon', 'Oregon St', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'S Alabama', 'S Carolina', 'S Florida', 'S Methodist', 'S Mississippi', 'San Diego St', 'San Jose St', 'Stanford', 'Syracuse', 'TX Christian', 'TX El Paso', 'TX-San Ant', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'U Mass', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah State', 'VA Tech', 'Vanderbilt', 'Virginia', 'W Kentucky', 'W Michigan', 'W Virginia', 'Wake Forest', 'Wash State', 'Washington', 'Wisconsin', 'Wyoming', 'W Kentucky', 'Middle Tenn']
teamlist = ['Air Force', 'Akron', 'Alabama', 'Appalachian St', 'Arizona', 'Arizona St', 'Arkansas', 'Arkansas St', 'Army','Auburn', 'BYU', 'Ball St', 'Baylor', 'Boise St', 'Boston College', 'Bowling Green', 'Buffalo', 'California', 'UCF','C Michigan', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado St', 'Connecticut', 'Duke','East Carolina','E Michigan',  'FL Atlantic', 'Florida', 'Florida Intl', 'Florida St', 'Fresno St', 'Ga Southern',  'Georgia Tech','Georgia', 'Georgia St', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa St', 'Kansas', 'Kansas St', 'Kent', 'Kentucky', 'ULL', 'ULM', 'Louisiana Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland','Memphis', 'Miami FL', 'Miami OH', 'Michigan', 'Michigan St', 'MTSU', 'Minnesota', 'Mississippi St', 'Mississippi', 'Missouri', 'North Carolina', 'N Illinois', 'New Mexico St', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio St', 'Oklahoma', 'Oklahoma St', 'Old Dominion', 'Oregon', 'Oregon St', 'Penn St', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'South Alabama', 'South Carolina', 'South Florida',  'SMU', 'Southern Miss', 'San Diego St', 'San Jose St', 'Stanford', 'Syracuse', 'TCU', 'UTEP', 'UT San Antonio', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas St', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'Massachusetts', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah St', 'Virginia Tech', 'Vanderbilt', 'Virginia',  'WKU', 'W Michigan', 'West Virginia', 'Wake Forest',  'Washington St', 'Washington',  'Wisconsin', 'Wyoming', 'W Kentucky', 'Middle Tenn St']

espnlist = ['Air Force', 'Akron', 'Alabama', 'Appalachian State', 'Arizona', 'Arizona State', 'Arkansas', 'Arkansas St', 'Army','Auburn', 'BYU', 'Ball State', 'Baylor', 'Boise State', 'Boston College', 'Bowling Green', 'Buffalo', 'California', 'UCF','C Michigan', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado State', 'Connecticut', 'Duke','East Carolina','E Michigan',  'FL Atlantic', 'Florida', 'Florida Intl', 'Florida State', 'Fresno State', 'Ga Southern',  'Georgia Tech','Georgia', 'Georgia St', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa St', 'Kansas', 'Kansas State', 'Kent', 'Kentucky', 'ULL', 'ULM', 'Louisiana Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland','Memphis', 'Miami', 'Miami OH', 'Michigan', 'Michigan State', 'MTSU', 'Minnesota', 'Mississippi State', 'Ole Miss', 'Missouri', 'North Carolina', 'Northern Illinois', 'New Mexico St', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma State', 'Old Dominion', 'Oregon', 'Oregon State', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'South Alabama', 'South Carolina', 'South Florida',  'SMU', 'Southern Miss', 'San Diego State', 'San Jose State', 'Stanford', 'Syracuse', 'TCU', 'UTEP', 'UT San Antonio', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'Massachusetts', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah State', 'Virginia Tech', 'Vanderbilt', 'Virginia',  'Western Kentucky', 'Western Michigan', 'West Virginia', 'Wake Forest',  'Washington State', 'Washington',  'Wisconsin', 'Wyoming']

teamsdict = {}
for i in range(0, len(teamnames)):
    teamsdict[teamlist[i]] = teamnames[i]
espndict = {}
for i in range(0, len(espnlist)):
    espndict[espnlist[i]] = teamnames[i]

for year in ['2012']:
    for qwerty in range(0, 15):
                
        url = None
        pageContent = None
        tree = None
        apteams = None
        uspoll = None
        playoffpoll = None
        bcspoll = None
        
#        year = '2014'
#        qwerty = 0
        
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
        
        
        url = None
        pageContent = None
        tree = None
        rankingabbrev = None
        headers = None
        rankabbrev = None
        url = 'https://www.masseyratings.com/cf/arch/compare%s-%s.htm'%(year, qwerty)
        pageContent=requests.get(url)
        
        
        tree = html.fromstring(pageContent.content)
        rankingabbrev = tree.xpath('//html/body/pre/font/text()')[0].split(' ')
        headers = []
        rankabbrev = []
        
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
            aplist.append(espndict[team])
        uslist = []
        for team in uspoll:
            uslist.append(espndict[team]) 
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
                bcslist.append(espndict[team])         
            bcscol = []
            for team in masseyteams:
                if team in bcslist:
                    bcscol.append(bcslist.index(team)+1)
                else:
                    bcscol.append(None)   
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
           
            
            
            
            
            
            
            
        print qwerty