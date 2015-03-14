#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Collection of all pyietflib header parsing methods."""
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
from .__meta__ import (__version__, __author__, __license__)

import sys
if sys.version_info < (3, 2):
    raise Exception("pyietflib requires Python 3.2 or higher.")

__all__ = ['register_header_parser', 'parse_header']

header_modules = {
    'content-type':'rfc2045',
    'accept-language':'rfc5646',
    'content-language':'rfc5646'
}

registered_headers = {
}


def register_header_parser(header, parser):
    """Register a new header parser."""
    header = header.lower()
    if header in registered_headers:
        raise KeyError("The header {0} is already registered.".format(header))
    registered_headers[header.lower()] = parser
    register_module_for_header(header.lower(), parser.__module__)

def register_module_for_header(header, module):
    mname = header_modules[header]
    for k, v in header_modules.items():
        if v == mname:
            header_modules[k] = module
    assert header_modules[header] == module

def load_module_for_header(header, globals, locals):
    """If the module for the `header` is not loaded then load it and
    return a reference to it."""
    if header.lower() not in header_modules:
        raise KeyError("Unknown builtin header `{0}` for pyietflib.".format(header))
    header = header.lower()
    if not isinstance(header_modules[header], types.ModuleType):
        m = __import__(header_modules[header], globals=globals, locals=locals)
        register_module_for_header(header.lower(), m)
    return header_modules[header]

def parse_header(header, value):
    """Contextually parse `value` based on `header` desired and return
    the appropriate object."""
    header = header.lower()
    if header not in registered_headers:
        load_module_for_header(header, globals(), locals())
    return registered_headers[header](value)







