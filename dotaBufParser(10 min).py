#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Андрей
#
# Created:     03.05.2018
# Copyright:   (c) Андрей 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
import requests
import time
import datetime
import json
import ssl
import re


def getMeetsLinks(tournamentLink,pages):
    payload = {
        "Host": "ru.dotabuff.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests":"1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
        "Referer": "https://ru.dotabuff.com/esports/leagues/9643-dota-2-asia-championships-2018/series?date=all&best_of=bo2_or_more&series_status=completed",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    links = []
    for page in range(1,pages+1):
        r = requests.get('https://ru.dotabuff.com'+tournamentLink+'?best_of=bo2_or_more&date=all&original_slug=9643-dota-2-asia-championships-2018&page='+str(page)+'&series_status=completed',verify=False, headers = payload)
        i1 = r.text.find('table table-striped recent-esports-matches series-table')
        meets = r.text[i1:len(r.text)]
        i1 = meets.find("<tbody>")
        i2 = meets.find("</tbody>")
        meets = meets[i1:i2]
        i = 0
        n = len(meets)
        i1 = 0;
        i2 = 0;
        cnt = 0;
        while(i < n):
            i1 = meets.find('<tr>',i)
            if(i1 != -1):
                i2 = meets.find('</tr>',i1+1)
                i = i2 + 1
                cnt = cnt + 1
                line = meets[i1:i2]
                i1 = line.find('href="')
                i2 = line.find('">')
                links.append(line[i1+6:i2])

            else:
                i = n + 1
    return links

def getMatchesLinks(meetLink):
    payload = {
            "Host": "ru.dotabuff.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests":"1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
            "Referer": "https://ru.dotabuff.com/esports/leagues/9643-dota-2-asia-championships-2018/series?date=all&best_of=bo2_or_more&series_status=completed",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    r = requests.get('https://ru.dotabuff.com'+meetLink,verify=False, headers = payload)
    n =len(r.text)
    i = 0
    links = []
    while (i < n):
        i1 = r.text.find('match-link',i)
        if(i1 != -1):
            i2 = r.text.find('<a href="',i1+1)
            i3 = r.text.find('">',i2+1)
            i = i1 + 1
            links.append(r.text[i2 + 9:i3])
        else:
            i = n + 1
    return links

def getMiderName(table):
    i = 0
    n = len(table)
    cnt = 0
    midHero = ''

    while (i < n):
        i1 = table.find('<tr',i)
        if(i1 != -1):
            i2 = table.find('</tr>',i1 + 1)
            i = i2 + 1
            row = table[i1:i2]
            role = row.find('Ключевая роль')
            line = row.find('Центр')
            cnt = cnt + 1
            if(role != -1 and line != -1):
                i1 = row.find('<a href="/heroes/')
                i2 = row.find('">',i1 + 1)
                midHero = row[i1+17:i2]
                i = n + 1
        else:
            i = n + 1
    return midHero

def getMatchData(matchLink):
    payload = {
                "Host": "ru.dotabuff.com",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests":"1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
                "Referer": "https://ru.dotabuff.com/esports/leagues/9643-dota-2-asia-championships-2018/series?date=all&best_of=bo2_or_more&series_status=completed",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            }

    r = requests.get('https://ru.dotabuff.com'+matchLink,verify=False, headers = payload)
    i1 = r.text.find('<tbody>')
    i2 = r.text.find('</tbody>')
    radiance = r.text[i1:i2];
    radianceMid = getMiderName(radiance)

    i1 = r.text.find('<tbody>',i2+1)
    i2 = r.text.find('</tbody>',i1 + 1)
    dire = r.text[i1:i2];
    direMid = getMiderName(dire)

    team = ''
    f1 = r.text.find('match-result team dire')
    f2 = r.text.find('match-result team radiant')
    if(f1 != -1 and f2 == -1):
        team = 'Тьма'
    elif(f1 == -1 and f2 != -1):
        team = 'Свет'

    result = [radianceMid,direMid,team]
    return result

def getLogData(matchLink,radianceMid,direMid):
    payload = {
                "Host": "ru.dotabuff.com",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests":"1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
                "Referer": "https://ru.dotabuff.com/esports/leagues/9643-dota-2-asia-championships-2018/series?date=all&best_of=bo2_or_more&series_status=completed",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            }

    r = requests.get('https://ru.dotabuff.com'+matchLink+'/kills',verify=False, headers = payload)

    i1 = r.text.find('<div class="match-log')
    i2 = r.text.find('</article>',i1 + 1)
    log = r.text[i1:i2]
    i = 0
    n = len(log)
    cnt = 0

    rk = 0
    ra = 0
    rd = 0

    dk = 0
    da = 0
    dd = 0
    while (i < n):
        i1 = log.find('<span class="time">',i)
        if(i1 != -1):
            i2 = log.find('</span>',i1 + 1)
            time = log[i1+19:i2]
            minutes = float(time[0:2])
            if(minutes < 11):
                cnt = cnt + 1
                j1 = log.find('<div class="event">',i1)
                j2 = log.find('</div>',j1)
                row = log[j1:j2]

                j1 = row.find('href="/heroes/')
                j2 = row.find('">',j1)
                hero = row[j1+14:j2]
                mult = row.find('сделал')
                kill = row.find('убил')
                die =  row.find('погиб')
                sup =  row.find('с помощью')
                if(mult == -1):
                    if(hero == radianceMid):
                       print(hero)
                       rd = rd + 1
                       df = row.find(direMid,j2 + 1)
                       if(df != -1):
                        if(sup == -1):
                            dk = dk + 1
                        elif(df > sup):
                            da = da + 1
                        else:
                            dk = dk + 1
                    elif(hero == direMid):
                        print(hero)
                        dd = dd + 1
                        rf = row.find(radianceMid,j2 + 1)
                        if(rf != -1):
                            if(sup == -1):
                                rk = rk + 1
                            elif(rf > sup):
                                ra = ra + 1
                            else:
                                rk = rk + 1
                    else:

                        rf = row.find(radianceMid,j2 + 1)
                        df = row.find(direMid,j2 + 1)
                        if(rf != -1):
                            print(hero)
                            if(sup == -1):
                                rk = rk + 1
                            elif(rf > sup):
                                ra = ra + 1
                            else:
                                rk = rk + 1
                        elif(df != -1):
                            print(hero)
                            if(sup == -1):
                                dk = dk + 1
                            elif(df > sup):
                                da = da + 1
                            else:
                                dk = dk + 1

                i = i2 + 1
            else:
                i = n + 1

        else:
            i = n + 1
    return [rk,ra,rd,dk,da,dd]


##matchLink = '/matches/3903099199'
##rez = getMatchData(matchLink)
##logData = getLogData(matchLink,rez[0],rez[1])
##matchData = rez[0]+';'+rez[1]+';'+rez[2]+';'+logData[0]+';'+logData[1]+';'+logData[2]+';'+logData[3]+';'+logData[4]+';'+logData[5]

meets = getMeetsLinks('/esports/leagues/9643-dota-2-asia-championships-2018/series',6)
links = []
lines = []
for i in range(0,len(meets)):
    matches = getMatchesLinks(meets[i])
    print('#############'+str(i) + '###############\n')
    for j in range(0,len(matches)):
        matchLink = matches[j]
        rez = getMatchData(matchLink)
        logData = getLogData(matchLink,rez[0],rez[1])
        matchData = rez[0]+';'+rez[1]+';'+rez[2]+';'+str(logData[0])+';'+str(logData[1])+';'+str(logData[2])+';'+str(logData[3])+';'+str(logData[4])+';'+str(logData[5])
        line = meets[i] + ';' + matches[j] + ';' + matchData + '\n'
        lines.append(line)

with open("D:\projects\python\Dac.csv",'w') as f:
    f.writelines(lines)






