#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Collection of all pyietflib generator creation methods."""
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
import types

__all__ = ['register_type_generator', 'media_type_generator']

mediatype_modules = {
    'text/vcard':'rfc6350'
}

registered_media_types = {
}


def register_type_generator(mediatype, generator_factory):
    """Register a new media-type generator factory for `media_type_generator`
    to construct a generator attached to a stream."""
    if mediatype in registered_media_types:
        raise KeyError("The media-type {0} is already registered.".format(mediatype))
    registered_media_types[mediatype.lower()] = generator_factory
    register_module_for_media_type(mediatype.lower(), generator_factory.__module__)

def register_module_for_media_type(mediatype, module):
    mname = mediatype_modules[mediatype]
    for k, v in mediatype_modules.items():
        if v == mname:
            mediatype_modules[k] = module
    assert mediatype_modules[mediatype] == module

def load_module_for_media_type(mediatype, globals, locals):
    """If the module for the `mediatype` is not loaded then load it and
    return a reference to it."""
    if mediatype.lower() not in mediatype_modules:
        raise KeyError("Unknown builtin mediatype `{0}` for pyietflib.".format(mediatype))
    mediatype = mediatype.lower()
    if not isinstance(mediatype_modules[mediatype], types.ModuleType):
        m = __import__(mediatype_modules[mediatype], globals=globals, locals=locals)
        register_module_for_media_type(mediatype, m)
    return mediatype_modules[mediatype]

def media_type_generator(mediatype, stream):
    """Return a generator that will parse the `stream` and return the top
    level media-type objects. For example if the stream is an RFC 6350
    vCard stream then this will yield a `pyietflib.rfc6350.vCard` object
    each time the generator is called.
    
    Generally the stream should be a byte stream to allow the generator
    itself to determine how to process it based on the given media-type.
    For instance all RFC 6350 streams must be UTF-8 encoded (see RFC 6350
    §3.1) so the stream will be decoded and unfolded automatically by
    the generator.
    """
    mediatype = mediatype.lower()
    if mediatype not in registered_media_types:
        load_module_for_media_type(mediatype, globals(), locals())
    return registered_media_types[mediatype](stream)
    







