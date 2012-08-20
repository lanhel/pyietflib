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

import rfc6350

class ParameterTest(unittest.TestCase):

    def test_any(self):
        p = rfc6350.build_parameter("ANY-PARAM", 'param1,param2')
        self.assertEqual('ANY-PARAM', p.name)
        self.assertEqual(['param1', 'param2'], p.value)
        self.assertEqual(';ANY-PARAM=param1,param2', str(p))        
        
    def test_language(self):
        from rfc5646 import LanguageTag
        l = LanguageTag('en-US')
        p = rfc6350.build_parameter('LANGUAGE', 'en-US')
        self.assertEqual('LANGUAGE', p.name)
        self.assertEqual(l, p.value)
        self.assertEqual(';LANGUAGE=en-US', str(p))

    def test_value(self):
        p = rfc6350.build_parameter('VALUE', 'text')
        self.assertEqual('VALUE', p.name)
        self.assertEqual('text', p.value)
        self.assertEqual(';VALUE=text', str(p))
    
    @unittest.expectedFailure
    def test_value_invalid(self):
        rfc6350.build_parameter('VALUE', 'spam_eggs')

    def test_pref(self):
        p = rfc6350.build_parameter("PREF", '69')
        self.assertEqual('PREF', p.name)
        self.assertEqual(69, p.value)
        self.assertEqual(';PREF=69', str(p))        
    
    @unittest.expectedFailure
    def test_pref_small(self):
        rfc6350.build_parameter('PREF', '-1')
    
    @unittest.expectedFailure
    def test_pref_large(self):
        rfc6350.build_parameter('PREF', '101')

    def test_altid(self):
        p = rfc6350.build_parameter("ALTID", 'param1')
        self.assertEqual('ALTID', p.name)
        self.assertEqual('param1', p.value)
        self.assertEqual(';ALTID=param1', str(p))        

    def test_pid(self):
        p = rfc6350.build_parameter("PID", '131.5,5,0.7')
        self.assertEqual('PID', p.name)
        self.assertEqual([131.5, 5.0, 0.7], p.value)
        self.assertEqual(';PID=131.5,5,0.7', str(p))        

    def test_type(self):
        p = rfc6350.build_parameter('TYPE', 'work,home')
        self.assertEqual('TYPE', p.name)
        self.assertEqual(['work','home'], p.value)
        self.assertEqual(';TYPE=work,home', str(p))

    @unittest.expectedFailure
    def test_type_invalid(self):
        rfc6350.build_parameter('TYPE', 'spam_eggs')

    @unittest.skip("RFC2045 and RFC4288 must be implemented.")
    def test_mediatype(self):
        p = rfc6350.build_parameter("MEDIATYPE", 'text/html')
        self.assertEqual('MEDIATYPE', p.name)
        self.assertEqual('text/html', p.value)
        self.assertEqual(';MEDIATYPE=text/html', str(p))        


    @unittest.skip("Unimplemented.")
    def test_calscale(self):
        """`§ 5.8 <http://tools.ietf.org/html/rfc6350#section-5.8>`_"""
        param_abnf = '''calscale-param = "CALSCALE=" calscale-value'''
        value_abnf = '''calscale-value = "gregorian" / iana-token / x-name'''
        param_name = 'CALSCALE'


    @unittest.skip("Unimplemented.")
    def test_sortas(self):
        """`§ 5.9 <http://tools.ietf.org/html/rfc6350#section-5.9>`_"""
        param_abnf = '''sort-as-param = "SORT-AS=" sort-as-value'''
        value_abnf = '''sort-as-value = param-value *("," param-value)'''
        param_name = 'SORT-AS'


    @unittest.skip("Unimplemented.")
    def test_geo(self):
        """`§ 5.10 <http://tools.ietf.org/html/rfc6350#section-5.10>`_"""
        param_abnf = '''geo-parameter = "GEO=" DQUOTE URI DQUOTE'''
        param_name = 'GEO'


    @unittest.skip("Unimplemented.")
    def test_tz(self):
        """`§ 5.11 <http://tools.ietf.org/html/rfc6350#section-5.11>`_"""
        param_abnf = '''tz-parameter = "TZ=" (param-value / DQUOTE URI DQUOTE)'''
        param_name = 'TZ'



