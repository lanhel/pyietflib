#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`RFC 5870 <http://tools.ietf.org/html/rfc5870>`_ A Uniform Resource
Identifier for Geographic Locations ('geo' URI).
"""
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
from .__meta__ import (__version__, __author__, __license__)

from .geouri import *


def geo_uri_parser_factory(value):
    raise NotImplementedError()

from ..uri_scheme import register_uri_scheme_parser
register_uri_scheme_parser('geo', geo_uri_parser_factory)


