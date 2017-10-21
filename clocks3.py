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
start_year = int(start_time[4]) - 1

# Calculate the total number of seconds in the intervening year
if abs(start_year - base_year) > 2:
    inter_year = start_year - base_year
    elap_E = elap_E + (inter_year * 31536000)

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