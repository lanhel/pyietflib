#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`RFC 5646 IANA Language Subtag Registry
<http://tools.ietf.org/html/rfc5646#section-3>`_ reader."""
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
    raise Exception("Language-Tag requires Python 3.2 or higher.")
import os
import logging
import re
from datetime import datetime

__all__ = ['registry', 'LanguageRegistry', 'LanguageRegistryRecord']


class LanguageRegistry():
    """Contains all of the valid language subtags from the registry
    file at `path` with the format defined by `IANA Language Subtag
    Registry <http://tools.ietf.org/html/rfc5646#section-3>`_.
    """
    def __init__(self, path):
        self.languages = {}
        self.extlangs = {}
        self.scripts = {}
        self.regions = {}
        self.variants = {}
        self.grandfathered = {}
        self.redundant = {}
        
        stream = open(path, encoding='UTF-8')
        line = stream.readline()
        while line and line.rstrip() != '%%':
            name, body = line.split(':')
            name = name.strip()
            body = body.strip()
            setattr(self, name, body)
            line = stream.readline()

        lines = []
        line = stream.readline()
        while line:
            if line.rstrip() == '%%':
                self.__addrecord(LanguageRegistryRecord(lines))
                lines = []
            elif line[0].isspace():
                lines[-1] = lines[-1] + line.strip()
            else:
                lines.append(line.strip())
            line = stream.readline()
        self.__addrecord(LanguageRegistryRecord(lines))
    
    def __addrecord(self, record):
        try:
            if record.type == 'language':
                self.languages[record.subtag] = record
            elif record.type == 'extlang':
                self.extlangs[record.subtag] = record
            elif record.type == 'script':
                self.scripts[record.subtag] = record
            elif record.type == 'region':
                self.regions[record.subtag] = record
            elif record.type == 'variant':
                self.variants[record.subtag] = record
            elif record.type == 'grandfathered':
                self.grandfathered[record.tag] = record
            elif record.type == 'redundant':
                self.redundant[record.tag] = record
            else:
                logging.warning("Unknown language subtag registry type %s.", record.subtag)
        except AttributeError as err:
            logging.exception("Invalid language registry record for %s, %s.", record.type, record.description)

class LanguageRegistryRecord():
    """Contains a single record for an IANA Language Subtag Registry
    which may be parsed from list of `lines`."""
    
    field_re = re.compile(r'''^
            (?P<fieldname>[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9])
            \s*:\s*
            (?P<fieldbody>.+)
        $''', flags=re.VERBOSE)
    
    def __init__(self, lines):
        for line in lines:
            mo = LanguageRegistryRecord.field_re.match(line)
            if not mo:
                raise ValueError("Unable to parse language registry field `{0}`.".format(line))
            name = mo.group('fieldname').strip()
            body = mo.group('fieldbody').strip()
            if not body.isprintable():
                raise ValueError("Langauge registry field `{0}` body contains unprintable characters".format(line, linenumber))
            
            if name == 'Type':
                self.type = body
            elif name == 'Subtag':
                self.subtag = body
            elif name == 'Tag':
                self.tag = body
            elif name == 'Description':
                self.description = body
            elif name == 'Added':
                try:
                    self.added = datetime.strptime(body, '%Y-%m-%d')
                except ValueError as err:
                    raise ValueError("Langauge registry added field `{0}` date is not ISO 8601 date.".format(line))
            
            elif name == 'Deprecated':
                try:
                    self.deprecated = datetime.strptime(body, '%Y-%m-%d')
                except ValueError as err:
                    raise ValueError("Langauge registry deprecated field `{0}` date is not ISO 8601 date.".format(line))
            
            elif name == 'Suppress-Script':     # language type
                self.suppress_script = body
            
            elif name == 'Macrolanguage':       # language type
                self.macro_language = body
            
            elif name == 'Scope':               # language type
                self.scope = body
            
            elif name == 'Prefix':              # variant type
                if not hasattr(self, 'prefix'):
                    self.prefix = []
                self.prefix.append(body)
                
            elif name == 'Comments':            # variant type
                self.comments = body
            
            elif name == 'Preferred-Value':     # grandfathered type
                self.preferred_value = body
            
            else:
                print('field', name)
                logging.warning("Unknown field name %s.", name)


default_registry = None

def registry():
    '''Load the default registry that is part of the RFC 5646 package.'''
    global default_registry
    if not default_registry:
        path = os.path.join(os.path.dirname(__file__), 'language-subtag-registry.txt')
        default_registry = LanguageRegistry(path)
    return default_registry
    