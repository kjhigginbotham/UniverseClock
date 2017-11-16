"""
Created on Wed Nov 9 22:01:00 2017

@author: Kenny Higginbotham, Adam Kull
"""

import argparse
import time
import math
import newConvert

# important constants
c = 3.0*10**8
G = 6.67*10**(-11)
NLyear_sec = 31536000
Lyear_sec = 31622400
day_sec = 86400
hour_sec = 3600
min_sec = 60

# masses and radii of test objects
earth_m = 5.972*10**24
earth_r = 6.371*10**6
sun_m = 1.989*10**30
sun_r = 695.7*10**6
psr_m = 1.4*sun_m
psr_r = 10*1.4*10**(-6)*sun_r
GW150914_m = 62.0*sun_m
GW150914_r = 199.0*10**3
garg_m = 100.0*10**6*sun_m
garg_r = 300.0*10**9
ngc1277_m = 1.7*10**10*sun_m
ngc1277_r = 5.011839*10**13

# tau ratio function
def taurat(m,r):
    return math.sqrt((1-(2*G*m)/(r*c**2))/(1-(2*G*earth_m)/(earth_r*c**2)))

# take input for base time
parser = argparse.ArgumentParser()
parser.add_argument("input_date", help='Input date to start clocks from. Format example: "Thu Nov 25 12:00:00 1915"', type=str)
parser.add_argument("runtime", help='Duration of clocks in seconds', type=str)
args = parser.parse_args()

# Find and print base and start time
base = args.input_date
start = time.asctime()

print('\n')
print("Base time: {}".format(base))
print("Starting time: {}".format(start))
print('\n')

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

# if current year
if base_year - 1 == start_year:
    if base_year % 4 == 0:
        if base_year % 100 == 0:
            if base_year % 400 == 0:
                elap_E -= Lyear_sec
            else:
                elap_E -= NLyear_sec
        else:
            elap_E -= Lyear_sec
    else:
        elap_E -= NLyear_sec

# Calculate the total number of seconds in the intervening year
leap_years = 0
orig_year = base_year - 1 # preserve variable for base year
while base_year < start_year:
    if base_year % 4 == 0:
        leap_years += 1
        if base_year % 100 == 0:
            leap_years -= 1
            if base_year % 400 == 0:
                leap_years += 1
                elap_E = elap_E + (366 * 86400)
                
            else:
                elap_E = elap_E + (365 * 86400)
        
        else:
            elap_E = elap_E + (366 * 86400)
    
    else:
        elap_E = elap_E + (365 * 86400)
        
    base_year = base_year + 1

tauS_E = taurat(sun_m,sun_r)
tauPSR_E = taurat(psr_m,psr_r)
tauBH_E = taurat(GW150914_m,GW150914_r)
tauGar_E = taurat(garg_m,garg_r)
tauNGC_E = taurat(ngc1277_m,ngc1277_r)

# time elapsed since base date, seconds on Earth
elap_S = tauS_E*elap_E
elap_PSR = tauPSR_E*elap_E
elap_BH = tauBH_E*elap_E
elap_Gar = tauGar_E*elap_E
elap_NGC = tauNGC_E*elap_E

# print elapsed times
print('Time elapsed on the surface of...')
print('Earth: {} sec'.format(elap_E))
print('Sun: {} sec'.format(elap_S))
print('PSR B1919+21: {} sec'.format(elap_PSR))
print('GW150914: {} sec'.format(elap_BH))
print('Gargantua: {} sec'.format(elap_Gar))
print('NGC 1277: {} sec'.format(elap_NGC))

# floor seconds
elap_E = int(elap_E)

# decimal function
def dec(num1, num2):
    return float(num1/num2) - int(num1/num2)

# function to convert elapsed seconds to elapsed years, days, etc
def calendar(seconds):
    year = ((seconds-leap_years*Lyear_sec)/NLyear_sec)+leap_years
    # dec_dayPerYear = dec(year, 1)/year
    # dec_day = dec_dayPerYear*(leap_years*Lyear_sec+(year-leap_years)*NLyear_sec)
    # day = dec_day/day_sec
    if newConvert.leapTest(start_year):
        dec_day = dec(year, 1)*Lyear_sec
        day = dec_day/day_sec
    else:
        dec_day = dec(year, 1)*NLyear_sec
        day = dec_day/day_sec
    dec_hour = dec(dec_day, day_sec)*day_sec
    hour = dec_hour/hour_sec
    dec_min = dec(dec_hour, hour_sec)*hour_sec
    minutes = dec_min/min_sec
    sec = dec(dec_min, min_sec)*min_sec
    return [int(year), int(day), int(hour), int(minutes), int(sec)]

# calculate calendar time passed one earth
Etime_list = calendar(elap_E)

