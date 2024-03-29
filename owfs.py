#!/usr/bin/python
print "running..."
import ow
import time
import sys # for handling errors
import xml.etree.ElementTree as ET # for loading config
from cosmSender import CosmSender

#########################################
#            CONSTANTS                  #
#########################################

configTree = ET.parse("config.xml") # load config from config file
API_KEY    = configTree.findtext("apikey") # Your Pachube API Key
FEED       = configTree.findtext("feed")   # Your Pachube Feed number

##################
# OWFS           #
##################

ow.init( 'u' )

# We're accessing the 1-wire bus directly from python but
# if you want to use owserver:
# ow.init( 'localhost:3030' ) # /opt/owfs/bin/owserver -p 3030 -u -r

sensors = ow.Sensor("/").sensorList()


dataStreamDefaults = {
    "unit": {
        "type"  : "derivedSI",
        "label" : "degree Celsius",
        "symbol": u"\u00B0C"}
    }

c = CosmSender(API_KEY, FEED, dataStreamDefaults, cacheSize=3)

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
while True:
    print int(time.time()), "\t",
    for sensor in sensors:
        print sensor.temperature, "\t",

        try:
            c.sendData(sensor.r_address, sensor.temperature)
        except:
            import traceback
            sys.stderr.write('Generic error: ' + traceback.format_exc())

        sys.stdout.flush()
    print "\n",
    sys.stdout.flush()
    time.sleep(60)

c.flush()
