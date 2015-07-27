from unittest import TestCase
from groundStation import dmsToDecimal

__author__ = 'Levi Willmeth'


class TestDmsToDecimal(TestCase):
  def test_latA(self):
    lat = '4435.17N'
    long = '12306.84W'

    deg, min, hem = int(lat[:2]), float(lat[2:7]), lat[-1]
    assert(dmsToDecimal(deg, min, hem) == 44.586167)

    deg, min, hem = int(long[:3]), float(long[3:8]), long[-1]
    assert(dmsToDecimal(deg, min, hem) == -123.114000)