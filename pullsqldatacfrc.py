#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 15:12:52 2017

@author: eric.hensleyibm.com
"""


def pullsqldatacfrc():
    import mysql.connector   
    import pandas as pd
    
    cnx = mysql.connector.connect(user='root', password='ibm1234',
                                  host='127.0.0.1',
                                  database='ncaa')    
    cursor = cnx.cursor() 
    
    query = 'SELECT \
        oddsdate,\
        favorite,\
        underdog,\
        favscore,\
        dogscore,\
        line,\
        homeaway,\
        (SELECT \
                (bassetrank)\
            FROM\
                bassetratings AS bt1\
            WHERE\
                bt1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(bt1.bassetdate, INTERVAL 4 DAY) AND DATE_ADD(bt1.bassetdate, INTERVAL 1 DAY)) AS `fav Basset rank`,\
        (SELECT \
                (bassetrank)\
            FROM\
                bassetratings AS bt2\
            WHERE\
                bt2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(bt2.bassetdate, INTERVAL 4 DAY) AND DATE_ADD(bt2.bassetdate, INTERVAL 1 DAY)) AS `dog Basset rank`,\
        (SELECT \
                (cfrcrank)\
            FROM\
                cfrcratings AS cfrc1\
            WHERE\
                cfrc1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(cfrc1.cfrcdate, INTERVAL 5 DAY) AND DATE_ADD(cfrc1.cfrcdate, INTERVAL 1 DAY)) AS `fav CFRC rank`,\
        (SELECT \
                (cfrcrank)\
            FROM\
                cfrcratings AS cfrc2\
            WHERE\
                cfrc2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(cfrc2.cfrcdate, INTERVAL 5 DAY) AND DATE_ADD(cfrc2.cfrcdate, INTERVAL 1 DAY)) AS `dog CFRC rank`,\
        (SELECT \
                (`predictive-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite predictive by others`,\
        (SELECT \
                (`predictive-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog predictive by others`,\
        (SELECT \
                (`home-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite home by others`,\
        (SELECT \
                (`home-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog home by others`,\
        (SELECT \
                (`away-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite away by others`,\
        (SELECT \
                (`away-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog away by others`,\
        (SELECT \
                (`neutral-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite neutral by others`,\
        (SELECT \
                (`neutral-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog neutral by others`,\
        (SELECT \
                (`home-adv-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite home adv by others`,\
        (SELECT \
                (`home-adv-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog home adv by others`,\
        (SELECT \
                (`schedule-strength-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite schedule strength by others`,\
        (SELECT \
                (`schedule-strength-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog schedule strength by others`,\
        (SELECT \
                (`future-sos-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite future sos by others`,\
        (SELECT \
                (`future-sos-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog future sos by others`,\
        (SELECT \
                (`season-sos-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite season sos by others`,\
        (SELECT \
                (`season-sos-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog season sos by others`,\
        (SELECT \
                (`sos-basic-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite basic sos by others`,\
        (SELECT \
                (`sos-basic-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog basic sos by others`,\
        (SELECT \
                (`in-conference-sos-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite in conference sos by others`,\
        (SELECT \
                (`in-conference-sos-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog in conference sos by others`,\
        (SELECT \
                (`non-conference-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite non conference sos by others`,\
        (SELECT \
                (`non-conference-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog non conference by others`,\
        (SELECT \
                (`last-5-games-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite last 5 games by others`,\
        (SELECT \
                (`last-5-games-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog last 5 games by others`,\
        (SELECT \
                (`last-10-games-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite last 10 games by others`,\
        (SELECT \
                (`last-10-games-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog last 10 games by others`,\
        (SELECT \
                (`in-conference-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite in conference by others`,\
        (SELECT \
                (`in-conference-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog in conference by others`,\
        (SELECT \
                (`non-conference-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite non conference by others`,\
        (SELECT \
                (`non-conference-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog non conference by others`,\
        (SELECT \
                (`luck-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite luck by others`,\
        (SELECT \
                (`luck-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog luck by others`,\
        (SELECT \
                (`consistency-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite consistency by others`,\
        (SELECT \
                (`consistency-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog consistency by others`,\
        (SELECT \
                (`vs-1-10-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite vs 1-10 by others`,\
        (SELECT \
                (`vs-1-10-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog vs 1-10 by others`,\
        (SELECT \
                (`vs-11-25-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite vs 11-25 by others`,\
        (SELECT \
                (`vs-11-25-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog vs 11-25 by others`,\
        (SELECT \
                (`vs-26-40-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite vs 26-40 by others`,\
        (SELECT \
                (`vs-26-40-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog vs 26-40 by others`,\
        (SELECT \
                (`vs-41-75-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite vs 41-75 by others`,\
        (SELECT \
                (`vs-41-75-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog vs 41-75 by others`,\
        (SELECT \
                (`vs-76-120-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite vs 76-120 by others`,\
        (SELECT \
                (`vs-76-120-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog vs 76-120 by others`,\
        (SELECT \
                (`first-half-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite first half by others`,\
        (SELECT \
                (`first-half-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog first half by others`,\
        (SELECT \
                (`second-half-by-other`)\
            FROM\
                baseratings AS br1\
            WHERE\
                br1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN br1.basedate AND DATE_ADD(br1.basedate, INTERVAL 6 DAY)) AS `favorite second half by others`,\
        (SELECT \
                (`second-half-by-other`)\
            FROM\
                baseratings AS br2\
            WHERE\
                br2.teamname = od.underdog\
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog second half by others`\
    FROM\
        oddsdata AS od'
        
        
    cursor.execute(query)
    x = pd.DataFrame(cursor.fetchall())
    return x