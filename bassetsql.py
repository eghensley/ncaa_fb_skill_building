# -*- coding: utf-8 -*-
"""
Created on Fri Oct 06 14:24:03 2017

@author: Eric
"""

def bassetsqlinsert(passcode):
    import requests
    from lxml import html
    import re
    import mysql.connector   
    cnx = mysql.connector.connect(user='root', password=passcode,
                                  host='127.0.0.1',
                                  database='ncaa')    
    cursor = cnx.cursor() 
    
    
    teamnames = ['Air Force', 'Akron', 'Alabama', 'App State', 'Arizona', 'Arizona St', 'Arkansas', 'Arkansas St', 'Army', 'Auburn', 'BYU', 'Ball State', 'Baylor', 'Boise State', 'Boston Col', 'Bowling Grn', 'Buffalo', 'California', 'Central FL', 'Central Mich', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado St', 'Connecticut', 'Duke', 'E Carolina', 'E Michigan', 'Fla Atlantic', 'Florida', 'Florida Intl', 'Florida St', 'Fresno St', 'GA Southern', 'GA Tech', 'Georgia', 'Georgia State', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas St', 'Kent State', 'Kentucky', 'LA Lafayette', 'LA Monroe', 'LA Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland', 'Memphis', 'Miami (FL)', 'Miami (OH)', 'Michigan', 'Michigan St', 'Middle Tenn', 'Minnesota', 'Miss State', 'Mississippi', 'Missouri', 'N Carolina', 'N Illinois', 'N Mex State', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma St', 'Old Dominion', 'Oregon', 'Oregon St', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'S Alabama', 'S Carolina', 'S Florida', 'S Methodist', 'S Mississippi', 'San Diego St', 'San Jose St', 'Stanford', 'Syracuse', 'TX Christian', 'TX El Paso', 'TX-San Ant', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'U Mass', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah State', 'VA Tech', 'Vanderbilt', 'Virginia', 'W Kentucky', 'W Michigan', 'W Virginia', 'Wake Forest', 'Wash State', 'Washington', 'Wisconsin', 'Wyoming']
    bassetnames = ['Air Force', 'Akron', 'Alabama',  'Appalachian State', 'Arizona', 'Arizona State', 'Arkansas', 'Arkansas State', 'Army', 'Auburn', 'Brigham Young', 'Ball State', 'Baylor', 'Boise State', 'Boston College', 'Bowling Green',  'Buffalo', 'California', 'Central Florida', 'Central Michigan',  'North Carolina - Charlot', 'Cincinnati', 'Clemson', 'Coastal Carolina', 'Colorado', 'Colorado State', 'Connecticut', 'Duke', 'East Carolina', 'Eastern Michigan',  'Florida Atlantic',  'Florida','Florida International', 'Florida State', 'Fresno State','Georgia Southern', 'Georgia Tech', 'Georgia', 'Georgia State', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas State', 'Kent State', 'Kentucky', 'Louisiana - Lafayette', 'Northeast Louisiana', 'Louisiana Tech',  'Louisiana State', 'Louisville', 'Marshall', 'Maryland', 'Memphis', 'Miami - Florida', 'Miami - Ohio', 'Michigan', 'Michigan State', 'Middle Tennessee State', 'Minnesota', 'Mississippi State',  'Mississippi','Missouri',  'North Carolina', 'Northern Illinois',  'New Mexico State','North Carolina State','Navy', 'Nebraska', 'Nevada - Reno',  'New Mexico', 'North Texas',  'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma State', 'Old Dominion', 'Oregon', 'Oregon State', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'South Alabama', 'South Carolina', 'South Florida', 'Southern Methodist', 'Southern Mississippi', 'San Diego State', 'San Jose State','Stanford', 'Syracuse',  'Texas Christian',  'Texas - El Paso', 'Texas - San Antonio', 'Temple', 'Tennessee', 'Texas','Texas A&M','Texas State - San Marcos', 'Texas Tech', 'Toledo', 'Troy State', 'Tulane', 'Tulsa',   'Massachusetts','Alabama - Birmingham','California - Los Angeles','Nevada - Las Vegas','Southern California',  'Utah', 'Utah State', 'Virginia Tech', 'Vanderbilt', 'Virginia', 'Western Kentucky', 'Western Michigan', 'West Virginia', 'Wake Forest', 'Washington State',  'Washington','Wisconsin', 'Wyoming']
    monthdict = {'Jan':1, 'Feb':2, 'Mar':3, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    bassetteamsdict = {}
    for i in range(0, len(teamnames)):
        bassetteamsdict[teamnames[i]] = bassetnames[i]
    
    
    seasonrange = ['03','04','05','06','07','08','09','10','11','12','13','14','15','16','17']
    weekrange = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
    
    for season in seasonrange:
        nextseason = 0
        for week in weekrange:
            bassetinsertx = None
            bassetinsert = []
            data = None
            pageContent = None
            tree = None
            invalid = None
            thisdate = None
            year = None
            month = None
            day = None
            day = None
            usedate = None
            r = None
            teamratings = []
            if nextseason == 1:
                pass
            else:
                url = 'http://gmbassett.nfshost.com/football/col_%swk%spred.html' % (season,week)
#                url = 'http://gmbassett.nfshost.com/football/col_07wk02pred.html'
                pageContent=requests.get(url)
                tree = html.fromstring(pageContent.content)
                invalid = tree.xpath('//html/head/title/text()')
                if invalid[0] == '404 Not Found':
                    if week == '00':
                        pass
                    else:
                        nextseason = 1
                else:
                    thisdate = tree.xpath('//html/body/h1/text()')[0].strip().split(' ')
                    bowlcheck = thisdate[1]
                    if bowlcheck == 'Bowl':
                        nextseason = 1
                        pass
                    else:
                        year = thisdate[0]
                        for q in range(0, len(thisdate)):
                            if thisdate[q] == 'Forecast':
                                try:
                                    month = str(monthdict[thisdate[q-1][:-1]])
                                    r = q-2
                                except KeyError:
                                    for w in range(0, q-1):
                                        try:
                                            month = str(monthdict[thisdate[w][:-1]])
                                            r = w-1
                                        except KeyError:
                                            continue                                   
                                try:
                                    day = str(int(thisdate[r]))
                                except ValueError:
                                    try:
                                        day = str(int(thisdate[r][1:]))
                                    except ValueError:
                                        day = str(int(thisdate[r].split('-')[1]))     
                        if month == None:
                            for q in range(0, len(thisdate)):
                                if thisdate[q] == 'for':
                                    month = str(monthdict[thisdate[q-1][:-1]])
                                    day = str(int(thisdate[q-2][1:]))
                                    
#                        try:
#                            month = str(monthdict[thisdate[4][:-1]])
#                        except KeyError:
#                            try:
#                                month = str(monthdict[thisdate[4]])
#                            except KeyError:
#                                month = str(monthdict[thisdate[3][:-1]])
#                        try:
##                            int(thisdate[3][1:].split('-')[0])
##                            day = thisdate[3][1:].split('-')[0]
#                            day = int(thisdate[3].split('-')[1])
#                        except IndexError:
#                            try:
#                                day = int(thisdate[3][1:])
#                            except ValueError:
#                                day = int(thisdate[2][1:])
                        usedate = year+'-'+month+'-'+day
                        data = str(tree.xpath('/html/body/pre/text()'))
                        for team in teamnames:
                            emptypass = 0
                            partialpass = 0
                            nameindex = None
                            namematch = None
                            nameloc = None
                            rank = None
                            ratingtuple = None
                            ratingtuplelist = []
                            nameindex = bassetteamsdict[team]+'  '
                            namematch = [m.start() for m in re.finditer(nameindex, data)]
                            for v in range(0, len(namematch)):
                                emptypass = 0
                                partialpass = 0
                                nameloc = None
                                rank = None
                                ratingtuple = None
                                try:
                                    nameloc = namematch[v]
                                except IndexError:
                                    emptypass = 1
                                if emptypass == 0:
                                    try:
                                        int(data[nameloc-2])
                                    except ValueError:
                                        partialpass = 1
                                if emptypass == 0 and partialpass == 0:
                                    try:
                                        int(data[nameloc-4])
                                        rank = int(data[nameloc-4:nameloc-1])
                                    except ValueError:
                                        rank = int(data[nameloc-3:nameloc-1])
                                    ratingtuple = (team, rank)
                                    ratingtuplelist.append(ratingtuple)
                            if len(ratingtuplelist) == 1:
                                teamratings.append(ratingtuplelist[0])
                            elif len(ratingtuplelist) == 2:
                                if ratingtuplelist[0] == ratingtuplelist[1]:
                                    teamratings.append(ratingtuplelist[0])
                                else:
                                    teamratings.append(ratingtuplelist[0])
                                    teamratings.append(ratingtuplelist[1])
                            elif len(ratingtuplelist) > 2:
                                for every in ratingtuplelist:
                                    teamratings.append(every)
                        if len(teamratings) > 0:
                            if week == '15' and season == '13':
                                usedate = '2013-05-14'
                            for team in teamratings:
                                    bassetinsert.append("('"+team[0]+"', '"+str(usedate)+"', "+str(team[1])+")")
                            bassetinsertx = ','.join(bassetinsert)
                            bassetlist = ['INSERT INTO bassetratings VALUES', bassetinsertx, ';']
                            initialbassetinsert = ' '.join(bassetlist)  
                            add_basset = initialbassetinsert  
                            print usedate
                            cursor.execute('SET foreign_key_checks = 0;')
                            cursor.execute(add_basset)
                            cnx.commit()
                            cursor.execute('SET foreign_key_checks = 1;')
    cursor.close()
    cnx.close()        
