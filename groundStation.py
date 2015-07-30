import time, serial, sys
# apparently, it's hard to import a library if it lacks an __init__.py
sys.path.insert(1, 'pygmaps')
import pygmaps
import webbrowser

class Waypoint:
    ''' A GPS coordinate. '''

    def __init__(self, dic):
        ' Create a new waypoint object '
        self.color = '#ffff00' # default yellow
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

    def setColor(self, color):
        self.color = color

    def getCoords(self):
        return self.lat, self.lon

    def mapInfo(self):
        return self.lat, self.lon, self.color


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

def drawRoute(route):
    '''
    Draws a map using a list of decimal deg waypoints
    '''
    for point in route:
        map.addpoint(point)


def main():
    try:
        # Try to connect to the local radio source
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
        # Next, create or append to a text file to save any results:
        filePath = 'logs/'
        fileName = time.strftime('%d-%m-%Y')+'.txt'
        f = open(filePath+fileName, 'a')
        print ser # debugging

    except Exception, e:
        # If the serial connection fails, there is no point continuing
        print "Error: Could not connect to radio source."
        print e
        quit()

    # List of valid LBCC callsigns
    lbccCallsigns = ['N7SEC-1']
    mapPath = 'maps/'+time.strftime('%d-%m-%Y')+'.html'
    map = pygmaps.maps(44.537, -123.2565, 14)
    route = []

    while True:
        # First string of data contains callsign & garbage
        callsign = ser.readline()
        if '>' in callsign:
            callsign = callsign.split('>')[0]
            # Second line contains everything else
            # parseGPS returns a dictionary of key:value pairs
            data = parseGPS(ser.readline())
            # Waypoints can only be created from valid data
            if data:
                data['callsign'] = callsign
                wp = Waypoint(data)
                if callsign in lbccCallsigns:
                    wp.setColor('#0000ff') # Set color to blue
                    # It's one of our payloads, do something with it
                    print wp
                    route.append(wp.mapInfo())
                    # write wp to file
                    f.write(wp)
                else:
                    # It's someone else's payload, but we should still see it
                    print "Bogey detected, scrambling MIG's:"
                    print "\t"+wp
                    # Draw unknown points in red(?)
                    wp.setColor('#0000ff') # Set color to blue

                # ugly, because this opens a new tab for new data
                map.addpoint(wp.mapInfo())
                map.draw(mapPath)
                webbrowser.open_new_tab(mapPath)

    f.close() # Close the text file..

if __name__ == "__main__":
    main()