# function for day correction
def daycorec(result, begin, end):
    begmon = begin[1]
    begday = begin[2]
    
    endmon = end[1]
    endday = end[2]

    begmonpos = monthList.index(begmon)
    endmonpos = monthList.index(endmon)

    if (begmonpos == endmonpos) & (int(begday) > int(endday)):
        corday = result[1] + 1
    elif begmonpos > endmonpos:
        corday = result[1] + 1
    else:
        corday = result[1]

    corDateStr = [result[0],corday,result[2],result[3],result[4]]
    return corDateStr

corEtime_list = daycorec(Etime_list, base_time, start_time)

# calculate elapsed years, days, hours, minutes, seconds on other locations (including decimals)
Sdec_list = [tauS_E*i for i in corEtime_list]
PSRdec_list = [tauPSR_E*i for i in corEtime_list]
BHdec_list = [tauBH_E*i for i in corEtime_list]
Gardec_list = [tauGar_E*i for i in corEtime_list]
NGCdec_list = [tauNGC_E*i for i in corEtime_list]

# function for calculating the number of leap years
def leaps(numyears):
    ind = orig_year
    year_list = []
    while ind <= numyears + orig_year:
        year_list.append(ind)
        ind += 1
    these_years = len(year_list)*[0]
    j = 0
    for i in year_list:
        if base_year % 4 == 0:
            these_years[j] = 1
            if base_year % 100 == 0:
                these_years[j] = 0
                if base_year % 400 == 0:
                    these_years[j] = 1
        j += 1
    if len(these_years) > 1:
        if these_years[-2] == 1:
            isPrevLeap = True
        elif these_years[-2] == 0:
            isPrevLeap = False
    elif len(these_years) == 1:
        if these_years[0] == 1:
            isPrevLeap = True
        elif these_years[0] == 0:
            isPrevLeap = False
    return sum(these_years), isPrevLeap

# function for pushing back decimals in converted times
def decpush(intime):
    inyear, inday, inhour, inmin, insec = intime
    year = int(inyear)
    numLeap, thisPrevLeap = leaps(year)
    if year != 0:
        dec_dayPerYear = dec(inyear,1)/year
        dec_day = dec_dayPerYear*(numLeap*Lyear_sec+(year-numLeap)*NLyear_sec)
    else:
        if thisPrevLeap:
            dec_day = inyear*Lyear_sec
        else:
            dec_day = inyear*NLyear_sec
    newday = inday + dec_day/day_sec
    day = int(newday)
    dec_hour = dec(newday, 1)*day_sec
    newhour = inhour + dec_hour/hour_sec
    hour = int(newhour)
    dec_min = dec(newhour, 1)*hour_sec
    newmin = inmin + dec_min/min_sec
    minutes = int(newmin)
    dec_sec = dec(newmin, 1)*min_sec
    newsec = insec + dec_sec
    sec = int(newsec)
    if 'thisPrevLeap' in locals():
        if thisPrevLeap:
            minusdays = 366
        else:
            minusdays = 365
    else:
        minusdays = 100000
    while sec >= 60:
        minutes += 1
        sec -= 60
    while minutes >= 60:
        hour += 1
        minutes -= 60
    while hour >= 24:
        day += 1
        hour -= 24
    while day >= minusdays:
        year += 1
        day -= minusdays
    return [year, day, hour, minutes, sec]


# calculate elapsed times for other locations
Stime_list = decpush(Sdec_list)
PSRtime_list = decpush(PSRdec_list)
BHtime_list = decpush(BHdec_list)
Gartime_list = decpush(Gardec_list)
NGCtime_list = decpush(NGCdec_list)

# print total times past
print('\n')
print('Place\t Years\t Days\t Hours\t Min\t Sec')
print('Earth\t {}\t {}\t {}\t {}\t {}'.format(Etime_list[0], Etime_list[1], Etime_list[2], Etime_list[3], Etime_list[4]))
print('Sun\t {}\t {}\t {}\t {}\t {}'.format(Stime_list[0], Stime_list[1], Stime_list[2], Stime_list[3], Stime_list[4]))
print('PSR\t {}\t {}\t {}\t {}\t {}'.format(PSRtime_list[0], PSRtime_list[1], PSRtime_list[2], PSRtime_list[3], PSRtime_list[4]))
print('BH\t {}\t {}\t {}\t {}\t {}'.format(BHtime_list[0], BHtime_list[1], BHtime_list[2], BHtime_list[3], BHtime_list[4]))
print('Gar\t {}\t {}\t {}\t {}\t {}'.format(Gartime_list[0], Gartime_list[1], Gartime_list[2], Gartime_list[3], Gartime_list[4]))
print('NGC\t {}\t {}\t {}\t {}\t {}'.format(NGCtime_list[0], NGCtime_list[1], NGCtime_list[2], NGCtime_list[3], NGCtime_list[4]))

