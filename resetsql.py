# -*- coding: utf-8 -*-
"""
Created on Fri Oct 06 14:12:39 2017

@author: Eric
"""

def resetsql(passcode):
    import mysql.connector   
    cnx = mysql.connector.connect(user='root', password=passcode,
                                  host='127.0.0.1',
                                  database='ncaa')    
    cursor = cnx.cursor() 
    
    teamnames = ['Air Force', 'Akron', 'Alabama', 'App State', 'Arizona', 'Arizona St', 'Arkansas', 'Arkansas St', 'Army', 'Auburn', 'BYU', 'Ball State', 'Baylor', 'Boise State', 'Boston Col', 'Bowling Grn', 'Buffalo', 'California', 'Central FL', 'Central Mich', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Car', 'Colorado', 'Colorado St', 'Connecticut', 'Duke', 'E Carolina', 'E Michigan', 'Fla Atlantic', 'Florida', 'Florida Intl', 'Florida St', 'Fresno St', 'GA Southern', 'GA Tech', 'Georgia', 'Georgia State', 'Hawaii', 'Houston', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Iowa State', 'Kansas', 'Kansas St', 'Kent State', 'Kentucky', 'LA Lafayette', 'LA Monroe', 'LA Tech', 'LSU', 'Louisville', 'Marshall', 'Maryland', 'Memphis', 'Miami (FL)', 'Miami (OH)', 'Michigan', 'Michigan St', 'Middle Tenn', 'Minnesota', 'Miss State', 'Mississippi', 'Missouri', 'N Carolina', 'N Illinois', 'N Mex State', 'NC State', 'Navy', 'Nebraska', 'Nevada', 'New Mexico', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio', 'Ohio State', 'Oklahoma', 'Oklahoma St', 'Old Dominion', 'Oregon', 'Oregon St', 'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'S Alabama', 'S Carolina', 'S Florida', 'S Methodist', 'S Mississippi', 'San Diego St', 'San Jose St', 'Stanford', 'Syracuse', 'TX Christian', 'TX El Paso', 'TX-San Ant', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy', 'Tulane', 'Tulsa', 'U Mass', 'UAB', 'UCLA', 'UNLV', 'USC', 'Utah', 'Utah State', 'VA Tech', 'Vanderbilt', 'Virginia', 'W Kentucky', 'W Michigan', 'W Virginia', 'Wake Forest', 'Wash State', 'Washington', 'Wisconsin', 'Wyoming']
    
    nameinsert = []
    for team in teamnames:
        nameinsert.append("('"+team+"')")
    nameinsertx = ','.join(nameinsert)
    insertlist = ['INSERT INTO teamnames VALUES', nameinsertx, ';']
    initialnameinsert = ' '.join(insertlist)  
    add_names = initialnameinsert 
    cursor.execute('call ncaa.sp_reset_tables();')  
    cursor.execute(add_names)
    cnx.commit()
    cursor.close()
    cnx.close()