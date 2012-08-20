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
import io
import unittest

from rfc5646 import *

class TestLanguageRegistry(unittest.TestCase):
    
    def test_record_language(self):
        text = [
            'Type: language',
            'Subtag: en',
            'Description: English',
            'Added: 2005-10-16',
            'Suppress-Script: Latn']
        x = LanguageRegistryRecord(text)
    
    
    def test_read_registry(self):
        r = registry()
        self.assertEqual('Aragonese', r.languages['an'].description)
        self.assertEqual('Mesopotamian Arabic', r.extlangs['acm'].description)
        self.assertEqual('Antigua and Barbuda', r.regions['AG'].description)
        self.assertEqual('Traditional German orthography', r.variants['1901'].description)
        self.assertEqual('English, Oxford English Dictionary spelling', r.grandfathered['en-GB-oed'].description)
        self.assertEqual('Azerbaijani in Latin script', r.redundant['az-Latn'].description)