# convert time lists to calendar dates and times using convertBack.py
fin_Etime = newConvert.addThatTrash(corEtime_list, base)
fin_Stime = newConvert.addThatTrash(Stime_list, base)
fin_PSRtime = newConvert.addThatTrash(PSRtime_list, base)
fin_BHtime = newConvert.addThatTrash(BHtime_list, base)
fin_Gartime = newConvert.addThatTrash(Gartime_list, base)
fin_NGCtime = newConvert.addThatTrash(NGCtime_list, base)

# print final times
print('\n')
print('Earth:\t{}'.format(fin_Etime))
print('Sun:\t{}'.format(fin_Stime))
print('PSR:\t{}'.format(fin_PSRtime))
print('BH:\t{}'.format(fin_BHtime))
print('Gar: \t{}'.format(fin_Gartime))
print('NGC: \t{}'.format(fin_NGCtime))

# seperate clocks function
def sepClocks(intime):
    # get values from time string
    month, day, time, year = intime.split()
    clk_hr, clk_mn, clk_sc = time.split(':') 
    day, clk_hr, clk_mn, clk_sc, year = list(map(int,[day, clk_hr, clk_mn, clk_sc, year]))
    monthpos = monthList.index(month)

    sepList = [monthpos, day, clk_hr, clk_mn, clk_sc, year]
    return sepList

# run clocks function
def runClocks(sepList, taurat):
    # seperate out variables from list
    monthpos, day, clk_hr, clk_mn, clk_sc, year = sepList

    # list of number of days in each month
    dayInMon = [31, 28,  31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if newConvert.leapTest(year):
        dayInMon[1] = dayInMon[1] + 1

    # increase seconds by 1 and push over
    clk_sc += 1*taurat
    while clk_sc >= 60:
        clk_sc -= 60
        clk_mn += 1
    while clk_mn >= 60:
        clk_mn -= 60
        clk_hr += 1
    while clk_hr >= 24:
        clk_hr -= 24
        day += 1
    while day >= dayInMon[monthpos]:
        day -= dayInMon[monthpos]
        monthpos += 1
    while monthpos >= 12:
        monthpos -= 1
        year += 1

    advanList = [monthpos, day, clk_hr, clk_mn, clk_sc, year]
    return advanList

# print clocks function
def printClocks(advanList):
    # seperate out variables from list
    monthpos, day, clk_hr, clk_mn, clk_sc, year = advanList

    # int times
    clk_hr, clk_mn, clk_sc = list(map(int, [clk_hr, clk_mn, clk_sc]))

    # add 0s to single digit times
    if len(str(clk_hr)) == 1:
        clk_hr = '0' + str(clk_hr)
    else:
        clk_hr = str(clk_hr)
    if len(str(clk_mn)) == 1:
        clk_mn = '0' + str(clk_mn)
    else:
        clk_mn = str(clk_mn)
    if len(str(clk_sc)) == 1:
        clk_sc = '0' + str(clk_sc)
    else:
        clk_sc = str(clk_sc)

    newmonth = monthList[monthpos]
    newtime = ':'.join((clk_hr, clk_mn, clk_sc))
    advanced = ' '.join((newmonth, str(int(day)), newtime, str(int(year))))
    return advanced

# assign final times to new variables
clock_E = sepClocks(fin_Etime)
clock_S = sepClocks(fin_Stime)
clock_PSR = sepClocks(fin_PSRtime)
clock_BH = sepClocks(fin_BHtime)
clock_Gar = sepClocks(fin_Gartime)
clock_NGC = sepClocks(fin_NGCtime)

# print clock headers
print('\n')
print('Earth\t\t\tSun  \t\t\tPSR B1919+21\t\tGW150914\t\tGargantua\t\tNGC 1277')
print('--------------------------------------------------------------------------------------------------------------------------------------------')

# run clocks
runtime = int(args.runtime)
ticker = 0
while ticker <= runtime:
    # advance the clocks
    clock_E = runClocks(clock_E, 1)
    prnt_E = printClocks(clock_E)
    clock_S = runClocks(clock_S, tauS_E)
    prnt_S = printClocks(clock_S)
    clock_PSR = runClocks(clock_PSR, tauGar_E)
    prnt_PSR = printClocks(clock_PSR)
    clock_BH = runClocks(clock_BH, tauBH_E)
    prnt_BH = printClocks(clock_BH)
    clock_Gar = runClocks(clock_Gar, tauGar_E)
    prnt_Gar = printClocks(clock_Gar)
    clock_NGC = runClocks(clock_NGC, tauGar_E)
    prnt_NGC = printClocks(clock_NGC)

    # print new times
    print('{}\t{}\t{}\t{}\t{}\t{}'.format(prnt_E, prnt_S, prnt_PSR, prnt_BH, prnt_Gar, prnt_NGC))

    # increase ticker and pause one second
    ticker += 1
    time.sleep(1)