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

from .date import *
from .time import *

__all__ = ['isodatetime']
__log__ = logging.getLogger("iso8601")


class isodatetime():
    """An `isodatetime` object duck types the python library class
    `datetime.datetime` to add capabilities that are available in
    `ISO 8601:2004 Representation of dates and times
    <http://www.iso.org/iso/catalogue_detail?csnumber=40874>`_.
    
    All arguments are either convertable to positive integers or are
    `None`. If the argument is associated with `isodate` then see its
    documentation for details on how a `None` is handled. If the
    argument is associated with `isotime` then see its documentation
    for deatails on how a `None` is handled.
    
    Format Specifier
    ----------------
    The following are `isodate` specific `format_spec` symantics for use
    with string formatting:
        fill
            The fill character, if `None` this defaults to space.
    
        align
            May use the '<', '>', or '^' alignment operator.
    
        sign
            If this is '+' or '-' then the expanded representation is used.
    
        #
            The normal format is to use extended unless not applicable
            then use basic. This will force all representations to basic.
    
        0
            This is not allowed because '=' align is not allowed.
    
        width
            The width of the field.
    
        ,
            This indicates that the preferred fraction separator [,]
            should be used instead of [.].
    
        precision
            This representation will be shortened to this length.
        
            .. WARNING::
                Use of precision could result in an invalid ISO 8601
                reduced precision representation.
    
        type
            s
                This results in the representation as `str(x)`. The align,
                width, and precision are used, and all other modifiers are
                ignored.
        
            c
                This will generate an ISO 8601 §5.2.1 Calendar date
                representation with ISO 8601 §5.3.4.2 time representation
                that has a [T] separator between date and time.
        
            o
                This will generate an ISO 8601 §5.2.2 Ordinal date
                representation with ISO 8601 §5.3.4.2 time representation
                that has a [T] separator between date and time.
        
            w
                This will generate an ISO 8601 §5.2.3 Week date
                representation with ISO 8601 §5.3.4.2 time representation
                that has a [T] separator between date and time.
    
    """
    def __init__(self,
                expanded=None, century=None, year=None,
                month=None, dayofmonth=None,
                dayofyear=None,
                weekcentury=None, weekdecade=None, weekyearofdec=None,
                weekofyear=None, dayofweek=None,
                hour=None, minute=None, second=None, microsecond=None,
                tzinfo=None,
                date=None, time=None):
        
        if date:
            if not isinstance(date, isodate):
                raise TypeError("Date must be of type isodate.")
            self.__date = date
        else:
            self.__date = isodate(
                expanded, century, year, month, dayofmonth, dayofyear,
                weekcentury, weekdecade, weekyearofdec, weekofyear, dayofweek)
        
        if time:
            if not isinstance(time, isotime):
                raise TypeError("Time must be of type isotime.")
            self.__time = time
        else:
            self.__time = isotime(hour, minute, second, microsecond, tzinfo)

    __today_expire = 0
    __today_cache = None
    @classmethod
    def today(cls):
        """Return a current local date.
        
        See `datetime.datetime.today` for more details.
        """
        t = time.time()
        if cls.__today_expire < t:
            secs = time.time()
            tt = time.gmtime(secs)
            cls.__today_cache = None
            cls.__today_cache = cls.fromtimestamp(secs)
            cls.__today_expire = time.mktime((tt.tm_year, tt.tm_mon, tt.tm_mday+1, 0, 0, 0, 0, 0, 0))
        assert cls.__today_cache, "No cached isodate."
        return cls.__today_cache
    
    @classmethod
    def now(cls, tz=None):
        return cls.fromtimestamp(time.time(), tz=tz)
    
    @classmethod
    def utcnow(cls):
        return cls.utcfromtimestamp(time.time())
    
    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        """Return the local date corresponding to the POSIX timestamp,
        such as is returned by `time.time()`.
        
        See `datetime.datetime.fromtimestamp` for more details.
        """
        us, secs = math.modf(timestamp)
        us = round(us * 1e6)
        if us == 1e6:
            secs += 1
            us = 0
        if tz is None:
            y, m, d, hh, mm, ss, wday, yday, isdst = time.localtime(secs)
        else:
            y, m, d, hh, mm, ss, wday, yday, isdst = time.gmtime(secs)
        ss = min(ss, 59)
        d = isodate(expanded=None, century=(y // 100), year=(y % 100),
            month=m, dayofmonth=d,
            dayofyear=yday,
            weekcentury=None, weekdecade=None, weekyearofdec=None,
            weekofyear=None, dayofweek=None)
        t = isotime(hour=hh, minute=mm, second=ss, microsecond=us, tzinfo=tz)
        return isodatetime(date=d, time=t)
    
    @classmethod
    def utcfromtimestamp(cls, timestamp):
        return cls.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    
    @classmethod
    def fromordinal(cls, ordinal):
        """Return the date corresponding to the proleptic Gregorian ordinal,
        where January 1 of year 1 has ordinal 1.
        
        See `datetime.datetime.fromordinal` for more details.
        """
        if not 0 < ordinal <= datetime.datetime.max.toordinal():
            raise OverflowError("Date ordinal {0} out of range [0, {1}].".format(ordinal, datetime.date.max.toordinal()))
        dt = datetime.datetime.fromordinal(ordinal)
        return cls.fromdatetime(dt)
    
    @classmethod
    def combine(cls, date, time):
        """Return the datetime as a combination of a date and time object.
        
        See `datetime.datetime.combine` for more details.
        """
        if isinstance(date, datetime.date):
            date = isodate.fromdatetime(date)
        if isinstance(time, datetime.time):
            time = isotime(hour=time.hour, minute=time.minute, second=time.second,
                microsecond=time.microsecond, tzinfo=time.tzinfo)
        return isodatetime(date=date, time=time)
    
    @classmethod
    def fromdatetime(cls, dt):
        """Construct an isodatetime from a `datetime.date`,
        `datetime.datetime`, or any object duck typed to those objects."""
        tt = dt.timetuple()
        y, m, d, hh, mm, ss, wday, yday, dst = tt
        wy, woy, dow = dt.isocalendar()
        wc = wy // 100
        wd = wy % 100 // 10
        wy = wy % 10
        ret = cls(
            expanded=0, century=(y // 100), year=(y % 100),
            month=m, dayofmonth=d,
            dayofyear=yday,
            weekcentury=wc, weekdecade=wd, weekyearofdec=wy, weekofyear=woy, dayofweek=dow,
            hour=hh, minute=mm, second=ss
        )
        ret.iso_implied = None
        return ret
    
    @classmethod
    def strptime(cls, date_string, format):
        t = time.mktime(time.strptime(date_string, format))
        return cls.fromtimestamp(t)
    
    @classmethod
    def parse_iso(cls, value, expand_digits=None):
        """Parse an ISO date time string in `value` and return an
        `isodatetime` object.
        
        Expanded Representation
        -----------------------
        An expanded representation is a special case where the number
        of agreed upon digits in the representation to be specified in
        `expand_digits`. If `expand_digits` is `None` (default) and
        the value matches an expanded format then a `ValueError` shall
        be thrown.
        """
        dv, tv = value.split('T')
        do = isodate.parse_iso(dv, expand_digits)
        to = isotime.parse_iso(tv)
        return isodatetime.combine(do, to)

    def __repr__(self):
        """This includes all the implied values to recrate this object as
        it stands."""
        d = repr(self.__date)[len("isodate("):-len(")")]
        t = repr(self.__time)[len("isotime("):-len(")")]
        return "isodatetime({0}, {1})".format(d, t)
    
    def __str__(self):
        """This is the same as calling `isoformat()`."""
        return self.isoformat(representation=CALENDAR, basic=False, expanded=False)

    def __bytes__(self):
        if self.__bytes is None:
            self.__bytes = [self.iso_dayofmonth, self.iso_month, self.iso_year, self.iso_century]
            exp = self.iso_expanded
            while abs(exp) > 256:
                exp, part = divmod(exp, 256)
                self.__bytes.append(part)
            self.__bytes.append(exp)
            self.__bytes.reverse()
            self.__bytes = bytes(self.__bytes)
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
        if mo.group("comma") is not None:
            raise ValueError("Comma not allowed in isodate format specifier.")
        
        expanded = (mo.group("sign") is not None)
        basic = (mo.group("altform") is not None)
        ftype = mo.group("type")
        if ftype is None:
            ret = str(self)
        elif ftype == 's':
            ret = str(self)
        elif ftype == 'c':
            ret = self.isoformat(representation=CALENDAR, basic=basic, expanded=expanded)
        elif ftype == 'o':
            ret = self.isoformat(representation=ORDINAL, basic=basic, expanded=expanded)
        elif ftype == 'w':
            ret = self.isoformat(representation=WEEK, basic=basic, expanded=expanded)
        else:
            raise ValueError("Unknown format code '{0}' for object of type 'isodate'.".format(ftype))
        
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
        od = other.date() if isinstance(other, datetime.datetime) else other.__date
        ot = other.time() if isinstance(other, datetime.datetime) else other.__time
        return (self.__date == od and self.__time == ot)
    
    def __ne__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        od = other.date() if isinstance(other, datetime.datetime) else other.__date
        ot = other.time() if isinstance(other, datetime.datetime) else other.__time
        return (self.__date != od or self.__time != ot)
    
    def __lt__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        od = other.date() if isinstance(other, datetime.datetime) else other.__date
        ot = other.time() if isinstance(other, datetime.datetime) else other.__time
        return (self.__date < od or (self.__date == od and self.__time < ot))
    
    def __le__(self, other):
        return self == other or self < other
    
    def __gt__(self, other):
        if not self.__comparable(other):
            return NotImplemented
        od = other.date() if isinstance(other, datetime.datetime) else other.__date
        ot = other.time() if isinstance(other, datetime.datetime) else other.__time
        return (self.__date > od or (self.__date == od and self.__time > ot))
    
    def __ge__(self, other):
        return self == other or self > other
    
    def __comparable(self, other):
        return (isinstance(other, isodatetime) or
            isinstance(other, datetime.datetime))
    
    def __hash__(self):
        return hash(bytes(self))
    
    def __int__(self):
        return self.__date.toordinal()
    
    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            o = self.toordinal() + other.days
            return isodate.fromordinal(o)
        return NotImplemented
    
    __radd__ = __add__
    
    def __sub__(self, other):
        if isinstance(other, datetime.timedelta):
            return self + datetime.timedelta(-other.days)
        if hasattr(other, "toordinal"):
            days1 = self.toordinal()
            days2 = other.toordinal()
            return datetime.timedelta(days=(days1 - days2))
        return NotImplemented
    
    def __getstate__(self):
        return bytes(self)
    
    def __setstate__(self, state):
        if len(state) < 5:
            raise TypeError("Not enough arguments.")
        expanded = 0
        for x in state[:-4]:
            expanded = expanded * 256 + x
        (
            self.__orig_expanded, self.__orig_century, self.__orig_year,
            self.__orig_month, self.__orig_dayofmonth,
            self.__orig_dayofyear,
            self.__orig_weekcentury, self.__orig_weekdecade, self.__orig_weekyearofdec,
            self.__orig_weekofyear, self.__orig_dayofweek
        ) = self.compute_all_fields(
            expanded=expanded, century=state[3], year=state[2],
            month=state[1], dayofmonth=state[0])
        self.iso_implied = None
    

    def isoformat(self, representation=CALENDAR, basic=False,
                reduced=None, truncated=None, expanded=False,
                fraction=True, preferred_mark=False, timezone=True,
                separator='T'):
        """Return a string representing the date time in ISO 8601 format.
        
        ``basic``, ``reduced``, and ``truncated`` are used in the same
        manner as in ``isodate`` for the date formatting and as in
        ``isotime`` for the time formatting.
        
        ``representation`` and ``expanded`` are used in the same manner
        as specified in ``isodate``.
        
        ``fraction``, ``preferred_mark``, and ``timezone`` are used in
        the same manner as specified in ``isotime``.
        
        ``separator`` will change the string used to separate the date
        from the time with the default being 'T'.
        """
        date = self.__date.isoformat(
                representation=representation, basic=basic,
                reduced=reduced, truncated=truncated, expanded=expanded)
        time = self.__time.isoformat(
                basic=basic, reduced=reduced, truncated=truncated,
                fraction=fraction, preferred_mark=preferred_mark, timezone=timezone)
        return "{0}{1}{2}".format(date, separator, time)
    
    
    ###
    ### datetime.date duck type methods
    ###
    @property
    def year(self):
        return self.__date.year
    
    @property
    def month(self):
        return self.__date.month
    
    @property
    def day(self):
        return self.__date.day
    
    def date(self):
        return self.__date
    
    def time(self):
        return self.__time
    
    def replace(self, year=None, month=None, day=None):
        date = self.__date.replace(year, month, day)
        time = self.__time
        return isodatetime(
            expanded=date.iso_expanded, century=date.iso_century, year=date.iso_year,
            month=date.iso_month, dayofmonth=date.iso_dayofmonth,
            dayofyear=date.iso_dayofyear,
            weekcentury=date.iso_weekcentury, weekdecade=date.iso_weekdecade, weekyearofdec=date.iso_weekyearofdec,
            weekofyear=date.iso_weekofyear, dayofweek=date.iso_dayofweek,
            hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond,
            tzinfo=time.tzinfo)
    
    def timetuple(self):
        y, m, d, hh, mm, ss, wday, doy, dst = self.__date.timetuple()
        hh = self.__time.hour
        mm = self.__time.minute
        ss = self.__time.second
        dst = self.__time.dst()
        if dst is None:
            dst = -1
        else:
            dst = int(dst != 0)
        return time.struct_time((y, m, d, hh, mm, ss, wday, doy, dst))
    
    def toordinal(self):
        return self.__date.toordinal()
    
    def weekday(self):
        return self.__date.weekday()
    
    def isoweekday(self):
        return self.__date.isoweekday()
    
    def isocalendar(self):
        return self.__date.isocalendar()
        
    def ctime(self):
        return self.strftime("%a %b %d %H:%M:%S %Y")
    
    def strftime(self, format):
        return time.strftime(format, self.timetuple())


### Initialize the class
isodate.today()


