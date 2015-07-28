__author__ = 'The LBCC Space Club'

import time, serial

class Waypoint:
    ' A GPS coordinate. '

    def __init__(self, dic):
        ' Create a new waypoint object '
        allowed_keys = ['callsign', 'lat', 'lon', 'alt', 'volt', 'desc']
        for k, v in dic.items():
            if k in allowed_keys:
                setattr(self, k, v)
        self.time = time.asctime( time.localtime(time.time()) )

    def __str__(self):
        ' Print function '
        return "{} spotted at: {}, {}; timestamp: {}".format(
            self.callsign, self.lat, self.lon, self.time)

    def getCallsign(self):
        return self.callsign

    def getCoords(self):
        return self.lat, self.lon


def parseGPS(line):
    '''
    Parse a gps string into a list of components.
    Sample string:
    !4432.22N/12315.39WO000/000/A=000082V2F6LBCC Near-Space Exploration
    Returns a dictionary of components.
    '''

    def todecimal(s):
        '''
        Helper function to convert deg:min:sec to decimal degrees
        Sample inputs can vary, here are two we expect to see:
        !4432.21N
        12315.39WO000
        '''
        if s.startswith('!'):
            s = s[1:]
        # String is predictable from decimal point
        i = s.find('.')
        deg = int(s[:i-2])
        min = float(s[i-2:i+3])
        hemisphere = s[i+3]
        result = deg + min/60
        # Account for hemisphere by flipping +/-
        if hemisphere in ('W', 'S'):
            result *= -1
        return round(result, 6)

    '''
        Each gps reading is made up of two separate lines:
            N7SEC-1>APBL10,WIDE1-1,WIDE2-1: <<UI>>:
            !4432.21N/12315.39WO000/000/A=000099V2F6LBCC Near-Space Exploration

        The first line gives us the call sign and information about the ground
        station, the second line gives us information about the payload location
    '''
    try:
        line = line.split('/')
        ret = {
            'lat': todecimal(line[0]),  # ex. !4432.21N
            'lon': todecimal(line[1]),  # ex. 12315.39WO000
            # line[3] ex. A=000099V2F6LBCC Near-Space Exploration
            'alt': int(line[3][2:8]),
            'volt': line[3][9:12],
            'desc': line[3][12:]
        }
        return ret
        # return lat, lon, alt, volt, desc

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

    # Next, listen for incoming serial data
    while True:
        # First line contains callsign, but no other useful info
        callsign = ser.readline()
        if callsign.find('>'):
            callsign = callsign.split('>')[0]
            # Second line contains everything else
            # parseGPS returns a dictionary of key:value pairs
            data = parseGPS(ser.readline())
        if callsign and data:
            # Waypoints can only be created from valid callsign/gps combinations
            data['callsign'] = callsign
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