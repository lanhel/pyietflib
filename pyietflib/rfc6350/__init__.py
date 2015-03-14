#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`vCard <http://tools.ietf.org/html/rfc6350>`_ parser to convert a
vCard representation to a structured object of a vCard, and to create
a vCard representation from the structured object.


media-types
-----------
- text/vcard;version=4.0;charset=UTF-8
- text/vcard;version=3.0;charset=UTF-8


File Extension
--------------
- .vcf
- .vcard
"""
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
from .__meta__ import (__version__, __author__, __license__)

from .vcard import *
from .property import *
from .parameter import *

def generator_factory(stream):
    return 'spam'

from ..generators import register_type_generator
register_type_generator('text/vcard', generator_factory)



