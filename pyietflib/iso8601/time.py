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
import math

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
        The hour number in the range [00, 24]. If `None` then the current
        hour is used as the implied hour. If this is 24 then the minute
        must be 0 and the second must be 0, and it indicates the end of
        the current day and may be exchanged with 00:00:00 of the next
        day.
    
    minute
        THe minute number in the range [00, 59]. If `None` then the
        current minute is used as the implied minute.
    
    second
        The second number in the range [00, 59]. If `None` then the
        current second is used as the implied second. This may be set
        to 60 if hour is 23 and minute is 59 to indicate a positive
        leap second.
    
    microsecond
        The number of microseconds in the range [0000, 9999] within the
        current second. If this is `None` then the start of the current
        second is assumed (i.e. microsecond is 0000).
    
    tzinfo
        The `timezone` information object that is a subclass of
        `datetime.tzinfo`. If `None` then the current local time zone
        is assumed.
    
    
    Properties
    ----------
    iso_implied
        This is the implied base that determines a fully qualitied ISO
        time. This is returned as an object that is duck typed to
        `datetime.time`.

    Built-in Function
    -----------------
    Built in functions may have behavior that seem unusual and are
    documented here:
        bytes
            This will return a byte string that is a compact encoding
            of the time.

        hash
            The hash code is the same as `hash(bytes(obj))`.

        int
            This will return the ordinal number of days from 1 Jan 0001.
    """
    def __init__(self, hour=None, minute=None, second=None, microsecond=None,
            tzinfo=None):
        
        if (hour is None and minute is None and second is None):
            raise ValueError("Either hour, minute, or second must be specified.")
        
        self.__orig_hour = None
        self.__orig_minute = None
        self.__orig_second = None
        self.__orig_microsecond = None
        self.__orig_tzinfo = None
        
        if hour is not None:
            hour = int(hour)
            if not (0 <= hour <= 24):
                raise ValueError("Hour is not in range [00, 24].")
            self.__orig_hour = hour
        
        if minute is not None:
            minute = int(minute)
            if not (0 <= minute <= 59):
                raise ValueError("Minute is not in range [00, 59].")
            self.__orig_minute = minute
        
        if second is not None:
            second = int(second)
            if not (0 <= second < 60):
                if second == 60 and (hour != 23 and minute != 59):
                    raise ValueError("Second can only be 60 at 23:59:60.")
                else:
                    raise ValueError("Second is not in range [00, 59].")
            self.__orig_second = second
        
        if microsecond is not None:
            microsecond = int(microsecond)
            if not (0 <= microsecond < 1000000):
                raise ValueError("Microsecond is not in range [0, 1000000].")
            self.__orig_microsecond = microsecond
        
        if tzinfo is not None:
            if not isinstance(tzinfo, datetime.tzinfo):
                raise TypeError("tzinfo argument is not of type `datetime.tzinfo`.")
            self.__orig_tzinfo = tzinfo
        
        self.iso_implied = None
    
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
            return None

        hour = mo.group("hour")
        if hour is not None and hour != '-':
            hour = int(hour)
        
        minute = mo.group("minute")
        if minute is not None and minute != '-':
            minute = int(minute)

        second = mo.group("second")
        if second is not None:
            second = int(second)
        
        microsecond = None
        fraction = mo.group("fraction")
        if fraction is not None:
            fraction = int(fraction) / 10**len(fraction)
            if second is not None:
                microsecond = math.floor(fraction * 1000000)
            elif minute is not None:
                second, microsecond = divmod(fraction * 60 * 1000000, 1000000)
            else:
                minute, second = divmod(fraction * 60 * 60, 60)
                second, microsecond = divmod(second * 1000000, 1000000)
        
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
        
        return isotime(hour, minute, second, microsecond, tzinfo)
    
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

    def __str__(self):
        """This is the same as calling `isoformat`."""
        return self.isoformat()

    def __bytes__(self):
        if self.__bytes is None:
            raise NotImplementedError()
        return self.__bytes

    __format_re = re.compile(r"""(?ax)^
            (?P<align>(?P<fill>.)?[<>=\^])?
            (?P<sign>[+\- ])?
            (?P<altform>\#)?
            (?P<width>(?P<fill0>0)?\d+)?
            (?P<comma>,)?
            (.(?P<precision>\d+))?
            (?P<type>[scow])?
        $""");
    
    def __format__(self, format_spec):
        mo = self.__format_re.match(format_spec)
        if mo.group("sign") is not None:
            raise ValueError("Sign not allowed in isodate format specifier.")

        preferred_mark = (mo.group("comma") is not None)
        basic = (mo.group("altform") is None)
        ftype = mo.group("type")
        if ftype is None:
            ret = str(self)
        elif ftype == 's':
            ret = self.isoformat(basic=basic, preferred_mark=preferred_mark)
        else:
            raise ValueError("Unknown format code '{0}' for object of type 'isotime'.".format(ftype))

        if mo.group('precision') is not None:
            precision = int(mo.group('precision'))
            if len(ret) > precision:
                ret = ret[:precision]

        if mo.group('width') is not None:
            align = mo.group('align')
            fill = mo.group('fill')
            width = int(mo.group('width')) - len(ret)

            if fill is None:
                fill = ' '

            if width > 0:
                if align == '<':
                    ret = ret + fill * width
                elif align == '>' or align is None:
                    ret = fill * width + ret
                elif align == '^':
                    l = r = width // 2
                    if l + r < width:
                        l += 1
                    ret = fill * l + ret + fill * r
                elif align == '=' or mo.group("fill0") is not None:
                    raise ValueError("'=' alignment not allowed in isodate format specification.")

        return ret

    def __eq__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        return self.__cmp(other) == 0

    def __ne__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        return self.__cmp(other) != 0

    def __lt__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        return self.__cmp(other) < 0

    def __le__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        return self.__cmp(other) <= 0

    def __gt__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        return self.__cmp(other) > 0

    def __ge__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        return self.__cmp(other) >= 0

    def __comparable(self, other):
        return (isinstance(other, isotime) or
            isinstance(other, datetime.time) or
            isinstance(other, datetime.datetime))

    def __cmp(self, other):
        return float(self) - float(other)

    def __hash__(self):
        return hash(bytes(self))

    def __int__(self):
        return int(float(self))
    
    def __float__(self):
        return self.hour * 3600 + self.minute * 60 + self.second + self.microsecond / 1000000
        
    def __add__(self, other):
        raise NotImplementedError()

    __radd__ = __add__

    def __sub__(self, other):
        raise NotImplementedError()

    @property
    def iso_implied(self):
        return datetime.time(self.hour, self.minute, self.second,
            self.microsecond, self.tzinfo)

    @iso_implied.setter
    def iso_implied(self, value):
        if value is None:
            value = datetime.datetime.now()
        elif isinstance(value, isotime): #or isinstance(value, isodatetime):
            pass
        elif isinstance(value, datetime.time) or isinstance(value, datetime.datetime):
            pass
        elif isinstance(value, str):
            value = isotime.parse_iso(value)
        elif isinstance(value, int):
            value = isotime.fromtimestamp(value)
        elif isinstance(value, float):
            value = isotime.fromtimestamp(float(value))
        elif isinstance(value, time.struct_time):
            value = isotime.fromtimestamp(time.mktime(value))
        elif isinstance(value, tuple):
            value = isotime.fromtimestamp(time.mktime(value))
        elif isinstance(value, list):
            value = isotime.fromtimestamp(time.mktime(tuple(value)))
        elif isinstance(value, dict):
            value = isotime.fromtimestamp(time.mktime(tuple(value.values)))
        else:
            isodate.parse_iso(str(value))
        
        self.__hour = self.__orig_hour if self.__orig_hour is not None else value.hour
        self.__minute = self.__orig_minute if self.__orig_minute is not None else value.minute
        self.__second = self.__orig_second if self.__orig_second is not None else value.second
        self.__microsecond = self.__orig_microsecond if self.__orig_microsecond is not None else value.microsecond
        self.__tzinfo = self.__orig_tzinfo if self.__orig_tzinfo is not None else value.tzinfo
        self.__bytes = None
    
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
    