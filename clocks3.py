"""
Created on Fri Oct 13 08:17:00 2017

@author: Kenny Higginbotham, Adam Kull, and Talha Irfan Khawaja
"""

import time
import math


# important constants
c = 3.0*10**8
G = 6.67*10**(-11)

# masses and radii of test objects
earth_m = 5.972*10**24
earth_r = 6.371*10**6
sun_m = 1.989*10**30
sun_r = 695.7*10**6
GW150914_m = 62.0*sun_m
GW150914_r = 199.0*10**3
garg_m = 100.0*10**6*sun_m
garg_r = 300.0*10**9

# tau ratio function
def taurat(m,r):
    return math.sqrt((1-(2*G*m)/(r*c**2))/(1-(2*G*earth_m)/(earth_r*c**2)))

# Find and print base and start time
base = "Fri Nov 25 12:00:00 1915"
start = time.asctime()

print("Base time: {}".format(base))
print("Starting time: {}".format(start))

# Dictionaries of months
monthDictBeg = {"Jan":0, "Feb":31, "Mar":59, "Apr":90, "May":120, "Jun":151, "Jul":181, "Aug":212, "Sep":243, "Oct":273, "Nov":304, "Dec":334}
monthDictEnd = {"Dec":31, "Nov":61, "Oct":92, "Sep":122, "Aug":153, "Jul":184, "Jun":214, "May":245, "Apr":275, "Mar":306, "Feb":334, "Jan":365}

# Split up times for analysis of seconds
base_time = base.split()
start_time = start.split()

elap_E = 0

# Take base_time and get the rest of the seconds left in the year
# First get seconds
base_secs = 60 - int(base_time[3][6] + base_time[3][7])
elap_E = elap_E + base_secs

# Next get minutes
base_minutes = 59 - int(base_time[3][3] + base_time[3][4])
elap_E = elap_E + (base_minutes * 60)

# Next hours
base_hours = 23 - int(base_time[3][0] + base_time[3][1])
elap_E = elap_E + (base_hours * 3600)

# Lastly days
base_days = monthDictEnd[base_time[1]] - int(base_time[2])
elap_E = elap_E + (base_days * 86400)

# Store number of seconds left in the year for later
secs_left = elap_E

# Get the base year offset by one year to prevent double counting
base_year = int(base_time[4]) + 1

# Repeat for start year in the opposite direction
# Start with seconds
start_secs = int(start_time[3][6] + start_time[3][7])
elap_E = elap_E + start_secs

# Next minutes
start_minutes = int(start_time[3][3] + start_time[3][4])
elap_E = elap_E + (start_minutes * 60)

# Next hours
start_hours = int(start_time[3][0] + start_time[3][1])
elap_E = elap_E + (start_hours * 3600)

# Next, days
start_days = monthDictBeg[start_time[1]] + int(start_time[2]) - 1
elap_E = elap_E + (start_days * 86400)

# Get the start year offset by one year to prevent double counting
start_year = int(start_time[4])

# Calculate the total number of seconds in the intervening year
while base_year < start_year:
    if base_year % 4 == 0:
        if base_year % 100 == 0:
            if base_year % 400 == 0:
                elap_E = elap_E + (366 * 86400)
                
            else:
                elap_E = elap_E + (365 * 86400)
        
        else:
            elap_E = elap_E + (366 * 86400)
    
    else:
        elap_E = elap_E + (365 * 86400)
        
    base_year = base_year + 1

tauS_E = taurat(sun_m,sun_r)
tauBH_E = taurat(GW150914_m,GW150914_r)
tauGar_E = taurat(garg_m,garg_r)

# time elapsed since base date, seconds on Earth
elap_S = tauS_E*elap_E
elap_BH = tauBH_E*elap_E
elap_Gar = tauGar_E*elap_E

