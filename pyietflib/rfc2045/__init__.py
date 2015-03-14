#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`RFC 2045 <http://tools.ietf.org/html/rfc2045>`_ Multipurpose Internet
Mail Extensions (MIME) Part One: Format of Internet Message Bodies headers
parsering and validation.
"""
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
from .__meta__ import (__version__, __author__, __license__)

from .contenttype import *

def parser_factory(value):
    return 'spam'

from ..headers import register_header_parser
register_header_parser('Content-Type', parser_factory)


