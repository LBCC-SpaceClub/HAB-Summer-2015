from unittest import TestCase
from groundStation import *

__author__ = 'Levi Willmeth'


class TestParseGPS(TestCase):
    def test_parseGPS(self):
        sampleData = (
            '!4432.22N/12315.39WO000/000/A=000082V2F6LBCC Near-Space Exploration',
            '!4435.48N/12316.44WO000/000/A=000092V2E5LBCC Near-Space Exploration'
        )
        g_results = (
            {   'lat': 44.537000,
                'lon': -123.256500,
                'alt': 82,
                'volt': '2F6',
                'desc': 'LBCC Near-Space Exploration'
            }, {'lat': 44.537000,
                'lon': -123.256500,
                'alt': 82,
                'volt': '2F6',
                'desc': 'LBCC Near-Space Exploration'
            }
        )
        # (44.537000, -123.256500, 82, '2F6', 'LBCC Near-Space Exploration'),
        # (44.591333, -123.274000, 92, '2E5', 'LBCC Near-Space Exploration')


        # a = Waypoint(callsign = 'N7SEC-1',
        #              lat = 44.537000,
        #              lon = -123.256500,
        #              alt = 82,
        #              volt = '2F6',
        #              desc = 'LBCC Near-Space Exploration',
        #              test = 'testing')
        # print a.getCoords()
        # print a.__dict__

        bData = {
            'callsign': 'N7SEC-1',
            'lat': 44.537000,  # ex. !4432.21N
            'lon': -123.256500,  # ex. 12315.39WO000
            'alt': 82,
            'volt': '2F6',
            'desc': 'LBCC Near-Space Exploration'
        }
        b = Waypoint(bData)
        print b

        # Compare all samples and google maps results above
        # for a,b in zip(sampleData, g_results):
        #     res = parseGPS(a)
        #     print res
        #     print Waypoint(res).getCoords()
            # wp = Waypoint(a)
            # self.assertEqual(wp.getCoords(), g_results[:2])
            # self.assertEqual(res, b)

    # def test_waypoint(self):
