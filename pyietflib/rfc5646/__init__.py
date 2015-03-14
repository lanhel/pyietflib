#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`RFC 5646 <http://tools.ietf.org/html/rfc5646>`_ Tags for Identifying
Languages parser.
"""
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
from .__meta__ import (__version__, __author__, __license__)

from .languagetag import *
from .registry import *

def accept_langauge_factory(value):
    raise NotImplementedError()

def content_language_factory(value):
    raise NotImplementedError()

from ..headers import register_header_parser
register_header_parser('accept-language', accept_langauge_factory)
register_header_parser('content-language', content_language_factory)


