#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:09:35 2017

@author: eric.hensleyibm.com
"""

def baseteamdata(week):
    import pandas as pd
    from lxml import html
    import requests
    
    ratinglist = ['predictive-by-other', 'home-by-other', 'away-by-other', 'neutral-by-other', 
              'home-adv-by-other', 'schedule-strength-by-other', 'future-sos-by-other', 
              'season-sos-by-other', 'sos-basic-by-other', 'in-conference-sos-by-other',
              'non-conference-sos-by-other', 'last-5-games-by-other', 'last-10-games-by-other',
              'in-conference-by-other', 'non-conference-by-other', 'luck-by-other',
              'consistency-by-other', 'vs-1-10-by-other', 'vs-11-25-by-other', 'vs-26-40-by-other',
              'vs-41-75-by-other', 'vs-76-120-by-other', 'first-half-by-other', 'second-half-by-other']
    
    teamnames = ['Air Force', 'Akron', 'Alabama', 'App State', 'Arizona', 'Arizona St', 'Arkansas',
                 'Arkansas St', 'Army', 'Auburn', 'BYU', 'Ball State', 'Baylor', 'Boise State', 'Boston Col', 
                 'Bowling Grn', 'Buffalo', 'California', 'Central FL', 'Central Mich', 'Charlotte', 
                 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado St', 'Connecticut', 'Duke', 
                 'E Carolina', 'E Michigan', 'Fla Atlantic', 'Florida', 'Florida Intl', 'Florida St', 'Fresno St',
                 'GA Southern', 'GA Tech', 'Georgia', 'Georgia State', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 
                 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas St', 'Kent State', 'Kentucky', 'LA Lafayette',
                 'LA Monroe', 'LA Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland', 'Memphis', 'Miami (FL)', 
                 'Miami (OH)', 'Michigan', 'Michigan St', 'Middle Tenn', 'Minnesota', 'Miss State', 'Mississippi', 
                 'Missouri', 'N Carolina', 'N Illinois', 'N Mex State', 'NC State', 'Navy', 'Nebraska', 'Nevada', 
                 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 
                 'Oklahoma St', 'Old Dominion', 'Oregon', 'Oregon St', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 
                 'Rutgers', 'S Alabama', 'S Carolina', 'S Florida', 'S Methodist', 'S Mississippi', 'San Diego St',
                 'San Jose St', 'Stanford', 'Syracuse', 'TX Christian', 'TX El Paso', 'TX-San Ant', 'Temple', 
                 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 
                 'U Mass', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah State', 'VA Tech', 'Vanderbilt', 'Virginia',
                 'W Kentucky', 'W Michigan', 'W Virginia', 'Wake Forest', 'Wash State', 'Washington', 'Wisconsin', 'Wyoming']

    
    weeklyratings = pd.DataFrame()
    weeklyratings = weeklyratings.append(teamnames)
    weeklyratings = weeklyratings.rename(columns = {0:'teamname'})
    for each in ratinglist:
        tree = None
        url = None
        names = None
        rating = None
        rankingdict = None
        ranking = None
        url = 'https://www.teamrankings.com/college-football/ranking/%s?date=%s' % (each, week)
        pageContent=requests.get(url)
        tree = html.fromstring(pageContent.content)
        names = tree.xpath('//*[@class="tr-table datatable scrollable"]/tbody/tr/td/a/text()')
        rating = tree.xpath('//*[@class="tr-table datatable scrollable"]/tbody/tr/td[3]/text()')
        rankingdict = {}
        for i in range(0, len(names)):
            try:
                rankingdict[names[i]] = float(rating[i])
            except ValueError:
                if rating[i] == '--':
                    rankingdict[names[i]] = 0
        ranking = []
        for name in teamnames:
            try:
                ranking.append(rankingdict[name])
            except KeyError:
                ranking.append("Null")
        weeklyratings[each] = ranking
    return weeklyratings