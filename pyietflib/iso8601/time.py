#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Module that will handle `ISO 8601:2004 Representation of dates and
times <http://www.iso.org/iso/catalogue_detail?csnumber=40874>`_ date
parsing and formatting.
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

import sys
if sys.version_info < (3, 2):
    raise Exception("iso8601 requires Python 3.2 or higher.")
import os
import logging
import datetime
import time
import re
import string

__all__ = ['isotime',
        'HOUR', 'MINUTE', 'SECOND'
    ]
__log__ = logging.getLogger("iso8601")

HOUR    = (0b100, 0b111)
MINUTE  = (0b110, 0b011)
SECOND  = (0b111, 0b001)


class isotime():
    """
    
    Arguments
    ---------
    hour
    
    minute
    
    second
    
    microsecond
    
    tzinfo
    
    """
    
    def __init__(self, hour=None, minute=None, second=None, microsecond=None,
            tzinfo=None):
        pass
    
    
    normal_re = re.compile(r'''(?ax)T?
        (?P<hour>\d{2})(:?(?P<minute>\d{2})(:?(?P<second>\d{2}))?)?
        ([,.](?P<fraction>\d+))?
        ((?P<utc>Z)|((?P<tzsign>[+-])(?P<tzhour>\d{2})(?P<tzmin>\d{2})?))?
        ''')
    truncated_re = re.compile(r'''(?ax)T?
        (?P<hour>-)
        ((?P<minute>(-|\d{2})))
        (:?(?P<second>\d{2}))?
        ([,.](?P<fraction>\d+))?
        (?P<utc>)(?P<tzsign>)(?P<tzhour>)(?P<tzmin>)
        ''')
        
    @classmethod
    def parse_iso(cls, value):
        if '-' not in value:
            mo = cls.normal_re.match(value)
        else:
            mo = cls.truncated_re.match(value)
        
        if mo is None:
            raise ValueError("Invalid ISO time representation.")

        hour = mo.group("hour")
        if hour is not None and hour != '-':
            hour = int(hour)
        
        minute = mo.group("minute")
        if minute is not None and minute != '-':
            minute = int(minute)

        second = mo.group("second")
        if second is not None:
            second = int(second)
        
        fraction = mo.group("fraction")
        if fraction is not None:
            fraction = int(fraction) % 1000000
        
        if mo.group("utc") == 'Z':
            tzinfo = datetime.timezone.utc
        elif mo.group("tzsign") is not None:
            offh = int(mo.group("tzhour"))
            if mo.group("tzsign") == '-':
                offh = offh * -1
            offm = int(mo.group("tzmin")) if mo.group("tzmin") is not None else 0
            td = datetime.timedelta(hours=offh, minutes=offm)
            tzinfo = datetime.timezone(td)
        else:
            tzinfo = None
        
        print(hour, minute, second, fraction, tzinfo)
        
        return isotime(hour, minute, second, fraction, tzinfo)
    
    
    def __str__(self):
        """This is the same as calling `isoformat`."""
        return self.isoformat()

    def __repr__(self):
        """This includes all the implied values to recrate this object as
        it stands."""
        fmt = []
        fmt.append("hour={0.hour:d}")
        fmt.append("minute={0.minute:d}")
        fmt.append("second={0.second:d}")
        if self.microsecond > 0:
            fmt.append("microsecond={0.microsecond:d}")
        if self.tzinfo:
            fmt.append("tzinfo={0.tzinfo}")
        fmt = "isotime({0})".format(', '.join(fmt))
        return self.__repr_fmt.format(self)

    def __eq__(self, other):
        if isinstance(other, isodate):
            return (self.hour == other.hour and
                    self.minute == other.minute and
                    self.second == other.second and
                    self.microsecond == other.microsecond)
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, timedelta):
            return NotImplemented
        raise NotImplementedError()

    def __le__(self, other):
        if not isinstance(other, timedelta):
            return NotImplemented
        raise NotImplementedError()

    def __gt__(self, other):
        if not isinstance(other, timedelta):
            return NotImplemented
        raise NotImplementedError()

    def __ge__(self, other):
        if not isinstance(other, timedelta):
            return NotImplemented
        raise NotImplementedError()

    def __hash__(self):
        return hash(self._getstate())
        raise NotImplementedError()

    def __add__(self, other):
        raise NotImplementedError()

    __radd__ = __add__

    def __sub__(self, other):
        raise NotImplementedError()
    
    @property
    def min(self):
        raise NotImplementedError()
    
    @property
    def max(self):
        raise NotImplementedError()
    
    @property
    def resolution(self):
        raise NotImplementedError()
    
    @property
    def hour(self):
        raise NotImplementedError()
    
    @property
    def minute(self):
        raise NotImplementedError()
    
    @property
    def second(self):
        raise NotImplementedError()
    
    @property
    def microsecond(self):
        raise NotImplementedError()
    
    @property
    def tzinfo(self):
        raise NotImplementedError()
    
    def replace(self, hour=None, minute=None, second=None, microsecond=None, tzinfo=None):
        raise NotImplementedError()
    
    def isoformat(self):
        raise NotImplementedError()
    
    def strftime(self, format):
        raise NotImplementedError()
        
    def utcoffset(self):
        raise NotImplementedError()
    
    def dst(self):
        raise NotImplementedError()
    
    def tzname(self):
        raise NotImplementedError()
    