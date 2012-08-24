#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`Content-Type <http://tools.ietf.org/html/rfc2045>`_"""
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
    raise Exception("Content-Type requires Python 3.2 or higher.")
import locale
import logging
import string
import re

__all__ = ['ContentType']

contenttag_re = re.compile(r'''^
    (?P<type>[-!#$%&'*+.0-9A-Z^_`a-z{|}~]+)
    /
    (?P<subtype>[-!#$%&'*+.0-9A-Z^_`a-z{|}~]+)
    (?P<parameters>(
            \s*;\s*[-!#$%&'*+.0-9A-Z^_`a-z{|}~]+
            \s*=\s*
            (([-!#$%&'*+.0-9A-Z^_`a-z{|}~]+)|("[!#-~]+"))
        )*)
    $''', flags=re.ASCII|re.VERBOSE)

tspecials_re = re.compile(r'''\(\)<>@,;:\/\[\]\?=''', flags=re.ASCII)

iana_types = {
    'text':['plain'],
    'image':['jpeg'],
    'audio':['basic'],
    'video':['mpeg'],
    'application':['octet-stream', 'postscript']
}


def iana_type(t):
    """Is the given type (`t`) a discrete IANA type defined in RFC 2045?"""
    return t in iana_types.keys()

def iana_subtype(t, st):
    """Is the given type (`st`) within (`t`) a defined subtype in
    RFC 2045?"""
    #TODO Build a registry that can contain all the IANA subtypes
    return st in iana_types.get(t, [])

ietf_token_re = re.compile(r'''^[-!#$&+.0-9A-Z^_a-z]+$''', flags=re.ASCII)

def ietf_type(t):
    """Is the given type (`t`) an IETF extension token defined in a
    standards track RFC and registered with IANA?"""
    return len(t) > 0 and len(t) < 128 and ietf_token_re.match(t) != None

def ietf_subtype(t, st):
    """Is the given subtype (`st`) within (`t`) an IETF extension token
    defined in a standards track RFC and registered with IANA?"""
    return len(st) > 0 and len(st) < 128 and ietf_token_re.match(st) != None

class ContentType(dict):
    """This will parse a `value` that conforms to the Content-Type
    header as defined in `RFC 2045 Multipurpose Internet Mail Extensions
    (MIME) Part One: Format of Internet Message Bodies
    <http://tools.ietf.org/html/rfc2045>`_, section 5.
    
    Content-Type parameters are accessed through dictionary mapping
    on this object.
    
    Notes
    -----
    1. This will use the entire string when parsing.
    
    2. If `value` is not a `str` then it will be converted to `str`
        using `ascii` decoding.
    
    3. This will validate all `type` and `subtype` pairs, but may be
        turned off by unsetting `validate` on creation.
    
    4. RFC 4288 has a more restrictive set of characters for a token
        which will be used for `type` and `subtype` this may be turned
        on by setting `rfc4288` on creation.
    
    5. Some `type` and `subtype` pairs have default parameters which
        will be set but will not be part of the string representation:
        for example "text/plain;charset=us-ascii" will be printed as
        "text/plain". This behavior may be turned off by setting
        `print_defaults` on object creation.
    
    Properties
    ----------
    type
        The `type` part of the header, for example `text`. When this is
        set the type will be validated, but the subtype will not be
        validated against the type so the combination may be invalid.
    
    type_iana
        The type is a discrete registered IANA type as defined in
        RFC 2045.
    
    type_ietf
        The type conforms to the IETF type extension token defined in
        standards track RFC and registered with IANA.
    
    type_private
        The type conforms to the private type extension where the name
        starts with `x-` or `X-`.

    subtype
        The `subtype` part of the header, for example `plain`.
    
    subtype_iana
        The subtype conforms to a publicly defined extension token as
        registered with IANA in accordance with RFC 2048.
    
    subtype_ietf
        The subtype conforms to the IETF subtype extension token defined
        in standards track RFC and registered with IANA.
    
    subtype_private
        The subtype conforms to the private subtype extension where the
        name starts with `x-` or `X-`.
    
    """
    def __init__(self, value=None, validate=True, rfc4288=False, print_defaults=False):
        self.validate = bool(validate)
        self.rfc4288 = bool(rfc4288)
        self.print_defaults = bool(print_defaults)
        self.type = 'application'
        self.subtype = 'octet-stream'
        
        if value:
            mo = contenttag_re.match(value)
            if not mo:
                raise ValueError("Invalid Content-Type header `{0}`".format(value))
            self.type = mo.group('type')
            self.subtype = mo.group('subtype')
            for parameter in mo.group('parameters').split(';'):
                parameter = parameter.strip()
                if parameter:
                    attr, value = parameter.split('=')
                    self[attr.strip().lower()] = value.strip().strip('"').lower()
        
        #Set any known defaults
        if self.type == 'text' and self.subtype == 'plain':
            if 'charset' not in self:
                self['charset'] = 'us-ascii'
        elif self.type == 'application' and self.subtype == 'octet-stream':
            if 'type' not in self:
                self['type'] = None
            if 'padding' not in self:
                self['padding'] = '8'
    
    def __eq__(self, o):
        return (isinstance(o, type(self)) and 
                self.type == o.type and
                self.subtype == o.subtype and
                dict(self) == dict(o))
        
    def __str__(self):
        params = ['']
        for a, v in self.items():
            if not self.print_defaults:
                if self.type == 'text' and self.subtype == 'plain':
                    if a == 'charset' and v == 'us-ascii':
                        continue
                elif self.type == 'application' and self.subtype == 'octet-stream':
                    if a == 'type' and v is None:
                        continue
                    elif a == 'padding' and v == '8':
                        continue

            if tspecials_re.search(v):
                v = '"{0}"'.format(v)
            params.append('{0}={1}'.format(a, v))
        return '{0}/{1}{2}'.format(self.type, self.subtype, ';'.join(params))
    
    def __repr__(self):
        raise NotImplementedError()
        return "ContentType('{0}')".format(str(self))
    
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        v = str(value).lower()
        iana = iana_type(v)
        ietf = self.rfc4288 and ietf_type(v)
        private = v.startswith('x-')
        if self.validate and not (iana or ietf or private):
            raise ValueError("Invalid Content-Type type value {0}.".format(value))
        self.__type = v
        self.__type_iana = iana
        self.__type_ietf = ietf
        self.__type_private = private
    
    @property
    def type_iana(self):
        return self.__type_iana
    
    @property
    def type_ietf(self):
        return self.__type_ietf
    
    @property
    def type_private(self):
        return self.__type_private
    
    @property
    def subtype(self):
        return self.__subtype
    
    @subtype.setter
    def subtype(self, value):
        v = str(value).lower()
        iana = iana_subtype(self.type, v)
        ietf = self.rfc4288 and ietf_subtype(self.type, v)
        private = v.startswith('x-')
        if self.validate and not (iana or ietf or private):
            raise ValueError("Invalid Content-Type subtype value {0}.".format(value))
        self.__subtype = v
        self.__subtype_iana = iana
        self.__subtype_ietf = ietf
        self.__subtype_private = private

    @property
    def subtype_iana(self):
        return self.__subtype_iana    
    
    @property
    def subtype_ietf(self):
        return self.__subtype_ietf
    
    @property
    def subtype_private(self):
        return self.__subtype_private
