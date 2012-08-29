#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Collection of all pyietflib header parsing methods."""
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







