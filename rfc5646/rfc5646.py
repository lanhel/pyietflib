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
import locale
import logging
import string
import re

from .registry import registry

__all__ = ['LanguageTag']

langtag = re.compile(r'''^
    (?P<language>
        ([a-zA-Z]{2,3}(?P<extlang>-([a-zA-Z]{3})|(-[a-zA-Z]{3}){0,2})?)|
        ([a-zA-Z]{4})|
        ([a-zA-Z]{5,8}))
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
    """This will parse a `value` that conforms to the language tag
    ABNF as defined in `RFC 5646 Tags for Identifying Languages
    <http://tools.ietf.org/html/rfc5646>`_, and will then `validate`
    the resulting parts against known accepted values.
    
    If `value` is `None` or an empty string then this will be initialized
    to `locale.getlocale()`.
    
    Notes
    -----
    1. This will only consider the first sequence of non-whitespace
        characters.
    
    2. If `value` is not a `str` then it will be converted to `str`
        using `ascii` decoding.
    
    Properties
    ----------
    language
        A 2 or 3 alpha character ISO 639 code, or a 4 alpha character
        reserved code, or a 5-8 alpha character registered language
        subtag.
    
    extlang
        A list of up to two 3 alpha character ISO 639 codes.
    
    script
        An ISO 15924 4 alpha character code.
    
    region
        Either ISO 3166-1 two alpha region code or an ISO 3166-1 three
        digit numeric code (identical to UN M.49 stated in RFC 5646).
    
    variants
        A list of strings of either 5-8 alphanumeric characters or a
        numeric character followed by 3 alphanumeric characters.
    
    extensions
        A list of strings of with the first being a singleton in the set
        (0-9, A-W, Y-Z, a-w, y-z) followed by one or more strings of
        2-8 alphanumeric characters.
    
    privateuse
        A list of strings of 1-8 alphanumeric characters. When output the
        singleton 'x-' will be prepended.
    """
    def __init__(self, value=None, validate=True):
        self.extlang = None
        self.script = None
        self.region = None
        self.variants = None
        self.extensions = None
        self.privateuse = None
        
        if not value:
            value = locale.getlocale()[0].replace('_', '-')
        
        if isinstance(value, str):
            value = value.lstrip()
            value = value.split()[0]
        elif isinstance(value, bytes) or isinstance(value, bytearray):
            value = value.lstrip()
            value = value.split()[0]
            value = value.decode(encoding='ascii')
        
        mo = langtag.match(value)
        if mo:
            self.type = 'langtag'
            
            if not mo.group('extlang'):
                self.language = mo.group('language')
            else:
                l = mo.group('language')
                e = mo.group('extlang')
                self.language = l.replace(e, '')
                self.extlang = e.strip('-').split('-')
            
            self.script = mo.group('script')
            
            self.region = mo.group('region')
            
            if mo.group('variants'):
                self.variants = mo.group('variants').strip('-').split('-')

            if mo.group('extensions'):
                def appendpart(l, part):
                    part = '-'.join(part)
                    if part:
                        l.append(part)                

                extensions = []
                parts = mo.group('extensions').split('-')
                part = []
                for p in parts:
                    if len(p) == 1:
                        appendpart(extensions, part)
                        part = [p]
                    else:
                        part.append(p)
                appendpart(extensions, part)
                self.extensions = extensions
            
            if mo.group('privateuse'):
                self.privateuse = mo.group('privateuse').strip('-').split('-')[1:]

        elif privateuse.match(value):
            self.type = 'private'
            self.__language = value
        elif value in irregular or value in regular:
            self.type = 'grandfathered'
            self.__language = value
        else:
            raise ValueError("Invalid LanguageTag `{0}`.".format(value))
    
    def __eq__(self):
        return False
        
    def __str__(self):
        if self.type == 'langtag':
            ret = [self.language]
            if self.extlang:
                ret.append('-'.join(self.extlang))
            if self.script:
                ret.append(self.script)
            if self.region:
                ret.append(self.region)
            if self.variants:
                ret.append('-'.join(self.variants))
            if self.extensions:
                ret.append('-'.join(self.extensions))
            if self.privateuse:
                ret.append('x-' + '-'.join(self.privateuse))
            return '-'.join(ret)
        else:
            return self.language

    def __repr__(self):
        return "LanguageTag('{0}')".format(str(self))
    
    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, value):
        if not value:
            raise ValueError("Language code cannot be empty.")
            
        value = str(value).lower()
        if not value.isalpha():
            raise ValueError("Invalid language code `{0}`.".format(value))

        if len(value) == 2 and valid_language_2(value):
            self.__language = value
        elif len(value) == 3 and valid_language_3(value):
            self.__language = value            
        elif len(value) == 4:
            self.__language = value
        elif len(value) in range(5,9):
            self.__language = value
        else:
            raise ValueError("Invalid language code `{0}`.".format(value))
    
    @property
    def extlang(self):
        return self.__extlang
    
    @extlang.setter
    def extlang(self, value):
        if not value:
            value = []
        elif not isinstance(value, (list, tuple)):
            value = [value]
        
        if len(value) > 2:
            raise ValueError("Maximum of two extended language codes allowed.")
        
        value = [str(v).lower() for v in value]
        for v in value:
            rentry = registry().extlangs.get(v)
            if not (v.isalpha() and len(v) == 3 and rentry):
                raise ValueError("Invalid extended language code `{0}`.".format(v))
            if self.language not in rentry.prefix:
                raise ValueError("Extended language `{0}` cannot extend language `{1}`.".format(v, self.language))
            
        self.__extlang = value
    
    @property
    def script(self):
        return self.__script
    
    @script.setter
    def script(self, value):
        if not value:
            self.__script = None
        else:
            value = str(value).title()
            if not (value.isalpha() and len(value) == 4 and valid_script(value)):
                raise ValueError("Invalid script code `{0}`.".format(value))
            self.__script = value
    
    @property
    def region(self):
        return self.__region
    
    @region.setter
    def region(self, value):
        if not value:
            self.__region = None
        else:
            value = str(value).upper()
            if len(value) == 2:
                if not valid_region_alpha(value):
                    raise ValueError("Invalid alpha region code `{0}`.".format(value))
            elif len(value) == 3:
                if not valid_region_numeric(value):
                    raise ValueError("Invalid numeric region code `{0}`.".format(value))
            else:
                raise ValueError("Invalid region code `{0}`.".format(value))
            self.__region = value
    
    @property
    def variants(self):
        return self.__variants
    
    @variants.setter
    def variants(self, value):
        if not value:
            self.__variants = []
            return
        
        if not isinstance(value, (list, tuple)):
            value = [value]
        
        value = [v.lower() for v in value]
        for v in value:
            if v[0].isnumeric() and len(v) == 4:
                continue
            if v.isalnum() and len(v) in range(5, 9) and valid_variant(v):
                continue
            raise ValueError("Invalid language variant code `{0}`.".format(v))
        
        if len(value) != len(set(value)):
            raise ValueError("Variant subtag used more than once: {0}".format(value))
        self.__variants = value
    
    @property
    def extensions(self):
        return self.__extensions
    
    @extensions.setter
    def extensions(self, value):
        if not value:
            self.__extensions = []
            return
            
        if not isinstance(value, (list, tuple)):
            value = [str(value)]
        
        value = [v.lower() for v in value]
        singletons = []
        for v in value:
            s, x = v.split('-')
            if not (s.isalnum() and s not in 'xX' and x.isalnum() and len(x) in range(2, 9)):
                raise ValueError("Invalid language extension code `{0}`.".format(v))
            if s in singletons:
                verr = '-'.join(value)
                raise ValueError("Duplicate extension singleton letter `{0}` in `{1}`.".format(s, verr))
            else:
                singletons.append(s)
        
        self.__extensions = value
    
    @property
    def privateuse(self):
        return self.__privateuse
    
    @privateuse.setter
    def privateuse(self, value):
        if not value:
            self.__privateuse = []
            return
            
        if not isinstance(value, (list, tuple)):
            value = [value]
        
        value = [v.lower() for v in value]
        for v in value:
            if v.isalnum() and len(v) in range(1, 9):
                continue
            raise ValueError("Invalid language privateuse code `{0}`.".format(v))
        self.__privateuse = value


###
### Language codes
###

def valid_language_2(code):
    """Is `code` a valid ISO 639-1 two character language code."""
    code = str(code)
    if len(code) != 2:
        return False
    return (registry().languages.get(code) != None)

def valid_language_3(code):
    """Is `code` a valid ISO 639-2 three character language code."""
    code = str(code)
    if len(code) != 3:
        return False
    if code[0] == 'q' and code[2] not in ['u', 'v', 'w', 'x', 'y', 'z']:
        return True
    return (registry().languages.get(code) != None)


###
### Script codes
###

def valid_script(code):
    code = str(code)
    return (registry().scripts.get(code) != None)


###
### Region (country) codes
###

iso3166_user = [
    'AA', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QU',
    'QV', 'QW', 'QX', 'QY', 'QZ', 'XA', 'XB', 'XC', 'XD', 'XE',
    'XF', 'XG', 'XH', 'XI', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XO', 
    'XP', 'XQ', 'XR', 'XS', 'XT', 'XU', 'XV', 'XW', 'XX', 'XY',
    'XZ', 'ZZ',
]

def valid_region_alpha(code):
    """Is `code` a valid ISO 3166-1 two character region code in the
    officially assigned or user assigned space. This will return
    `False` if code is in exceptionally, transitionally, and
    indeterminately reserved spaces, or is not used, or is unassigned.
    """
    code = str(code)
    if len(code) != 2:
        return False
    if code in iso3166_user:
        return True
    return (registry().regions.get(code) != None)


def valid_region_numeric(code):
    """Is `code` a valid ISO 3166-1 three character numeric region
    code in the officially assigned or user assigned space. This will return
    `False` if code is in exceptionally, transitionally, and
    indeterminately reserved spaces, or is not used, or is unassigned.
    """
    code = str(code)
    if len(code) != 3:
        return False
    return (registry().regions.get(code) != None)


###
### Variant codes
###

def valid_variant(code):
    code = str(code)
    return (registry().variants.get(code) != None)


