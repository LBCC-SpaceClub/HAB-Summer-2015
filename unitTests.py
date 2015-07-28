# import sys
# sys.path.append('../')
from unittest import TestCase
from groundStation import parseGPS

__author__ = 'Levi Willmeth'


class unitTests(TestCase):
  def test_parseGPS(self):
    lat = '4435.17N'
    long = '12306.84W'

    deg, min, hem = int(lat[:2]), float(lat[2:7]), lat[-1]
    # assert(todecimal(deg, min, hem) == 44.586167)
    print parseGPS("!4432.22N/12315.39WO000/000/A=000082V2F6LBCC Near-Space Exploration")

    deg, min, hem = int(long[:3]), float(long[3:8]), long[-1]
    # assert(todecimal(deg, min, hem) == -123.114000)