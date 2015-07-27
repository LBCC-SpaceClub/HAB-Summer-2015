__author__ = 'The LBCC Space Club'

import time, serial

class Waypoint:
    ' A GPS coordinate. '

    def __init__(self, lat, lon, alt, volt = 'NA', callsign='Unknown', desc='NA'):
        self.callsign = callsign
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.volt = volt
        self.desc = desc
        self.time = time.time()

    def __str__(self):
        'Overrided print function.'
        return "Callsign: {callsign}, Description: {desc}, " \
               "Lat: {lat}, Lon:{long}," \
                "Alt: {alt}, Voltage: {volt}, " \
               "Time: {time}"\
                .format(self.callsign, self.lat, self.lon,
                        self.alt, self.volt, self.desc, self.time)

    def getCallsign(self):
        return self.callsign

    def getCoords(self):
        return self.lat+' '+self.lon




def parseGPS(line):
    '''
    Parse a gps string into a list of components.
    Sample string:
    !4432.22N/12315.39WO000/000/A=000082V2F6LBCC Near-Space Exploration
    '''

    def todecimal(s):
        '''
        Converts from raw gps lat or long, to decimal coordinate
        Sample inputs can vary, here are two we expect to see:
        !4432.21N
        12315.39WO000
        '''
        # Strip leading non-numeric characters
        if s.startswith('!'):
            s = s[1:]
        # String becomes predictable from decimal point
        i = s.find('.')
        deg = int( s[:i-2] )
        min = float( s[i-2:i+3] )
        hem = s[i+3]
        result = deg + min/60
        # Account for pos/neg degrees
        if hem in ('W', 'S'):
            result *= -1
        return round(result, 6)

    '''
        Each gps reading is made up of two separate lines:
            N7SEC-1>APBL10,WIDE1-1,WIDE2-1: <<UI>>:
            !4432.21N/12315.39WO000/000/A=000099V2F6LBCC Near-Space Exploration

        The first line gives us the callsign and information about the ground
        station, the second line gives us information about the payload location.
    '''
    if len(line)>0:
        # Non-empty string, so we should attempt to parse it
        try:
            # First line contains callsign, but no other useful info
            callsign = line.split('>')[0]
            # Second line contains everything else
            line = ser.readline().split('/')
            # findDMS converts to format 'dd mm.ss N'
            lat = todecimal(line[0]) # ex. !4432.21N
            lon = todecimal(line[1]) # ex. 12315.39WO000
            # line[3] ex. A=000099V2F6LBCC Near-Space Exploration
            alt, volt = line[3][2:8], line[3][9:12]
            desc = line[3][12:]
            return callsign, lat, lon, alt, volt, desc
        except Exception, e:
            # An exception is thrown if any of the above formatting fails
            print "Error: " + str(e)
    # An empty return means no useful data was gathered
    return None

if __name__ == "__main__":
    try:
        # First, try to connect to the local radio source
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
        print ser

    except Exception, e:
        print "Error: Could not connect to radio source."
        print e
        quit() # If the connection fails, there is no point continuing

    # Next, create or append to a text file to save any results:
    filePath = 'logs/'
    fileName = time.strftime('%d/%m/%Y')
    f = open(filePath+fileName, 'a')

    while True:
        data = parseGPS(ser.readline())
        if data:
            wp = Waypoint(data)
            if wp.getCallsign() in lbccCallsigns:
                # It's one of our payloads, do something with it
                print wp
                # plot wp to map
                # write wp to file
                f.write(wp)
            else:
                # It's someone else's payload, but we should still see it
                print "Bogey detected, scrambling MIG's:"
                print "\t"+wp

    f.close()