#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""RFC6350 Unit Test."""
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

import pyietflib.rfc2045
import pyietflib.rfc5870
import pyietflib.rfc6350

class ParameterTest(unittest.TestCase):

    def test_any(self):
        p = pyietflib.rfc6350.build_parameter("ANY-PARAM", 'param1,param2')
        self.assertEqual('ANY-PARAM', p.name)
        self.assertEqual(['param1', 'param2'], p.value)
        self.assertEqual(';ANY-PARAM=param1,param2', str(p))        
        
    def test_language(self):
        from pyietflib.rfc5646 import LanguageTag
        l = LanguageTag('en-US')
        p = pyietflib.rfc6350.build_parameter('LANGUAGE', 'en-US')
        self.assertEqual('LANGUAGE', p.name)
        self.assertEqual(l, p.value)
        self.assertEqual(';LANGUAGE=en-US', str(p))

    def test_value(self):
        p = pyietflib.rfc6350.build_parameter('VALUE', 'text')
        self.assertEqual('VALUE', p.name)
        self.assertEqual('text', p.value)
        self.assertEqual(';VALUE=text', str(p))
    
    @unittest.expectedFailure
    def test_value_invalid(self):
        pyietflib.rfc6350.build_parameter('VALUE', 'spam_eggs')

    def test_pref(self):
        p = pyietflib.rfc6350.build_parameter("PREF", '69')
        self.assertEqual('PREF', p.name)
        self.assertEqual(69, p.value)
        self.assertEqual(';PREF=69', str(p))        
    
    @unittest.expectedFailure
    def test_pref_small(self):
        pyietflib.rfc6350.build_parameter('PREF', '-1')
    
    @unittest.expectedFailure
    def test_pref_large(self):
        pyietflib.rfc6350.build_parameter('PREF', '101')

    def test_altid(self):
        p = pyietflib.rfc6350.build_parameter("ALTID", 'param1')
        self.assertEqual('ALTID', p.name)
        self.assertEqual('param1', p.value)
        self.assertEqual(';ALTID=param1', str(p))        

    def test_pid(self):
        p = pyietflib.rfc6350.build_parameter("PID", '131.5,5,0.7')
        self.assertEqual('PID', p.name)
        self.assertEqual([131.5, 5.0, 0.7], p.value)
        self.assertEqual(';PID=131.5,5,0.7', str(p))        

    def test_type(self):
        p = pyietflib.rfc6350.build_parameter('TYPE', 'work,home')
        self.assertEqual('TYPE', p.name)
        self.assertEqual(['work','home'], p.value)
        self.assertEqual(';TYPE=work,home', str(p))

    @unittest.expectedFailure
    def test_type_invalid(self):
        pyietflib.rfc6350.build_parameter('TYPE', 'spam_eggs')

    def test_mediatype(self):
        p = pyietflib.rfc6350.build_parameter("MEDIATYPE", 'text/plain')
        self.assertEqual('MEDIATYPE', p.name)
        self.assertEqual(pyietflib.rfc2045.ContentType('text/plain'), p.value)
        self.assertEqual(';MEDIATYPE=text/plain', str(p))        

    def test_calscale(self):
        """`§ 5.8 <http://tools.ietf.org/html/rfc6350#section-5.8>`_"""
        p = pyietflib.rfc6350.build_parameter("CALSCALE", 'gregorian')
        self.assertEqual('CALSCALE', p.name)
        self.assertEqual('gregorian', p.value)
        self.assertEqual(';CALSCALE=gregorian', str(p))

    def test_sortas(self):
        """`§ 5.9 <http://tools.ietf.org/html/rfc6350#section-5.9>`_"""
        p = pyietflib.rfc6350.build_parameter("SORT-AS", 'a,b,c,"special;case"')
        self.assertEqual('SORT-AS', p.name)
        self.assertEqual(['a', 'b', 'c', 'special;case'], p.value)
        self.assertEqual(';SORT-AS=a,b,c,"special;case"', str(p))

    def test_geo(self):
        """`§ 5.10 <http://tools.ietf.org/html/rfc6350#section-5.10>`_"""
        p = pyietflib.rfc6350.build_parameter("GEO", '"geo:40.685922,-111.853206,1321"')
        self.assertEqual('GEO', p.name)
        self.assertEqual(pyietflib.rfc5870.geo_uri("geo:40.685922,-111.853206,1321"), p.value)
        self.assertEqual(';GEO="geo:40.685922,-111.853206,1321"', str(p))

    def test_tz(self):
        """`§ 5.11 <http://tools.ietf.org/html/rfc6350#section-5.11>`_"""
        p = pyietflib.rfc6350.build_parameter("TZ", 'MST')
        self.assertEqual('TZ', p.name)
        self.assertEqual("MST", p.value)
        self.assertEqual(';TZ=MST', str(p))

        p = pyietflib.rfc6350.build_parameter("TZ", '"tz:unknown"')
        self.assertEqual('TZ', p.name)
        self.assertEqual("tz:unknown", p.value)
        self.assertEqual(';TZ="tz:unknown"', str(p))