# print elapsed times
print('Time elapsed on the surface of...')
print('Earth: {} sec'.format(elap_E))
print('Sun: {} sec'.format(elap_S))
print('GW150914: {} sec'.format(elap_BH))
print('Gargantua: {} sec'.format(elap_Gar))

# Round seconds down to nearest second
elap_S = int(elap_S)
elap_BH = int(elap_BH)
elap_Gar = int(elap_Gar)

# Grab values from base year for reformulation of date
baseMonth = base_time[1]
baseDay = int(base_time[2])
baseYear = int(base_time[4])
temp_time = base_time[3].split(":")
baseHour = int(temp_time[0])
baseMinute = int(temp_time[1])
baseSecond = int(temp_time[2])
'''
# Calculate new date function
def newDate(secs):
    yearsPassed = int(secs / 31536000)
    secs = (secs / 31536000) - yearsPassed
    days = (secs * 365)
    
    loopYear = baseYear
    newYear = baseYear + yearsPassed
    
    while loopYear < newYear:
        if baseYear % 4 == 0:
            if baseYear % 100 == 0:
                if baseYear % 400 == 0:
                    days = days - 1
                    
            else:
                days = days - 1
    
        loopYear = loopYear + 1
    
    monthDays = [["Jan",31],["Feb",28],["Mar",31],["Apr",30],["May",31],["Jun",30],["Jul",31],["Aug",31],["Sep",30],["Oct",31],["Nov",30],["Dec",31],["Jan",31],["Feb",28],["Mar",31],["Apr",30],["May",31],["Jun",30],["Jul",31],["Aug",31],["Sep",30],["Oct",31],["Nov",30]]
    month = []
    for i in range(len(monthDays)):
        if monthDays[i][0] == baseMonth:
            month.append(i)
            
    monthIndex = month[0]
    
    dayCount = 0
    while dayCount < (days-28):
        dayCount = dayCount + monthDays[monthIndex][1]
        
        monthIndex = monthIndex + 1
        
    newMonth = monthDays[monthIndex][0]
    if monthIndex > 11:
        newYear = newYear + 1

    extraDays = days - dayCount
    newDay = int(baseDay + extraDays) 
    
    bonusTime = (baseDay + extraDays) - newDay
    
    extraHours = bonusTime * 24
    newHour = baseHour + int(extraHours)
    
    bonusTime = extraHours - int(extraHours)
    newMinute = baseMinute + int(bonusTime * 60)
    
    bonusTime = (bonusTime * 60) - int(bonusTime * 60)
    newSecond = baseSecond + int(bonusTime * 60)
    
    if newSecond > 60:
        newSecond = newSecond - 60
        newMinute = newMinute + 1
    if newMinute > 60:
        newMinute = newMinute - 60
        newHour = newHour + 1
    if newHour > 24:
        newHour = newHour - 24
        newDay = newDay + 1
    if newDay > monthDays[monthIndex][1]:
        newDay = newDay - monthDays[monthIndex][1]
        monthIndex = monthIndex + 1
        newMonth = monthDays[monthIndex][0]
    if monthIndex > 10:
        newYear = newYear + 1
    
    newDay = str(newDay)
    newHour = str(newHour)
    newMinute = str(newMinute)
    newSecond = str(newSecond)
    
    if len(newDay) == 1:
        newDay = "0" + newDay
    if len(newHour) == 1:
        newHour = "0" + newHour
    if len(newMinute) == 1:
        newMinute = "0" + newMinute
    if len(newSecond) == 1:
        newSecond = "0" + newSecond
    
    dateStr = "{0} {1} {2}:{3}:{4} {5}".format(newMonth,newDay,newHour,newMinute,newSecond,newYear)
    
    return dateStr'''

