#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""IANA registered Content-Type type and subtype values."""
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
    raise Exception("rfc2045 requires Python 3.2 or higher.")
import locale
import logging
import string
import re

__all__ = ['iana_type', 'iana_subtype', 'iana_default_parameters']

#
# The text file that contains all the IANA registered types and subtypes
# with each pair containing zero or more named lists of parameters.
# - "defaults" is a dictionary of parameters and default values.
# - "mandatory" is a list of parameters that must exist when parsing.
# - "optional" is a list of parameters that may be used with the type/subtype.
#

iana_types = {
    'text':{
        'plain':{"defaults":[("charset", "us-ascii")]}
    },
    'image':{
        'jpeg':{}
    },
    'audio':{
        'basic':{}
    },
    'video':{
        'mpeg':{}
    },
    'application':{
        'octet-stream':{"defaults":[("type", None), ("padding", '8')]},
        'postscript':{}
    }
}

def iana_type(t):
    """Is the given type (`t`) a discrete IANA type defined in RFC 2045?"""
    return t in iana_types.keys()

def iana_subtype(t, st):
    """Is the given type (`st`) within (`t`) a defined subtype in
    RFC 2045?"""
    #TODO Build a registry that can contain all the IANA subtypes
    return st in iana_types.get(t, {}).keys()

def iana_default_parameters(t, st):
    """Return a dictionary of default parameters for the given type
    and subtype."""
    t_st = iana_types.get(t, {}).get(st, {}).get("defaults", [])
    t_st = dict(t_st)
    return t_st

class ContentTypeIANA():
    """This defines a top level IANA Content-Type type value."""
    pass

