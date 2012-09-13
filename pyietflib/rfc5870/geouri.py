#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`RFC5870 <http://tools.ietf.org/html/rfc5870>`_ A Uniform Resource
Identifier for Geographic Locations ('geo' URI)."""
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

import sys
if sys.version_info < (3, 2):
    raise Exception("rfc5870 requires Python 3.2 or higher.")
import locale
import logging
import math
import re
import urllib.parse

__all__ = ['geo_uri']

geouri_re = re.compile(r'''^
    geo
    (:(?P<coord_a>-?\d+(\.\d+)?))
    (,(?P<coord_b>-?\d+(\.\d+)?))
    (,(?P<coord_c>-?\d+(\.\d+)?))?
    (;crs=(?P<crsp>((wgs84)|([-0-9a-zA-Z]+))))?
    (;u=(?P<uncp>\d+(\.\d+)?))?
    (?P<parameters>(;[-0-9a-zA-Z]+(=([][:&+$]|[-_.!~*'()0-9a-zA-Z]|(%[0-9a-fA-F]{2}))+))*)
    $''', flags=re.ASCII|re.VERBOSE)

parameter_re = re.compile(r'''
        \s*;\s*
        (?P<pname>[-0-9a-zA-Z]+)
        \s*=\s*
        (?P<pvalue>([][:&+$]|[-_.!~*'()0-9a-zA-Z]|(%[0-9a-fA-F]{2}))+)
    ''', flags=re.ASCII|re.VERBOSE)


def geo_uri(geo):
    """This will parse a `geo` URI into object that contains the component
    parts that define a geographic location on the earth geoid. The `geo`
    URI is defined in `RFC5870 <http://tools.ietf.org/html/rfc5870>`_ A
    Uniform Resource Identifier for Geographic Locations ('geo' URI).
    """
    mo = geouri_re.match(geo)
    if not mo:
        raise ValueError("Invalid RFC 5870 geo URI: `{0}`.".format(geo))
    crs = mo.group('crsp')
    if crs is not None:
        crs = crs.lower()
    if crs is not None and crs not in crs2class:
        raise ValueError("Unknown crs `{0}` for geo URI.".format(mo.group('crsp')))
    subcls = crs2class[crs]
    return subcls(mo)

class GeoURI(dict):
    """This will parse a `geo` URI into component parts that define
    a geographic location on the earth geoid. The `geo` URI is defined
    in `RFC5870 <http://tools.ietf.org/html/rfc5870>`_ A Uniform Resource
    Identifier for Geographic Locations ('geo' URI).
    
    Properties
    ----------
    """
    def __init__(self, crs, crs_urn, mo):
        self.__crs = crs
        self.__crs_urn = crs_urn
        self.__crs_explicit = (mo.group('crsp') is not None)
        if mo.group('uncp') is None:
            del self.uncertainty
        else:
            self.uncertainty = mo.group('uncp')
        
        parameters = mo.group('parameters')
        pmo = parameter_re.search(parameters)
        while pmo:
            pname = pmo.group('pname').lower()
            if pname in ['crs', 'u']:
                raise ValueError("crs and u parameters have specific positions.")
            pvalue = pmo.group('pvalue')
            pvalue = urllib.parse.unquote(pvalue).lower()
            self[pname] = pvalue
            pmo = parameter_re.search(parameters, pmo.end())
        
        self.coord_a = mo.group('coord_a')
        self.coord_b = mo.group('coord_b')
        if mo.group('coord_c') is not None:
            self.coord_c = mo.group('coord_c')
        else:
            self.__coord_c = None
        self.__normalized = False
        
    def __eq__(self, o):
        if isinstance(o, GeoURI):
            self.__normalize_coord()
            if not (self.crs == o.crs and
                    self.uncertainty == o.uncertainty and
                    self.coord_a == o.coord_a and
                    self.coord_b == o.coord_b and
                    self.coord_c == o.coord_c):
                return False
            for pname, pvalue0 in self.items():
                if pname not in o:
                    return False
                if not self.compare_parameter(pname, pvalue0, o[pname]):
                    return False
            return True
        return NotImplemented
    
    def __ne__(self, o):
        return not self.__eq__(o)
    
    def __str__(self):
        def strip_float(f, n=6):
            return "{0:1.6f}".format(f).rstrip('0').rstrip('.')
        
        self.__normalize_coord()
        
        params = ['']
        if self.__crs_explicit:
            params.append('crs={0}'.format(self.crs))
        if self.uncertainty is not None:
            u = "{0:1.3f}".format(self.uncertainty).rstrip('0').rstrip('.')
            params.append('u={0}'.format(u))
        for pname, pvalue in self.items():
            if pname == 'crs' or pvalue == 'u':
                continue
            params.append('{0}={1}'.format(pname, urllib.parse.quote(pvalue, safe="-_.!~*'()[]:&+$")))
        if self.coord_c is not None:
            ca = strip_float(self.coord_a)
            cb = strip_float(self.coord_b)
            cc = strip_float(self.coord_c)
            return "geo:{0},{1},{2}{3}".format(ca, cb, cc, ';'.join(params))
        else:
            ca = strip_float(self.coord_a)
            cb = strip_float(self.coord_b)
            return "geo:{0},{1}{2}".format(ca, cb, ';'.join(params))
    
    def __repr__(self):
        return "geo_uri('{0}')".format(str(self))
    
    def __getitem__(self, key):
        if key == 'crs':
            return self.crs
        elif key == 'u':
            return self.uncertainty
        else:
            return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        if key == 'crs':
            self.crs = value
        elif key == 'u':
            self.uncertainty = value
        else:
            super().__setitem__(key, value)
    
    def __delitem__(self, key):
        if key == 'crs':
            raise KeyError("Unable to delete parameter `crs`.")
        elif key == 'u':
            self.uncertainty = None
        else:
            super().__setitem__(key, value)
    
    @property
    def crs(self):
        return self.__crs
    
    @property
    def crs_urn(self):
        return self.__crs_urn
    
    @property
    def uncertainty(self):
        return self.__uncertainty
    
    @uncertainty.setter
    def uncertainty(self, value):
        self.__uncertainty = round(float(value), 3)
    
    @uncertainty.deleter
    def uncertainty(self):
        self.__uncertainty = None
    
    @property
    def coord_a(self):
        self.__normalize_coord()
        return self.__coord_a
    
    @coord_a.setter
    def coord_a(self, value):
        value = float(value)
        self.coord_a_range(value)
        self.__coord_a = value

    def coord_a_range(self, value):
        raise NotImplementedError
    
    @property
    def coord_b(self):
        self.__normalize_coord()
        return self.__coord_b
    
    @coord_b.setter
    def coord_b(self, value):
        value = float(value)
        self.coord_b_range(value)
        self.__coord_b = value
    
    def coord_b_range(self, value):
        raise NotImplementedError
    
    @property
    def coord_c(self):
        self.__normalize_coord()
        return self.__coord_c
    
    @coord_c.setter
    def coord_c(self, value):
        value = float(value)
        self.coord_c_range(value)
        self.__coord_c = value
    
    @coord_c.deleter
    def coord_c(self):
        self.__coord_c = None
        
    def coord_c_range(self, value):
        raise NotImplementedError
    
    def __normalize_coord(self):
        if not self.__normalized:
            self.__normalized = True
            self.__coord_a, self.__coord_b, self.__coord_c = self.normalize_coord(self.__coord_a, self.__coord_b, self.__coord_c)
    
    def normalize_coord(self, a, b, c):
        """Normalize the coordinates."""
        return (a, b, c)
    
    def compare_parameter(self, pname, pvalue0, pvalue1):
        """In the context of `pname` do a comparision of `pvalue0` and
        `pvalue1`, the default is a simple equality check."""
        return (pvalue0 == pvalue1)


class GeoURI_WGS84(GeoURI):
    """This is a geo URI for WGS 84 reference geoid using lattitude and
    longitude when 'crs=wgs84'."""
    def __init__(self, mo):
        if mo.group('crsp') is None:
            super().__init__("wgs84", "urn:ogc:def:crs:EPSG::4979", mo)
        else:
            super().__init__("wgs84", "urn:ogc:def:crs:EPSG::4326", mo)
    
    def coord_a_range(self, value):
        if value < -90 or value > 90:
            raise ValueError("coord_a is not in range [-90, 90].")
    
    def coord_b_range(self, value):
        if value < -180 or value > 180:
            raise ValueError("coord_b is not in range [-180, 180].")
    
    def coord_c_range(self, value):
        pass
    
    def normalize_coord(self, a, b, c):
        """Normalize the coordinates."""
        if a == 90 or a == -90:
            b = 0
        elif a == -0:
            a = 0
        
        if b == -180:
            b = 180
        elif b == -0:
            b = 0
        
        if c == -0:
            c = 0
        return (a, b, c)
    
    @property
    def lattitude(self):
        return self.coord_a
    
    @property
    def lattitude_range(self):
        if self.uncertainty is None:
            return None
        else:
            epsilon = self.uncertainty / (1852 * 60)
            return (self.lattitude - epsilon, self.lattitude + epsilon)
    
    @property
    def longitude(self):
        return self.coord_b
    
    @property
    def longitude_range(self):
        if self.uncertainty is None:
            return None
        else:
            r = 6378137 * math.cos(math.radians(self.lattitude))
            epsilon = self.uncertainty / r
            epsilon = math.degrees(epsilon)
            return (self.longitude - epsilon, self.longitude + epsilon)
    
    @property
    def altitude(self):
        return self.coord_c
    
    @property
    def altitude_range(self):
        if self.altitude is None or self.uncertainty is None:
            return None
        else:
            epsilon = self.uncertainty
            return (self.altitude - epsilon, self.altitude + epsilon)


crs2class = {
    None:GeoURI_WGS84,
    'wgs84':GeoURI_WGS84
}