def newDate2(secs):
    yearsPassed = int(secs / 31536000)
    extra = secs % 31536000
    daysPast = int(extra / 86400)
    extra = extra % 86400
    hoursPast = int(extra / 3600)
    extra = extra % 3600
    minutesPast = int(extra / 60)
    secondsPast = extra % 60
    
    newSecond = baseSecond + secondsPast
    while newSecond > 60:
        newSecond = newSecond - 60
        minutesPast = minutesPast + 1
    
    newMinute = baseMinute + minutesPast
    while newMinute > 60:
        newMinute = newMinute - 60
        hoursPast = hoursPast + 1
    
    newHour = baseHour + hoursPast
    while newHour > 23:
        newHour = newHour - 24
        daysPast = daysPast + 1
        
    baseTOY = monthDictBeg[baseMonth] + baseDay
    newTOY = baseTOY + daysPast
    while newTOY > 365:
        newTOY = newTOY - 365
        yearsPassed = yearsPassed + 1
    monthList = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    #daysInMonth = {"Jan":31,"Feb",28,"Mar":31,"Apr":30,"May":31,"Jun":30,"Jul":31,"Aug":31,"Sep":30,"Oct":31,"Nov":30,"Dec":31}
    for i in range(len(monthList)):
        thisMonth = monthList[i]
        if i > 0:
            lastMonth = monthList[i-1]
        if i == 0:
            lastMonth = "Jan"
        
        if monthDictBeg[thisMonth] < newTOY:
            pass
        elif monthDictBeg[thisMonth] > newTOY and monthDictBeg[lastMonth] < newTOY:
            newDay = newTOY - monthDictBeg[lastMonth]
        '''else:
            #newMonth =  thisMonth
            newDay = newTOY - monthDictBeg[thisMonth]'''
    
    newYear = baseYear + yearsPassed
    if newDay < 10:
        newDay = "0" + str(newDay)
    if newHour < 10:
        newHour = "0" + str(newHour)
    if newMinute < 10:
        newMinute = "0" + str(newMinute)
    if newSecond < 10:
        newSecond = "0" + str(newSecond)
    dateStr = "{0} {1} {2}:{3}:{4} {5}".format(thisMonth,newDay,newHour,newMinute,newSecond,newYear)
    
    return dateStr

def newDate3(secs):
    newDay = monthDictBeg[baseMonth] + baseDay
    newSecond = baseSecond
    newMinute = baseMinute
    newHour = baseHour
    newYear = baseYear
    
    while secs > 0:
        newSecond = newSecond + 1
        if newSecond > 60:
            newSecond = newSecond - 60
            newMinute = newMinute + 1
            if newMinute > 60:
                newMinute = newMinute - 60
                newHour = newHour + 1
                if newHour > 23:
                    newHour = newHour - 24
                    newDay = newDay + 1
                    if newDay > 365:
                        newDay = newDay - 365
                        newYear = newYear + 1
        secs = secs - 1
    
    monthList = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for i in range(len(monthList)):
        thisMonth = monthList[i]
        if i > 0:
            lastMonth = monthList[i-1]
        if i == 0:
            lastMonth = "Jan"
        
        if monthDictBeg[thisMonth] < newDay:
            pass
        elif monthDictBeg[thisMonth] > newDay and monthDictBeg[lastMonth] < newDay:
            newDay = newDay - monthDictBeg[lastMonth]

    if newDay < 10:
        newDay = "0" + str(newDay)
    if newHour < 10:
        newHour = "0" + str(newHour)
    if newMinute < 10:
        newMinute = "0" + str(newMinute)
    if newSecond < 10:
        newSecond = "0" + str(newSecond)
    dateStr = "{0} {1} {2}:{3}:{4} {5}".format(thisMonth,newDay,newHour,newMinute,newSecond,newYear)
    
    return dateStr

doublecheck = newDate3(elap_E)
date_S = newDate3(elap_S)
date_EH = newDate3(elap_BH)
date_Gar = newDate3(elap_Gar)

print(doublecheck)
print("Original Date: {}".format(base))
print("Date on Earth: {}".format(start))
print("Date on the Sun: {}".format(date_S))
print("Date on GW150914: {}".format(date_EH))
print("Date on Gargantua: {}".format(date_Gar))











