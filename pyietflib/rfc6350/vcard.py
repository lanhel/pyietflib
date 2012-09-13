#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`vCard <http://tools.ietf.org/html/rfc6350>`_ object that contains
the information in structured form."""
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
    raise Exception("rfc6350 requires Python 3.2 or higher.")
import logging
import re
import string

from .property import *
from .parameter import *
import pyietflib.iso8601

__all__ = ['parse_vcard', 'vCard']
__log__ = logging.getLogger('rfc6350')



def parse_vcard(stream):
    """Given a binary `stream` that is UTF-8 encoded and RFC 6350
    folded parse and return a single vCard from that stream."""
    state = 'start'
    vcard = None
    contentline_parser = None
    for line, linenum in contentline_generator(stream):
        if state == 'content':
            if re.match('^END:VCARD\r\n$', line):
                state = 'end'
                contentline_parser = None
                vcard.validate()
                return vcard
            else:
                assert contentline_parser
                prop = contentline_parser(line, linenum)
                if prop.name not in vcard:
                    vcard[prop.name] = []
                vcard[prop.name].append(prop)
        
        elif state == 'start':
            if not re.match('^BEGIN:VCARD\r\n$', line):
                raise ValueError('Invalid vCard BEGIN content-line[{0}]: "{1:.30s}...".'.format(linenum, line))
            state = 'version'
            continue
        
        elif state == 'version':
            mo = re.match(r'^VERSION:(?P<version>.+)\r\n$', line)
            if not mo:
                raise ValueError('Invalid vCard VERSION content-line[{0}]: "{1:.30s}...".'.format(linenum, line))
            state = 'content'
            version = mo.group('version')
            if version == '4.0':
                vcard = vCard()
                contentline_parser = property_from_contentline
            else:
                raise ValueError('Invalid or unknown vCard version {0} on line {1}: "{2:.30s}...".'.format(version, linenum, line))
    raise ValueError('Invalid vCard stream END contentline not found before EOF.')



def contentline_generator(stream):
    """Generate unfolded and decoded content lines from the stream."""
    linenum = 0
    try:
        unfold = None
        unfoldline = 0
        for line in stream:
            linenum = linenum + 1
            if line[-2:] != b'\r\n':
                raise ValueError('Invalid line ending on line {0}: "{1:.30s}...".'.format(linenum, line))
            line = line[:-2]
            if not line[:-2]:
                continue
            
            if line[0] in b' \t':
                if not unfold:
                    raise ValueError('Invalid line folding on line {0}: "{1:.30s}...".'.format(linenum, line))
                while line[0] in b' \t':
                    line = line[1:]
                unfold.extend(line)
            elif not unfold:
                unfold = bytearray(line)
                unfoldline = linenum
            else:
                unfold.extend(b'\r\n')
                yield (unfold.decode("UTF-8"), unfoldline)
                unfold = bytearray(line)
                unfoldline = linenum
        else:
            if unfold:
                unfold.extend(b'\r\n')
                yield (unfold.decode("UTF-8"), unfoldline)
    except UnicodeDecodeError as err:
        print(line)
        raise ValueError('Invalid UTF-8 encoded stream on line {0}: "{1:.30s}...".'.format(linenum, line))



class vCard(dict):
    """Defines a structured vCard in accordance with `RFC 6350: vCard
    Format Specification <http://tools.ietf.org/html/rfc6350>`_
    that defines version 4 vCard.
    """
    def __init__(self, version='4.0'):
        self.version = version
    
    def __str__(self):
        raise NotImplementedError()
    
    def __repr__(self):
        return 'parse_vcard(r"""{0}""")'.format(str(self))

    def validate(self):
        """Check that the vCard is valid IAW RFC 6350."""
        if len(self) == 0:
            raise ValueError("Invalid vCard: a property is required.")


