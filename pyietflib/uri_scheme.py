#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Collection of all pyietflib URI parsing methods."""
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

__all__ = ['register_uri_parser', 'parse_uri']

scheme_modules = {
    'geo':'rfc5870'
}

registered_schemes = {
}


def register_uri_scheme_parser(scheme, parser):
    """Register a new URI `scheme` parser."""
    scheme = scheme.lower()
    if scheme in registered_schemes:
        raise KeyError("The scheme {0} is already registered.".format(scheme))
    registered_schemes[scheme.lower()] = parser
    register_module_for_uri_scheme(scheme.lower(), parser.__module__)

def register_module_for_uri_scheme(scheme, module):
    mname = scheme_modules[scheme]
    for k, v in scheme_modules.items():
        if v == mname:
            scheme_modules[k] = module
    assert scheme_modules[scheme] == module

def load_module_for_uri_scheme(scheme, globals, locals):
    """If the module for the URI `scheme` is not loaded then load it and
    return a reference to it."""
    if scheme.lower() not in scheme_modules:
        raise KeyError("Unknown builtin URI scheme `{0}` for pyietflib.".format(scheme))
    scheme = scheme.lower()
    if not isinstance(scheme_modules[scheme], types.ModuleType):
        m = __import__(scheme_modules[scheme], globals=globals, locals=locals)
        register_module_for_uri_scheme(scheme, m)
    return scheme_modules[scheme]

def parse_uri_scheme(scheme, value):
    """Contextually parse `value` based on URI `scheme` desired and return
    the appropriate object."""
    scheme = scheme.lower()
    if scheme not in registered_schemes:
        load_module_for_scheme(scheme, globals(), locals())
    return registered_schemes[scheme](value)







