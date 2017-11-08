"""
Created on Mon Nov 7 20:00:00 2017

@author: Kenny Higginbotham
"""

import time
import math


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
GW150914_m = 62.0*sun_m
GW150914_r = 199.0*10**3
garg_m = 100.0*10**6*sun_m
garg_r = 300.0*10**9

# tau ratio function
def taurat(m,r):
    return math.sqrt((1-(2*G*m)/(r*c**2))/(1-(2*G*earth_m)/(earth_r*c**2)))

# Find and print base and start time
base = "Thu Nov 25 12:00:00 1915"
# base = "Tue Nov 7 23:00:00 2015"
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

# floor seconds
elap_E = int(elap_E)

# decimal function
def dec(num1, num2):
    return float(num1/num2) - int(num1/num2)

# function to convert elapsed seconds to elapsed years, days, etc
def calendar(seconds):
    year = ((seconds-leap_years*Lyear_sec)/NLyear_sec)+leap_years
    dec_dayPerYear = dec(year, 1)/year
    dec_day = dec_dayPerYear*(leap_years*Lyear_sec+(year-leap_years)*NLyear_sec)
    day = dec_day/day_sec
    dec_hour = dec(dec_day, day_sec)*day_sec
    hour = dec_hour/hour_sec
    dec_min = dec(dec_hour, hour_sec)*hour_sec
    minutes = dec_min/min_sec
    sec = dec(dec_min, min_sec)*min_sec
    return [int(year), int(day), int(hour), int(minutes), int(sec)]

# calculate calendar time passed one earth
Etime_list = calendar(elap_E)

# calculate elapsed years, days, hours, minutes, seconds on other locations (including decimals)
Sdec_list = [tauS_E*i for i in Etime_list]
BHdec_list = [tauBH_E*i for i in Etime_list]
Gardec_list = [tauGar_E*i for i in Etime_list]

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
    if these_years[-1] == 1:
        isLeap = True
    else:
        isLeap = False
    return sum(these_years), isLeap

# function for pushing back decimals in converted times
def decpush(intime):
    inyear, inday, inhour, inmin, insec = intime
    year = int(inyear)
    numLeap, thisLeap = leaps(year)
    if year != 0:
        dec_dayPerYear = dec(inyear,1)/year
        dec_day = dec_dayPerYear*(numLeap*Lyear_sec+(year-numLeap)*NLyear_sec)
    else:
        if thisLeap:
            dec_day = inyear*Lyear_sec
        else:
            dec_day = inyear*NLyear_sec
    newday = inday + dec_day/day_sec
    day = int(newday)
    dec_hour = dec(newday, day_sec)*day_sec
    newhour = inhour + dec_hour/hour_sec
    hour = int(newhour)
    dec_min = dec(newhour, hour_sec)*hour_sec
    newmin = inmin + dec_min/min_sec
    minutes = int(newmin)
    dec_sec = dec(newmin, min_sec)*min_sec
    newsec = insec + dec_sec
    sec = int(newsec)
    if 'thisLeap' in locals():
        if thisLeap:
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
        day == 1
        hour -= 24
    while day >= minusdays:
        year += 1
        day -= minusdays
    return [year, day, hour, minutes, sec]


# calculate elapsed times for other locations
Stime_list = decpush(Sdec_list)
BHtime_list = decpush(BHdec_list)
Gartime_list = decpush(Gardec_list)

# print total times past
print('\n')
print('Place\t Years\t Days\t Hours\t Min\t Sec')
print('Earth\t {}\t {}\t {}\t {}\t {}'.format(Etime_list[0], Etime_list[1], Etime_list[2], Etime_list[3], Etime_list[4]))
print('Sun\t {}\t {}\t {}\t {}\t {}'.format(Stime_list[0], Stime_list[1], Stime_list[2], Stime_list[3], Stime_list[4]))
print('BH\t {}\t {}\t {}\t {}\t {}'.format(BHtime_list[0], BHtime_list[1], BHtime_list[2], BHtime_list[3], BHtime_list[4]))
print('Gar\t {}\t {}\t {}\t {}\t {}'.format(Gartime_list[0], Gartime_list[1], Gartime_list[2], Gartime_list[3], Gartime_list[4]))