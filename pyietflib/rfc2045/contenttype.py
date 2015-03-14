#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`Content-Type <http://tools.ietf.org/html/rfc2045>`_"""
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
from .__meta__ import (__version__, __author__, __license__)

import sys
if sys.version_info < (3, 2):
    raise Exception("rfc2045 requires Python 3.2 or higher.")
import locale
import logging
import string
import re

from .contenttype_iana import *

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

token_re = re.compile(r'''^[-!#$%&'*+.0-9A-Z^_`a-z{|}~]+$''', flags=re.ASCII)

quoted_re = re.compile(r'''^[!#-~]+$''', flags=re.ASCII)

ietf_token_re = re.compile(r'''^[-!#$&+.0-9A-Z^_a-z]+$''', flags=re.ASCII)

private_token_re = re.compile(r'''^x-[-!#$%&'*+.0-9A-Z^_`a-z{|}~]+$''', flags=re.ASCII)

parameter_re = re.compile(r'''
        \s*;\s*
        (?P<attribute>[-!#$%&'*+.0-9A-Z^_`a-z{|}~]+)
        \s*=\s*
        (?P<value>([-!#$%&'*+.0-9A-Z^_`a-z{|}~]+)|("[!#-~]+"))
    ''', flags=re.ASCII|re.VERBOSE)

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

            parameters = mo.group('parameters')
            mo = parameter_re.search(parameters)
            while mo:
                attr = mo.group('attribute').lower()
                value = mo.group('value').lower().strip('"')
                self[attr] = value
                mo = parameter_re.search(parameters, mo.end())

        for k, v in iana_default_parameters(self.type, self.subtype).items():
            if k not in self:
                self[k] = v

    def __eq__(self, o):
        if isinstance(o, type(self)):
            return (self.type == o.type and
                self.subtype == o.subtype and
                dict(self) == dict(o))
        return NotImplemented

    def __str__(self):
        defaults = iana_default_parameters(self.type, self.subtype)
        params = ['']
        for a, v in self.items():
            if not self.print_defaults and a in defaults and v == defaults[a]:
                continue
            if v is None:
                continue
            if not token_re.match(v):
                v = '"{0}"'.format(v)
            params.append('{0}={1}'.format(a, v))
        return '{0}/{1}{2}'.format(self.type, self.subtype, ';'.join(params))

    def __repr__(self):
        return "ContentType('{0}')".format(str(self))

    def __setitem__(self, key, value):
        key = str(key)
        if not token_re.match(key):
            raise ValueError("Invalid Content-Type parameter attribute `{0}`.".format(key))
        if value is not None:
            value = str(value)
            if not quoted_re.match(value):
                raise ValueError("Invalid Content-Type parameter value `{0}`.".format(value))
        super().__setitem__(key, value)

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        v = str(value).lower()
        iana = iana_type(v)
        ietf = self.rfc4288 and ietf_type(v)
        private = (private_token_re.match(v) is not None)
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
        private = (private_token_re.match(v) is not None)
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
