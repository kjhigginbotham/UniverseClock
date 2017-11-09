# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 17:30:48 2017

@author: Adam
"""

import time

# Find and print base and start time
base = "Thu Nov 25 12:00:00 1915"
# base = "Sun Nov 5 12:00:00 2017"
start = time.asctime()

# print("Base time: {}".format(base))
# print("Starting time: {}".format(start))

# Dictionaries of months
monthDictBeg = {"Jan":0, "Feb":31, "Mar":59, "Apr":90, "May":120, "Jun":151, "Jul":181, "Aug":212, "Sep":243, "Oct":273, "Nov":304, "Dec":334}
monthDictEnd = {"Dec":31, "Nov":61, "Oct":92, "Sep":122, "Aug":153, "Jul":184, "Jun":214, "May":245, "Apr":275, "Mar":306, "Feb":334, "Jan":365}
monthList = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Split up times for analysis of seconds
base_time = base.split()
start_time = start.split()

baseYear = int(base_time[-1])
baseMonth = base_time[1]
baseDay = monthDictBeg[baseMonth] + int(base_time[2])
baseHour = int(base_time[3][0] + base_time[3][1])
baseMinute = int(base_time[3][3] + base_time[3][4])
baseSecond = int(base_time[3][6] + base_time[3][7])
baseTuple = (baseYear,baseDay,baseHour,baseMinute,baseSecond)


def leapTest(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def showMeTheMonthy(days):
    for i in range(len(monthList)):
        nextDays = monthDictBeg[monthList[i]]
        if nextDays > days:
            theMonth = monthList[i-1]
            newDate = days - monthDictBeg[theMonth]
            
            return [theMonth, newDate]

def addThatTrash(timeList):
    timeYears = timeList[0]
    timeDays = timeList[1]
    timeHours = timeList[2]
    timeMins = timeList[3]
    timeSecs = timeList[4]
    global baseTuple
    baseYear = baseTuple[0]
    baseDay = baseTuple[1]
    baseHour = baseTuple[2]
    baseMinute = baseTuple[3]
    baseSecond = baseTuple[4]
    
    newSecs = baseSecond + timeSecs
    if newSecs > 60:
        newSecs = newSecs - 60
        baseMinute = baseMinute + 1
    
    newMins = baseMinute + timeMins
    if newMins > 60:
        baseHour = baseHour + 1
        newMins = newMins - 60
    
    newHour = baseHour + timeHours
    if newHour > 24:
        baseDay = baseDay + 1
        newHour = newHour - 24
    
    newYear = baseYear
    while timeYears > 0:
        newYear = newYear + 1
        if newYear % 4 == 0:
            if newYear % 100 == 0:
                if newYear % 400 == 0:
                    baseDay = baseDay - 1
                else:
                    pass
            else:
                baseDay = baseDay - 1
        else:
            pass
        timeYears = timeYears - 1
            
    nextYear = newYear + 1
    thisLeap = leapTest(newYear)
    
    newDay = baseDay + timeDays
    if thisLeap:
        if newDay > 60:
            newDay = newDay + 1
            
        if newDay > 366:
            newDay = newDay - 366
            newYear = nextYear
    else:
        if newDay > 365:
            newDay = newDay - 365
            newYear = nextYear
    
    thisLeap = leapTest(newYear)
    if thisLeap:
        for i in range(len(monthList)):
            if i > 1:
                monthDictBeg[monthList[i]] = monthDictBeg[monthList[i]] + 1
    
    montharoony = showMeTheMonthy(newDay)
    
    newMonth = montharoony[0]
    theDay = montharoony[1]
    
    dateStr = "{} {} {}:{}:{} {}".format(newMonth,theDay,newHour,newMins,newSecs,newYear)
    
    return dateStr


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        