#! /usr/bin/env python
print "running..."
import ow
import time
import sys

ow.init( 'u' )

# We're accessing the 1-wire bus directly from python but
# if you want to use owserver:
# ow.init( 'localhost:3030' ) # /opt/owfs/bin/owserver -p 3030 -u -r

sensors = ow.Sensor("/").sensorList()

# We're only interested in temperature sensors so remove
# any 1-wire devices which aren't temperature sensors
for sensor in sensors[:]:
    if sensor.type != 'DS18B20':
        sensors.remove( sensor ) 

# Print column headers
for sensor in sensors:
    print sensor.r_address + "\t",
print "\n",

# Print temperatures
while 1==1:
    print int(time.time()), "\t",
    for sensor in sensors:
        print sensor.temperature, "\t",
        sys.stdout.flush()
    print "\n",
    sys.stdout.flush()
    time.sleep(60)
