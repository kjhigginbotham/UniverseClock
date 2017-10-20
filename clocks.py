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

# print start time
start = time.asctime()
print 'Starting time: %s \n' % start 

tauS_E = taurat(sun_m,sun_r)
tauBH_E = taurat(GW150914_m,GW150914_r)
tauGar_E = taurat(garg_m,garg_r)

# time elapsed = 10 seconds on Earth
elap_E = 21
elap_S = tauS_E*elap_E
elap_BH = tauBH_E*elap_E
elap_Gar = tauGar_E*elap_E

# print elapsed times
print 'Time elapsed on the surface of...'
print 'Earth: %f sec' % elap_E
print 'Sun: %f sec' % elap_S
print 'GW150914: %f sec' % elap_BH
print 'Gargantua: %f sec' % elap_Gar