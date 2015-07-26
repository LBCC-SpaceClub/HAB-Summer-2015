__author__ = 'The LBCC Space Club'

import time, serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
print ser

def parseGPS(line):
    '''
    Parse a gps string into a list of components.
    Sample string:
    !4432.22N/12315.39WO000/000/A=000082V2F6LBCC Near-Space Exploration
    '''
    try:
        # lat should be in format 'dd mm.ss N'
        lat = line[1:3] + line[3:9]
        # ugly fix for spacing out the N char
        lat = lat[:len(lat)-1]+' '+lat[-1:]

        # long should be in format 'ddd mm.ss W'
        long = line[10:13] + line[12:19]
        long = long[:len(long)-1]+' '+long[-1:]

        alt, volt = line[30:36], line[37:40]
        return lat, long, alt, volt
    except Exception, e:
        print "Error: " + str(e)

while True:
    data = ser.readline()
    if data:
        callsign = data.split('>')[0]
        if callsign == 'N7SEC-1':
            lat, long, alt, volt = parseGPS(ser.readline())
            print 'GPS Coordinates: {}, {}'.format(lat, long)
            print 'Altitude: {}, voltage:{}'.format(alt, volt)
        else:
            print "Invalid callsign: " + data
            print "Discarding gps data: " + ser.readline()