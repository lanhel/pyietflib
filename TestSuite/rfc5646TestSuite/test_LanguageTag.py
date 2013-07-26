#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""RFC5646 Unit Test."""
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
import locale
import unittest

from pyietflib.rfc5646 import *

class TestLanguageTag(unittest.TestCase):
    
    def test_default(self):
        lang, region = locale.getlocale()[0].split('_')
        code = "{0}-{1}".format(lang, region)
        x = LanguageTag()
        self.assertEqual(lang, x.language)
        self.assertIsNone(x.script)
        self.assertEqual(region, x.region)
        self.assertEqual([], x.variants)
        self.assertEqual([], x.extensions)
        self.assertEqual([], x.privateuse)
        self.assertEqual(code, str(x))
        self.assertEqual("LanguageTag('{0}')".format(code), repr(x))

    def test_simple(self):
        """Make a simple language tag with only the language element."""
        x = LanguageTag("en")
        self.assertEqual("en", x.language)
        self.assertIsNone(x.script)
        self.assertIsNone(x.region)
        self.assertEqual([], x.variants)
        self.assertEqual([], x.extensions)
        self.assertEqual([], x.privateuse)
        self.assertEqual("en", str(x))
        self.assertEqual("LanguageTag('en')", repr(x))

        x = LanguageTag("YuE")
        self.assertEqual("yue", x.language)
        self.assertEqual("yue", str(x))
        self.assertEqual("LanguageTag('yue')", repr(x))
    
    def test_grandfathered(self):
        """Test a grandfathered language tag."""
        x = LanguageTag("i-enochian")
        self.assertEqual("i-enochian", x.language)
        self.assertEqual("i-enochian", str(x))
        self.assertEqual("LanguageTag('i-enochian')", repr(x))
    
    def test_extended(self):
        x = LanguageTag("ZH-CMN-hANS-cn")
        self.assertEqual("zh", x.language)
        self.assertEqual("Hans", x.script)
        self.assertEqual("CN", x.region)
        self.assertEqual("zh-cmn-Hans-CN", str(x))
        self.assertEqual("LanguageTag('zh-cmn-Hans-CN')", repr(x))
    
    def test_script(self):
        """Test a language subtag with script subtag."""
        x = LanguageTag("ZH-hANT")
        self.assertEqual("zh", x.language)
        self.assertEqual("Hant", x.script)
        self.assertEqual("zh-Hant", str(x))
        self.assertEqual("LanguageTag('zh-Hant')", repr(x))
    
    def test_region(self):
        """Test a language with a script and region subtags."""
        x = LanguageTag("de-de")
        self.assertEqual("de", x.language)
        self.assertEqual("DE", x.region)
        self.assertEqual("de-DE", str(x))
        self.assertEqual("LanguageTag('de-DE')", repr(x))

        x = LanguageTag("es-419")
        self.assertEqual("es", x.language)
        self.assertEqual("419", x.region)
        self.assertEqual("es-419", str(x))
        self.assertEqual("LanguageTag('es-419')", repr(x))
    
    def test_script_region(self):
        """Test a language with region subtag."""
        x = LanguageTag("sr-Latn-rs")
        self.assertEqual("sr", x.language)
        self.assertEqual("Latn", x.script)
        self.assertEqual("RS", x.region)
        self.assertEqual("sr-Latn-RS", str(x))
        self.assertEqual("LanguageTag('sr-Latn-RS')", repr(x))
    
    def test_variant(self):
        """Test a language with a langauge variant."""
        x = LanguageTag("sl-ROZAJ-BISKE")
        self.assertEqual("sl", x.language)
        self.assertEqual(['rozaj', 'biske'], x.variants)
        self.assertEqual("sl-rozaj-biske", str(x))
        self.assertEqual("LanguageTag('sl-rozaj-biske')", repr(x))
    
    def test_region_variant(self):
        """Test a language with a region and langauge variant."""
        x = LanguageTag("de-CH-1901")
        self.assertEqual("de", x.language)
        self.assertEqual("CH", x.region)
        self.assertEqual(['1901'], x.variants)
        self.assertEqual("de-CH-1901", str(x))
        self.assertEqual("LanguageTag('de-CH-1901')", repr(x))

        x = LanguageTag("sl-IT-NeDiS")
        self.assertEqual("sl", x.language)
        self.assertEqual("IT", x.region)
        self.assertEqual(['nedis'], x.variants)
        self.assertEqual("sl-IT-nedis", str(x))
        self.assertEqual("LanguageTag('sl-IT-nedis')", repr(x))
    
    def test_script_region_variant(self):
        """Test a language with a script, region, and langauge variant."""
        x = LanguageTag("hy-Latn-IT-arevela")
        self.assertEqual("hy", x.language)
        self.assertEqual("Latn", x.script)
        self.assertEqual("IT", x.region)
        self.assertEqual(['arevela'], x.variants)
        self.assertEqual("hy-Latn-IT-arevela", str(x))
        self.assertEqual("LanguageTag('hy-Latn-IT-arevela')", repr(x))
    
    def test_extension(self):
        """Test a language with a langauge extension."""
        x = LanguageTag("en-US-u-isLaMcal")
        self.assertEqual("en", x.language)
        self.assertEqual("US", x.region)
        self.assertEqual(['u-islamcal'], x.extensions)
        self.assertEqual("en-US-u-islamcal", str(x))
        self.assertEqual("LanguageTag('en-US-u-islamcal')", repr(x))
        
        x = LanguageTag("zh-CN-a-myext-x-private")
        self.assertEqual("zh", x.language)
        self.assertEqual("CN", x.region)
        self.assertEqual(['a-myext'], x.extensions)
        self.assertEqual(["private"], x.privateuse)
        self.assertEqual("zh-CN-a-myext-x-private", str(x))
        self.assertEqual("LanguageTag('zh-CN-a-myext-x-private')", repr(x))
        
        x = LanguageTag("en-a-myext-b-another")
        self.assertEqual("en", x.language)
        self.assertEqual(['a-myext', 'b-another'], x.extensions)
        self.assertEqual("en-a-myext-b-another", str(x))
        self.assertEqual("LanguageTag('en-a-myext-b-another')", repr(x))
    
    def test_privateuse(self):
        """Test a private use tag."""
        x = LanguageTag("de-CH-x-pHonEbk")
        self.assertEqual("de", x.language)
        self.assertEqual("CH", x.region)
        self.assertEqual(["phonebk"], x.privateuse)
        self.assertEqual("de-CH-x-phonebk", str(x))
        self.assertEqual("LanguageTag('de-CH-x-phonebk')", repr(x))
        
        x = LanguageTag("az-Arab-x-AZE-derbend")
        self.assertEqual("az", x.language)
        self.assertEqual("Arab", x.script)
        self.assertEqual(["aze", "derbend"], x.privateuse)
        self.assertEqual("az-Arab-x-aze-derbend", str(x))
        self.assertEqual("LanguageTag('az-Arab-x-aze-derbend')", repr(x))
    
    def test_privateuse_registry(self):
        """Test a private use registry tag."""
        x = LanguageTag("x-whatever")
        self.assertEqual("x-whatever", x.language)
        self.assertIsNone(x.script)
        self.assertIsNone(x.region)
        self.assertEqual([], x.variants)
        self.assertEqual([], x.extensions)
        self.assertEqual([], x.privateuse)
        self.assertEqual("x-whatever", str(x))
        self.assertEqual("LanguageTag('x-whatever')", repr(x))
        
    def test_complex(self):
        """Make a complex language tax with all elments."""
        tag = "en-Latn-US-1694acad-1994-baku1926-1aaa-a-e1-b-e1234567-x-1-abcd-a321bfrc"
        x = LanguageTag(tag)
        self.assertEqual("en", x.language)
        self.assertEqual("Latn", x.script)
        self.assertEqual("US", x.region)
        self.assertEqual(['1694acad', '1994', 'baku1926', '1aaa'], x.variants)
        self.assertEqual(['a-e1', 'b-e1234567'], x.extensions)
        self.assertEqual(["1", "abcd", "a321bfrc"], x.privateuse)
        self.assertEqual(tag, str(x))
        self.assertEqual("LanguageTag('{0}')".format(tag), repr(x))
    
    def test_invalid_tworegions(self):
        self.assertRaises(ValueError, LanguageTag, 'de-419-DE')
        self.assertRaises(ValueError, LanguageTag, 'a-DE')
        self.assertRaises(ValueError, LanguageTag, 'ar-a-aaa-b-bbb-a-ccc')
        self.assertRaises(ValueError, LanguageTag, 'tlh-a-b-foo')

    def test_grandfathered_regular(self):
        x = LanguageTag('art-lojban')
