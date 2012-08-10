#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`Language Tag <http://tools.ietf.org/html/rfc5646>`_"""
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
    raise Exception("Language-Tag requires Python 3.2 or higher.")
import logging
import string
import re

__all__ = ['LanguageTag']
__log__ = logging.getLogger(__name__)

langtag = re.compile(r'''^
    (?P<language>[a-zA-Z]{2,3})
    (-(?P<script>[a-zA-Z]{4}))?
    (-(?P<region>([a-zA-Z]{2})|([0-9]{3})))?
    (?P<variants>(-(([a-zA-Z0-9]{5,8})|([0-9][a-zA-Z0-9]{3})))*)?
    (?P<extensions>(-[0-9A-WY-Za-wy-z](-[a-zA-Z0-9]{2,8})+)*)?
    (-(?P<privateuse>[xX](-[a-zA-Z0-9]{1,8})+))?
    $''', flags=re.ASCII|re.VERBOSE)

privateuse = re.compile(r'''[xX](-[a-zA-Z0-9]{1,8})+''', flags=re.VERBOSE)

irregular = ["en-GB-oed",
    "i-ami", "i-bnn", "i-default", "i-enochian", "i-hak", "i-klingon",
    "i-lux", "i-mingo", "i-navajo", "i-pwn", "i-tao", "i-tay", "i-tsu",
    "sgn-BE-FR", "sgn-BE-NL", "sgn-CH-DE"]

regular = ["art-lojban", "cel-gaulish", "no-bok", "no-nyn", "zh-guoyu",
    "zh-hakka", "zh-min", "zh-min-nan", "zh-xiang"]


class LanguageTag():
    """A language tag as defined in `RFC 5646 Tags for Identifying
    Languages <http://tools.ietf.org/html/rfc5646>`_
    
    Parameter
    ---------
    value
        A string to parse for the `Language-Tag`.
    """
    def __init__(self, value):
        mo = langtag.match(value)
        if mo:
            self.type = 'langtag'
            self.language = mo.group('language')
            self.script = mo.group('script')
            self.region = mo.group('region')
            self.variants = []
            if mo.group('variants'):
                self.variants = mo.group('variants').strip('-').split('-')
                if len(self.variants) != len(set(self.variants)):
                    raise ValueError("Variant subtag used more than once: {0}".format(self.variants))
            self.extensions = []
            if mo.group('extensions'):
                def appendpart(l, part):
                    part = '-'.join(part)
                    if part:
                        l.append(part)                
                parts = mo.group('extensions').split('-')
                part = []
                for p in parts:
                    if len(p) == 1:
                        appendpart(self.extensions, part)
                        part = [p]
                    else:
                        part.append(p)
                appendpart(self.extensions, part)
            self.privateuse = mo.group('privateuse')
        elif privateuse.match(value):
            self.type = 'private'
            self.language = value
        elif value in irregular or value in regular:
            self.type = 'grandfathered'
            self.language = value
        else:
            raise ValueError("Invalid LanguageTag `{0}`.".format(value))
    
    def __eq__(self):
        return False
        
    def __str__(self):
        if self.type == 'langtag':
            ret = [self.language]
            if self.script:
                ret.append(self.script)
            if self.region:
                ret.append(self.region)
            if self.variants:
                ret.append('-'.join(self.variants))
            if self.extensions:
                ret.append('-'.join(self.extensions))
            if self.privateuse:
                ret.append(self.privateuse)
            return '-'.join(ret)
        else:
            return self.language

    def __repr__(self):
        return "LanguageTag('{0}')".format(str(self))


