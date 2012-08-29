#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""IETF RFC 5870 A Uniform Resource Identifier for Geographic Locations
('geo' URI) unit test."""
__author__ = ('Lance Finn Helsten',)
__version__ = '1.0'
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
__license__ = """
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
__docformat__ = "reStructuredText en"

import sys
import unittest

from pyietflib.rfc5870 import *

class GeoSchemeTest(unittest.TestCase):

    def test_default_crs(self):
        """Testing geo_uri sets the default crs to WGS-84."""
        x = geo_uri("geo:0,0,0;a=1;b=2;c=ab%2dcd")
        x = geo_uri("geo:0,0,0")
        self.assertEqual('wgs84', x.crs)
        self.assertTrue(isinstance(x, geouri.GeoURI_WGS84))
        self.assertIsNone(x.uncertainty)
        self.assertEqual("geo:0,0,0", str(geo_uri("geo:0,0,0")))
    
    def test_equality(self):
        """Testing geo_uri equaltity operation."""
        self.assertEqual(geo_uri("geo:0,0,0"), geo_uri("geo:0,0,0"))
        self.assertEqual(geo_uri("geo:0,0,0;crs=wgs84"), geo_uri("geo:0,0,0"))
        self.assertEqual(geo_uri("geo:0,0,0;crs=wgs84"), geo_uri("geo:0,0,0;crs=wgs84"))
        
        self.assertEqual(geo_uri("geo:90,0,0"), geo_uri("geo:90,0,0"))
        self.assertEqual(geo_uri("geo:90,0,0"), geo_uri("geo:90,-22.43,0;crs=wgs84"))
        self.assertEqual(geo_uri("geo:90,0,0"), geo_uri("geo:90,180,0"))
        self.assertEqual(geo_uri("geo:90,0,0"), geo_uri("geo:90,-180,0"))
        self.assertEqual(geo_uri("geo:0,180,0"), geo_uri("geo:0,-180,0"))
        self.assertEqual(geo_uri("geo:27,180,0"), geo_uri("geo:27,-180,0"))
        
        self.assertEqual(geo_uri("geo:0,0,0;u=30"), geo_uri("geo:0,0,0;u=30"))
        self.assertEqual(geo_uri("geo:0,0,0;u=30"), geo_uri("geo:0,0,0;u=29.9999"))
        self.assertNotEqual(geo_uri("geo:0,0,0;u=30"), geo_uri("geo:0,0,0"))
        self.assertNotEqual(geo_uri("geo:0,0,0;u=30"), geo_uri("geo:0,0;u=30"))
        
        self.assertNotEqual(geo_uri("geo:0,0,0"), geo_uri("geo:0,0"))
        self.assertNotEqual(geo_uri("geo:0,0,0"), geo_uri("geo:1,0,0"))
        self.assertNotEqual(geo_uri("geo:0,0,0"), geo_uri("geo:0,1,0"))
        self.assertNotEqual(geo_uri("geo:0,0,0"), geo_uri("geo:0,0,1"))
        
        self.assertEqual(geo_uri("geo:40.685922,-111.853206,1321"), geo_uri("geo:40.685922,-111.853206,1321"))
        self.assertEqual(geo_uri("geo:40.685922,-111.853206"), geo_uri("geo:40.685922,-111.853206"))
        self.assertNotEqual(geo_uri("geo:40.685922,-111.853206,1321"), geo_uri("geo:40.685922,-111.853206"))
        
        self.assertEqual(geo_uri("geo:40.685,-111.85,1321"), geo_uri("geo:40.685000,-111.8500,1321"))
        
        self.assertEqual(geo_uri("geo:0,0,0;unknown=ab-cd"), geo_uri("geo:0,0,0;unknown=ab%2dcd"))
        self.assertNotEqual(geo_uri("geo:0,0,0;unknown=ab%21cd"), geo_uri("geo:0,0,0"))
        
        self.assertEqual(geo_uri("geo:0,0;a=1;b=2"), geo_uri("geo:0,0;b=2;a=1"))
        
    def test_unknown_crs(self):
        """Check that geo_uri raises exception for unknown coordinate
        reference system (crs)."""
        self.assertRaises(ValueError, geo_uri, "geo:0,0,0;crs=SpamEggs")
        
    def test_faulty(self):
        """Check that geo_uri raises exceptions for faulty URI formats."""
        self.assertRaises(ValueError, geo_uri, "xxx:40.685922,-111.853206,1321;crs=wgs84;u=1.2")
        self.assertRaises(ValueError, geo_uri, "geo:40.685922,-111.853206,1321;u=1.2;crs=wgs84")
        self.assertRaises(ValueError, geo_uri, "geo:40.685922,-111.853206,1321;crs=wgs84;spam=1;u=1.2")


