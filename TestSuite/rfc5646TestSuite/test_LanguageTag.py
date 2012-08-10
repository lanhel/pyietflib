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

from rfc5646 import *

class TestLanguageTag(unittest.TestCase):

    def test_language(self):
        """Make a simple language tag with only the language element."""
        x = LanguageTag("en")
        self.assertEqual("en", x.language)
        self.assertEqual("en", str(x))
        self.assertEqual("LanguageTag('en')", repr(x))

    def test_complex(self):
        """Make a complex language tax with all elments."""
        tag = "en-Latn-US-abcde-abcdef-abcdefg-abcdefgh-1aaa-1901-a-e1-b-e1234567-x-1"
        x = LanguageTag(tag)
        self.assertEqual("en", x.language)
        self.assertEqual("Latn", x.script)
        self.assertEqual("US", x.region)
        self.assertEqual(['abcde', 'abcdef', 'abcdefg', 'abcdefgh', '1aaa', '1901'], x.variants)
        self.assertEqual(['a-e1', 'b-e1234567'], x.extensions)
        self.assertEqual("x-1", x.privateuse)
        self.assertEqual(tag, str(x))
        self.assertEqual("LanguageTag('{0}')".format(tag), repr(x))

