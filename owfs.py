#! /usr/bin/env python
print "running..."
import ow
import time
import sys # for handling errors
import urllib2 # for sending data to Pachube
import json # for assembling JSON data for Pachube
import xml.etree.ElementTree as ET # for loading config

#########################################
#            CONSTANTS                  #
#########################################

configTree = ET.parse("config.xml") # load config from config file
API_KEY    = configTree.findtext("apikey") # Your Pachube API Key
FEED       = configTree.findtext("feed")   # Your Pachube Feed number

#########################################
#        PUSH TO PACHUBE                #
#########################################

def pushToPachube( sensor ):
    '''For sending a single reading to Pachube'''
    # adapted from http://stackoverflow.com/a/111988
    jsonData = json.dumps({
                           "version":"1.0.0",
                           "datastreams":[{
                                           "id"           : sensor.r_address,
                                           "current_value": sensor.temperature,
                                           "unit": {
                                                    "type"  : "derivedSI",
                                                    "label" : "degree Celsius",
                                                    "symbol": u"\u00B0C"}
                                           }
                                          ] 
                           })
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request('http://api.pachube.com/v2/feeds/'+FEED, data=jsonData)
    request.add_header('X-PachubeApiKey', API_KEY)
    request.get_method = lambda: 'PUT'
    try:
        opener.open(request)
    except urllib2.URLError as reason:
        sys.stderr.write("URL IO error: " + str(reason) + "\n")
    except urllib2.HTTPError as reason:
        sys.stderr.write("HTTP error: " + str(reason) + "\n")

##################

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
while True:
    print int(time.time()), "\t",
    for sensor in sensors:
        print sensor.temperature, "\t",
        pushToPachube(sensor)
        sys.stdout.flush()
    print "\n",
    sys.stdout.flush()
    time.sleep(60)