class GeoURI_WGS84_Test(unittest.TestCase):
    def test_urn(self):
        """Testing the URN for the WGS-84 CRS identifier."""
        self.assertEqual("urn:ogc:def:crs:EPSG::4979", geo_uri("geo:48.2010,16.3695,183").crs_urn)
        self.assertEqual("urn:ogc:def:crs:EPSG::4326", geo_uri("geo:48.198634,16.371648;crs=wgs84;u=40").crs_urn)
    
    def test_3d(self):
        """Testing geo_uri WGS-84 lattitue, longitude, and altitude format."""
        x = geo_uri("geo:40.685922,-111.853206,1321;crs=WGS84")
        self.assertEqual('wgs84', x.crs)
        self.assertAlmostEqual(40.685922, x.lattitude, places=6)
        self.assertAlmostEqual(-111.853206, x.longitude, places=6)
        self.assertAlmostEqual(1321, x.altitude, places=3)
        self.assertEqual("geo:40.685922,-111.853206,1321;crs=wgs84", str(x))
    
    def test_2d(self):
        """Testing geo_uri WGS-84 lattitue and longitude format."""
        x = geo_uri("geo:40.685922,-111.853206;crs=wgs84")
        self.assertEqual('wgs84', x.crs)
        self.assertAlmostEqual(40.685922, x.lattitude, places=6)
        self.assertAlmostEqual(-111.853206, x.longitude, places=6)
        self.assertIsNone(x.altitude)
        self.assertEqual("geo:40.685922,-111.853206;crs=wgs84", str(x))
    
    def test_0(self):
        """Testing geo_uri WGS-84 zeros."""
        x = geo_uri("geo:0,0,0;crs=wgs84")
        y = geo_uri("geo:-0,-0,-0;crs=wgs84")
        self.assertEqual(x, y)
        self.assertEqual("geo:0,0,0;crs=wgs84", str(x))
        self.assertEqual("geo:0,0,0;crs=wgs84", str(y))
    
    def test_poles(self):
        """Testing geo_uri WGS-84 at the poles."""
        x = geo_uri("geo:90,0;crs=wgs84")
        self.assertEqual(x, geo_uri("geo:90,-180;crs=wgs84"))
        self.assertEqual(x, geo_uri("geo:90,180;crs=wgs84"))
        self.assertEqual(x, geo_uri("geo:90,1;crs=wgs84"))
        self.assertEqual("geo:90,0;crs=wgs84", str(geo_uri("geo:90,-23;crs=wgs84")))
        
        x = geo_uri("geo:-90,0;crs=wgs84")
        self.assertEqual(x, geo_uri("geo:-90,-180;crs=wgs84"))
        self.assertEqual(x, geo_uri("geo:-90,180;crs=wgs84"))
        self.assertEqual(x, geo_uri("geo:-90,-32;crs=wgs84"))
        self.assertEqual("geo:-90,0;crs=wgs84", str(geo_uri("geo:-90,72;crs=wgs84")))
    
    def test_uncertainty(self):
        """Testing geo_uri WGS-84 uncertainty ranges."""
        x = geo_uri("geo:40.685922,-111.853206,1321;crs=wgs84;u=0")
        self.assertAlmostEqual(40.685922, x.lattitude, places=6)
        self.assertAlmostEqual(-111.853206, x.longitude, places=6)
        self.assertAlmostEqual(1321, x.altitude, places=3)

        xr = x.lattitude_range
        self.assertAlmostEqual(40.685922, xr[0], places=6)
        self.assertAlmostEqual(40.685922, xr[1], places=6)
        
        xr = x.longitude_range
        self.assertAlmostEqual(-111.853206, xr[0], places=6)
        self.assertAlmostEqual(-111.853206, xr[1], places=6)
        
        xr = x.altitude_range
        self.assertAlmostEqual(1321, xr[0], places=3)
        self.assertAlmostEqual(1321, xr[1], places=3)
        
        y = geo_uri("geo:40.685922,-111.853206,1321;crs=wgs84;u=30")
        self.assertAlmostEqual(40.685922, y.lattitude, places=6)
        self.assertAlmostEqual(-111.853206, y.longitude, places=6)
        self.assertAlmostEqual(1321, y.altitude, places=3)
        
        yr = y.lattitude_range
        self.assertAlmostEqual(40.685652, yr[0], places=6)
        self.assertAlmostEqual(40.686192, yr[1], places=6)
        
        yr = y.longitude_range
        # TODO: This range assumes a sphere of radius 6378137 m, whereas
        # the earth is an elipsoid with that radius as the semi-major
        # axis and 6356752.3142 m as the radius of the semi-minor axis
        # at the poles.
        self.assertAlmostEqual(-111.853561, yr[0], places=6)
        self.assertAlmostEqual(-111.852851, yr[1], places=6)
        
        yr = y.altitude_range
        self.assertAlmostEqual(1291, yr[0], places=3)
        self.assertAlmostEqual(1351, yr[1], places=3)
        
        z = geo_uri("geo:40.685922,-111.853206,1321;crs=wgs84")
        self.assertIsNone(z.lattitude_range)
        self.assertIsNone(z.longitude_range)
        self.assertIsNone(z.altitude_range)
    
    def test_max(self):
        """Testing geo_uri WGS-84 max values."""
        self.assertRaises(ValueError, geo_uri, "geo:90.000001,180.000001,0;crs=wgs84")
    
    def test_min(self):
        """Testing geo_uri WGS-84 min values."""
        self.assertRaises(ValueError, geo_uri, "geo:-90.000001,-180.000001,0;crs=wgs84")
    



