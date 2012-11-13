#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Package that will handle `ISO 8601:2004 Representation of dates and
times <http://www.iso.org/iso/catalogue_detail?csnumber=40874>`_ parsing
and formatting.
"""
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

from .time import *
from .date import *
from .datetime import *
#from .duration import *
#from .recurring import *

__all__ = ['isodate', 'isotime', 'isodatetime',
        'CALENDAR', 'ORDINAL', 'WEEK',
        'CENTURY', 'DECADE', 'YEAR', 'MONTH', 'DAYOFMONTH', 'DAYOFYEAR',
        'WEEKOFYEAR', 'DAYOFWEEK',
        'HOUR', 'MINUTE', 'SECOND'
    ]


def parse_iso8601(value):
    """This will parse an ISO 8601 arbitrary representation and return
    a list of the component parts.
    
    All time representations must have the time designator [T] before
    the time starts. This is in accordance with ISO 8601 §5.3.1.5
    where if time is not explicitly specified then the designator is
    required.
    
    Examples
    --------
    19660829
        This will return an isodate object.
    
    1966-08-29
        This will return an isodate object.
    
    T05:11:23
        This will return an isotime object.
        
    T051123
        This will return an isotime object.
    
    051123
        This will return an isodate object even though it is a valid
        basic format complete representation of time because the
        time designator [T] is missing.
    
    19660829T052436
        This will return an isodatetime object.
    
    P1Y2M15DT12H30M0S
        This will return an isoduration object.
    
    19660829/P1Y2M15DT12H30M0S
        This will return an isodate object and an isoduration object.
    
    P1Y2M15DT12H30M0S/19660829
        This will return an isoduration object and an isodate object.
    """
    ret = []
    for p in value.split('/'):
        if p.startswith('P'):
            ret.append(isoduration.parse_iso(p))
        elif p.startswith('R'):
            ret.append(isorecur.parse_iso(p))
        elif p.startswith('T'):
            ret.append(isotime.parse_iso(p))
        elif 'T' in p:
            ret.append(isodatetime.parse_iso(p))
        else:
            ret.append(isodate.parse_iso(p))
    return ret


