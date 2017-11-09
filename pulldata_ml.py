#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 21:51:10 2017

@author: eric.hensleyibm.com
"""


def pulldata_ml():
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
        favmoneyline,\
        dogmoneyline,\
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
                    AND od.oddsdate BETWEEN br2.basedate AND DATE_ADD(br2.basedate, INTERVAL 6 DAY)) AS `dog season sos by others`, \
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
        (SELECT\
                (LAZ)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav LAZ`,\
        (SELECT \
                (LAZ)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog LAZ`,\
        (SELECT \
                (ARG)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav ARG`,\
        (SELECT \
                (ARG)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog ARG`,\
        (SELECT \
                (MAS)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav MAS`,\
        (SELECT \
                (MAS)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog MAS`,\
        (SELECT \
                (SAG)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav SAG`,\
        (SELECT \
                (SAG)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog SAG`,\
        (SELECT \
                (HOW)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav HOW`,\
        (SELECT \
                (HOW)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog HOW`,\
        (SELECT \
                (BIL)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav BIL`,\
        (SELECT \
                (BIL)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog BIL`,\
        (SELECT \
                (MAR)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav MAR`,\
        (SELECT \
                (MAR)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog MAR`,\
        (SELECT \
                (DOK)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav DOK`,\
        (SELECT \
                (DOK)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog DOK`,\
        (SELECT \
                (DES)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav DES`,\
        (SELECT \
                (DES)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog DES`,\
        (SELECT \
                (MOR)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav MOR`,\
        (SELECT \
                (MOR)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog MOR`,\
        (SELECT \
                (BRN)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav BRN`,\
        (SELECT \
                (BRN)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog BRN`,\
        (SELECT \
                (PIG)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav PIG`,\
        (SELECT \
                (PIG)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog PIG`,\
        (SELECT \
                (CGV)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav CGV`,\
        (SELECT \
                (CGV)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog CGV`,\
        (SELECT \
                (BDF)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.favorite\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `fav BDF`,\
        (SELECT \
                (BDF)\
            FROM\
                masseyratings AS m1\
            WHERE\
                m1.teamname = od.underdog\
                    AND od.oddsdate BETWEEN DATE_SUB(m1.masseydate, INTERVAL 5 DAY) AND m1.masseydate) AS `dog BDF`\
    FROM\
        oddsdata AS od\
        where year(oddsdate) < "2017"\
        order by oddsdate asc;'
        
    cursor.execute(query)
    x = pd.DataFrame(cursor.fetchall())
    return x