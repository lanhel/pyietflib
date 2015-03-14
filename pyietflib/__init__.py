#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""pyietflib is a collection of classes that will parse various IETF RFC
defined data streams into objects that may be used directly in Python,
and the written as fully compliant data streams.
"""
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
from .__meta__ import (__version__, __author__, __license__)


from .headers import *
from .generators import *


