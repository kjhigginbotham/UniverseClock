"""
Created on Wed Nov 9 22:30:00 2017

@author: Kenny Higginbotham, Adam Kull
"""

monthDictBeg = {"Jan":0, "Feb":31, "Mar":59, "Apr":90, "May":120, "Jun":151, "Jul":181, "Aug":212, "Sep":243, "Oct":273, "Nov":304, "Dec":334}

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
	monthList = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	for i in range(len(monthList)):
		nextDays = monthDictBeg[monthList[i]]
		if nextDays > days:
			theMonth = monthList[i-1]
			newDate = days - monthDictBeg[theMonth]
			
			return [theMonth, newDate]
		
	return ["Dec",days - monthDictBeg["Dec"]]

def addThatTrash(timeList, base):

	monthDictBeg = {"Jan":0, "Feb":31, "Mar":59, "Apr":90, "May":120, "Jun":151, "Jul":181, "Aug":212, "Sep":243, "Oct":273, "Nov":304, "Dec":334}
	monthList = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

	# get elapsed times from input
	timeYears, timeDays, timeHours, timeMins, timeSecs = timeList

	# get base times
	baseTime = base.split()
	baseYear = int(baseTime[-1])
	baseMonth = baseTime[1]
	baseDay = monthDictBeg[baseMonth] + int(baseTime[2])
	baseHour = int(baseTime[3][0] + baseTime[3][1])
	baseMinute = int(baseTime[3][3] + baseTime[3][4])
	baseSecond = int(baseTime[3][6] + baseTime[3][7])

	# calculate new times (including rollover)
	newYears = baseYear + timeYears
	newDays = baseDay + timeDays
	newHours = baseHour + timeHours
	newMins = baseMinute + timeMins
	newSecs = baseSecond + timeSecs

	# check if year is a leap year and assign minusdays
	if leapTest(newYears):
		minusdays = 366
	else:
		minusdays = 365

	# shift rollover
	while newSecs >= 60:
		newMins += 1
		newSecs -= 60
	while newMins >= 60:
		newHours += 1
		newMins -= 60
	while newHours >= 24:
		newDays += 1
		newHours -= 24
	while newDays >= minusdays:
		newYears += 1
		newDays -= minusdays

	# check to see if last year is leap year; adjust monthDictBeg accordingly
	if leapTest(newYears) & newDays > 60:
		thisLeap = leapTest(newYears)
		if thisLeap:
			for i in range(len(monthList)):
				if i > 1:
					monthDictBeg[monthList[i]] = monthDictBeg[monthList[i]] + 1

	# find the new month
	montharoony = showMeTheMonthy(newDays)
	
	newMonth = montharoony[0]
	theDay = montharoony[1]

	# prevent day 0
	if theDay == 0:
		theDay = 1

	# add 0s to single digit times
	if len(str(newHours)) == 1:
		newHours = '0' + str(newHours)
	if len(str(newMins)) == 1:
		newMins = '0' + str(newMins)
	if len(str(newSecs)) == 1:
		newSecs = '0' + str(newSecs)
	
	# create and return new Calendar date
	dateStr = "{} {} {}:{}:{} {}".format(newMonth,theDay,newHours,newMins,newSecs,newYears)
		
	return dateStr