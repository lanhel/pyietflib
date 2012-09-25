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
                tzinfo=None):
        
        self.__date = isodate(
            expanded, century, year, month, dayofmonth, dayofyear,
            weekcentury, weekdecade, weekyearofdec, weekofyear, dayofweek)
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
    def fromtimestamp(cls, timestamp):
        """Return the local date corresponding to the POSIX timestamp,
        such as is returned by `time.time()`.
        
        See `datetime.datetime.fromtimestamp` for more details.
        """
        dt = datetime.datetime.fromtimestamp(timestamp)
        return cls.fromdatetime(dt)

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
        return isodatetime(expanded=date.iso_expanded,
                century=date.iso_century, year=date.iso_year,
                month=date.iso_month, dayofmonth=date.iso_dayofmonth,
                dayofyear=date.iso_dayofyear,
                weekcentury=date.iso_weekcentury, weekdecade=date.iso_weekdecade, weekyearofdec=date.iso_weekyearofdec,
                weekofyear=date.iso_weekofyear, dayofweek=date.iso_dayofweek,
                hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond,
                tzinfo=time.tzinfo)
    
    @classmethod
    def fromdatetime(cls, dt):
        """Construct an isodatetime from a `datetime.date`,
        `datetime.datetime`, or any object duck typed to those objects."""
        tt = dt.timetuple()
        wy, woy, dow = dt.isocalendar()
        wc = wy // 100
        wd = wy % 100 // 10
        wy = wy % 10
        ret = cls(
            expanded=0, century=(dt.year // 100), year=(dt.year % 100),
            month=dt.month, dayofmonth=dt.day,
            dayofyear=tt.tm_yday,
            weekcentury=wc, weekdecade=wd, weekyearofdec=wy, weekofyear=woy, dayofweek=dow,
            hour=tt.tm_hour, minute=tt.tm_minute, second=tt.tm_second
        )
        ret.iso_implied = None
        return ret
    
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
        fmt = []
        if self.iso_expanded:
            fmt.append("expanded={0.iso_expanded:+2d}")
        if self.iso_century:
            fmt.append("century={0.iso_century:2d}")
        if self.iso_year:
            fmt.append("year={0.iso_year:2d}")
        if self.iso_month:
            fmt.append("month={0.iso_month:2d}")
        if self.iso_dayofmonth:
            fmt.append("dayofmonth={0.iso_dayofmonth:2d}")
        if self.iso_dayofyear:
            fmt.append("dayofyear={0.iso_dayofyear:2d}")
        if self.iso_weekofyear:
            fmt.append("weekofyear={0.iso_weekofyear:2d}")
        if self.iso_dayofweek:
            fmt.append("dayofweek={0.iso_dayofweek:2d}")
        fmt = "isodate({0})".format(', '.join(fmt))
        return self.__repr_fmt.format(self)
    
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
        return (isinstance(other, isodate) or
            isinstance(other, datetime.date) or
            isinstance(other, datetime.datetime))
    
    def __cmp(self, other):
        return self.toordinal() - other.toordinal()
    
    def __hash__(self):
        return hash(bytes(self))
    
    def __int__(self):
        return self.__ordinal
    
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
                reduced=None, truncated=None, expanded=False):
        """Return a string representing the date in ISO 8601 format.
        
        `representation` may be `CALENDAR` (default), `ORDINAL`, or
        `WEEK` which will determine if the representation is a §5.2.1
        Calendar date, §5.2.2 Ordinal date, or §5.2.3 Week date. If
        this is `WEEK` and `year_of_decade` is True then §5.2.3.3 (c)
        or (d) will be selected (note: `year_of_decade` with `CALENDAR`
        or `ORDINAL` will result in an exception).
        
        If `basic` is true then the [-](hypen) is ommitted from the
        representation, otherwise (default) it will separate the parts
        of the representation. If there is no extended format then this
        will be asserted to be true.
        
        For reduced precision set `reduced` to the last part to include
        (`None` means no reduced precision) based on the representation
        desired:
            - `CALENDAR`
                - `DAYOFMONTH` for a complete representation §5.2.1.1.
                - `MONTH` for a specific month §5.2.1.2 (a).
                - `YEAR` for a specific year §5.2.1.2 (b).
                - `CENTURY` for a specific century §5.2.1.2 (c).
            
            - `ORDINAL`
                - `DAYOFYEAR` for a complete representation §5.2.2.1.
                - `YEAR` for a specific year §5.2.1.2 (b).
                - `CENTURY` for a specific century §5.2.1.2 (c).
            
            - `WEEK`
                - `DAYOFWEEK` for a complete representation §5.2.3.1.
                - `WEEKOFYEAR` for a specific week §5.2.3.2 (a).
                - `YEAR` for a specific year §5.2.1.2 (b).
                - `CENTURY` for a specific century §5.2.1.2 (c).
        
        For truncated representations set `truncated` to the first part
        to include (`None` means no truncation) based on the representation
        desired:
            - `CALENDAR`
                - `CENTURY` for a complete representation §5.2.1.1.
                
                - `YEAR` for an implied century §5.2.1.3 (a).
                    - `reduced=MONTH` for specific year and month
                      §5.2.1.3 (b)
                    
                    - `reduced=YEAR` for specific year §5.2.1.3 (c)
                
                - `MONTH` for an implied year §5.2.1.3 (d).
                    - `reduced=MONTH` for specific month §5.2.1.3 (e)
                
                - `DAYOFMONTH` for an implied month §5.2.1.3 (f).
            
            - `ORDINAL`
                - `CENTURY` for a complete representation §5.2.2.1.
                - `YEAR` for an implied century §5.2.2.2 (a).
                - `DAYOFYEAR` for an implied year §5.2.2.2 (b).
            
            - `WEEK`
                - `CENTURY` for a complete representation §5.2.3.1.
            
                - `DECADE` for year, week, and day in an implied
                  century §5.2.3.3 (a).
                    - `reduced=WEEKOFYEAR` for year and week in an
                      implied century §5.2.3.3 (b)
            
                - `YEAR` for year of implied decade, week, and day
                  §5.2.3.3 (c).
                    - `reduced=WEEKOFYEAR` for year of implied decade
                      and week §5.2.3.3 (d)
                
                - `WEEKOFYEAR` for week and day of implied year §5.2.3.3 (e).
                    - `reduced=WEEKOFYEAR` for week only of implied
                      year §5.2.3.3 (f)
            
                - `DAYOFWEEK` for day of an implied week §5.2.3.3 (g).
        
        Expanded representations will only be created if `expanded` is
        set to true. Note that if `iso_expanded` is 0 then the
        representation will have a '+0' before the century even though
        the ISO 8601 standard allows for the 0 to be missing. No truncation
        is allowed in an expanded representation, if both expanded and
        truncated are selected an error will be raised.
        
        This will duck type to `datetime.date.isoformat()` if called with
        no arguments.
        """
        pass
    
    
    ###
    ### datetime.date duck type methods
    ###
    @property
    def year(self):
        if self.iso_expanded:
            return self.iso_expanded * 10000 + self.iso_century * 100 + self.iso_year
        else:
            return self.iso_century * 100 + self.iso_year
    
    @property
    def month(self):
        return self.iso_month
    
    @property
    def day(self):
        return self.iso_dayofmonth
    
    def date(self):
        return self.__date
    
    def time(self):
        return self.__time
    
    def replace(self, year=None, month=None, day=None):
        e = self.iso_expanded
        c = self.iso_century
        y = self.iso_year
        m = self.iso_month
        d = self.iso_dayofmonth
        if year:
            c = year // 100
            y = year % 100
        if month:
            m = month
        if day:
            d = day
        fields = self.compute_all_fields(expanded=e, century=c, year=y,
                month=m, dayofmonth=d)
        return isodate(*fields)
    
    def timetuple(self):
        return (self.year, self.month, self.day, 0, 0, 0, self.weekday(), self.iso_dayofyear, -1)
    
    def toordinal(self):
        return self.__ordinal
    
    def weekday(self):
        return self.__dayofweek - 1
    
    def isoweekday(self):
        return self.__dayofweek
    
    def isocalendar(self):
        return (self.__weekcentury * 100 + self.__weekdecade * 10 + self.__weekyearofdec,
            self.__weekofyear, self.__dayofweek)
        
    def ctime(self):
        return self.strftime("%a %b %d %H:%M:%S %Y")
    
    def strftime(self, format):
        return time.strftime(format, self.timetuple())


### Initialize the class
isodate.today()


