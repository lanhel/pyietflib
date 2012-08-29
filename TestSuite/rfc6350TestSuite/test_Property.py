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

from pyietflib.rfc6350 import *

class PropertyTest(unittest.TestCase):
    
    def test_tag_N(self):
        v = 'N:Helsten;Lance;Finn;;\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('N', p.name)
        self.assertEqual('Helsten;Lance;Finn;;', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

    def test_tag_FN(self):
        v = 'FN:Lance Finn Helsten\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('FN', p.name)
        self.assertEqual('Lance Finn Helsten', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

    def test_tag_ORG(self):
        v = 'ORG:Flying Titans\, Inc.;\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('ORG', p.name)
        self.assertEqual('Flying Titans\, Inc.;', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

    def test_tag_TITLE(self):
        v = 'TITLE:Chief Engineer\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('TITLE', p.name)
        self.assertEqual('Chief Engineer', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

    def test_tag_EMAIL(self):
        v = 'EMAIL;TYPE=INTERNET;TYPE=HOME;TYPE=pref:lanhel@mac.com\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('EMAIL', p.name)
        self.assertEqual('lanhel@mac.com', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(3, len(p.parameters))
        self.assertEqual(build_parameter('TYPE', 'INTERNET'), p.parameters[0])
        self.assertEqual(build_parameter('TYPE', 'HOME'), p.parameters[1])
        self.assertEqual(build_parameter('TYPE', 'pref'), p.parameters[2])

    def test_tag_TEL(self):
        v = 'TEL;TYPE=CELL;TYPE=VOICE;TYPE=pref:(801) 739-6929\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('TEL', p.name)
        self.assertEqual('(801) 739-6929', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(3, len(p.parameters))
        self.assertEqual(build_parameter('TYPE', 'CELL'), p.parameters[0])
        self.assertEqual(build_parameter('TYPE', 'VOICE'), p.parameters[1])
        self.assertEqual(build_parameter('TYPE', 'pref'), p.parameters[2])

    def test_tag_X_SOCIALPROFILE(self):
        v = 'X-SOCIALPROFILE;TYPE=twitter:http://twitter.com/lanhel\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('X-SOCIALPROFILE', p.name)
        self.assertEqual('http://twitter.com/lanhel', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(1, len(p.parameters))
        self.assertEqual(build_parameter('TYPE', 'twitter'), p.parameters[0])

    def test_tag_NOTE(self):
        v = 'NOTE:12T 438530 4463396\\nBSA\\nLNT Trainer\\nLNT Master Educator\\nLNT Mountain Bike Master Course (2009)\\nCivil Air Patrol\\n\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('NOTE', p.name)
        self.assertEqual('12T 438530 4463396\\nBSA\\nLNT Trainer\\nLNT Master Educator\\nLNT Mountain Bike Master Course (2009)\\nCivil Air Patrol\\n', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

    def test_tag_URL(self):
        v = 'URL;TYPE=WORK;TYPE=pref:http://flyingtitans.com\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('URL', p.name)
        self.assertEqual('http://flyingtitans.com', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(2, len(p.parameters))
        self.assertEqual(build_parameter('TYPE', 'WORK'), p.parameters[0])
        self.assertEqual(build_parameter('TYPE', 'pref'), p.parameters[1])

    def test_tag_BDAY(self):
        v = 'BDAY:1966-08-29\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('BDAY', p.name)
        self.assertEqual('1966-08-29', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

    def test_tag_PHOTO(self):
        v = 'PHOTO;ENCODING=b;TYPE=JPEG:/9j/4AAQSkZJR\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('PHOTO', p.name)
        self.assertEqual('/9j/4AAQSkZJR', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(2, len(p.parameters))
        self.assertEqual(build_parameter('ENCODING', 'b'), p.parameters[0])
        self.assertEqual(build_parameter('TYPE', 'JPEG'), p.parameters[1])

    def test_tag_CATEGORIES(self):
        v = 'CATEGORIES:com\,com.flyingtitans\,fam.helsten\,fam\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('CATEGORIES', p.name)
        self.assertEqual('com\,com.flyingtitans\,fam.helsten\,fam', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

    def test_tag_UID(self):
        v = 'UID:ba06e938-185e-4ab8-9922-f1d3845f9432\r\n'
        p = property_from_contentline(v)
        self.assertEqual(v, str(p))
        self.assertEqual('UID', p.name)
        self.assertEqual('ba06e938-185e-4ab8-9922-f1d3845f9432', p.value)
        self.assertIsNone(p.group)
        self.assertEqual(0, len(p.parameters))

