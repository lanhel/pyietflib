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

__all__ = ['isodate',
        'CALENDAR', 'ORDINAL', 'WEEK',
        'CENTURY', 'YEAR',
        'MONTH', 'DAYOFMONTH',
        'DAYOFYEAR',
        'WEEKOFYEAR', 'DAYOFWEEK'
    ]
__log__ = logging.getLogger("iso8601")

CALENDAR = 0b1110110001
ORDINAL  = 0b1110001001
WEEK     = 0b1111000111

CENTURY    = (0b1100000001, 0b1111111111)
YEAR       = (0b1110000001, 0b0011111111)
MONTH      = (0b1110100001, 0b0000110001)
DAYOFMONTH = (0b1110110001, 0b0000010001)
DAYOFYEAR  = (0b1110001001, 0b0000001001)
WEEKOFYEAR = (0b1111000101, 0b0000000111)
DAYOFWEEK  = (0b1111000111, 0b0000000011)


class isodate():
    """An `isodate` object duck types the python library class
    `datetime.date` to add capabilities that are available in
    `ISO 8601:2004 Representation of dates and times
    <http://www.iso.org/iso/catalogue_detail?csnumber=40874>`_.
    
    All arguments are either convertable to positive integers or are
    `None`. If an argument is `None` then the associated property shall
    receive a value based on `iso_implied` as follows:
        1. If `century` is `None` then `century` is set to
            `iso_implied.century` then item 2 is performed.
        2. If `year` is `None` then `year` is set to `iso_implied.year`
            then item 3 is performed.
        3. If `dayofyear`, `month`, and `weekofyear` are `None` then
            `dayofyear` shall be set to `iso_implied.dayofyear`, and
            then item 4 is performed.
        4. If `dayofyear` is given then `month`, `dayofmonth`,
            `weekyear`, `weekofyear`, and `dayofweek` shall be
            set to match.
        5. If `month` and `dayofmonth` are given then `dayofyear`,
            `weekyear`, `weekofyear`, and `dayofweek` shall be
            set to match.
        6. If `month` is given then `dayofmonth` is set to
            `iso_implied.day`, and then item 5 is performed.
        7. If `dayofmonth` is given then `month` is set to
            `iso_implied.month`, and then item 5 is performed.
        8. If `weekyear`, `weekofyear` and `dayofweek` are given
           then `dayofyear`, `month`, and `dayofmonth` shall be
            set to match.
        9. If `weekyear`, and `weekofyear` is set then `dayofweek`
            is set to `iso_implied.dayofweek`, and then item 8 is
            performed.
        10. If `weekyear` is given then `weekofyear` is set to
            `iso_implied.weekofyear` and item 9 is then performed.
        11. If `weekofyear` and `dayofweek` is set then `weekyear`
            is set to `iso_implied.weekyear` and item 8 is performed.
        12. If `weekofyear` is set then `dayofweek` is set to
            `iso_implied.dayofweek` and item 11 is performed.
        13. If `dayofweek` is set then `weekofyear` is set to
            `iso_implied.weekofyear` and then item 11 is performed.
        
    This may create a calendar date (§5.2.1 Calendar date) by using
    `month` and `dayofmonth`; an ordinal date (§5.2.2 Ordinal date)
    by using `dayofyear`; or a week date (§5.2.3 Week date) by using
    `weekyear`, `weekofyear`, and `dayofweek`. If these calendar
    types are mixed it must result in the same day being represented
    otherwise a `ValueError` shall be thrown.
    
    The creation of expanded respresentations may be done by using the
    `expanded` argument.
    
    Reduced precision (§5.2.1.2, §5.2.3.2) and truncated (§5.2.1.2,
    §5.2.2.2, and §5.2.3.3) may be created by igoring some arguments
    or setting those arguments to `None`. The only condition is that
    if more than one argument is given they must be contiguous, for
    example `isodate(year=66, day=29)` will result in a `ValueError`
    being raised. In ISO 8601 there is no representation for a reduced
    precision ordinal date so if an object is created and only `dayofyear`
    is given then a string representation will always have the current
    year.
    
    
    Arguments
    ---------
    expanded
        This is a signed integer that will allow for dates that are
        before 1 A.D. (`datetime.MINYEAR`) or after 9999 A.D.
        (`datetime.MAXYEAR`). If `None` then this will be set to
        `+00`. If 1 B.C. is desired then this would be set to `-00`.
    
    century
        This represents the century and must be in the range 0 to 99.
    
    year
        This represents the year within the century and must be in the
        range 00 to 99.
        
        This is different from `datetime.date` where the `year` is expected
        to be in the range 1 to 9999. This change is to allow construction
        of reduced, truncated, and expanded representations.
    
    month
        This represents the month of the year and must be in the range
        of 1 to 12.
    
    dayofmonth
        This represents the day of the year and must be in the range of
        1 to 31.
        
        In a truncated representation with an implied `month` then 29,
        30, and 31 are always allowed, and in string representations will
        always be the last day of the month and may be adjusted. For
        example if this is 30 but the current month is February and the
        year is not a leap year then in the string representation this
        will 28.
    
    dayofyear
        This is the ordinal day of the year and must be in the range of
        1 to 366.
        
        If the `century` and `year` are given and it is not a leap year
        then a value of 366 will not be accepted.
        
        In a truncated representation with an implied `year` then 366 is
        always allowed, and in string representations it will always be
        the last day of the year and may be changed to 365.
    
    weekyear
        This is the gregorian year that the week falls in. This is usually
        the same as the actual year, but may be the previous year for week
        52 or 53, or the following year for week 1.
    
    weekofyear
        This is the week of the year in the range 1 to 53.
        
        In a truncated representation with an implied `year` then 53 is
        always allowed, and in string representations it will always be
        the last week of the year and may be changed to 52.
    
    weekday
        This is the day of the week in the range 1 to 7.
    
    
    Class Properties
    ----------------
    months
        Is a list indexed on the ISO month number where each element is
        a tuple with the month name from the standard, the number of
        days in the month, the number of days in a leap year, the ordinal
        days, and the ordinal days in a leap year.
    
    weekdays
        Is a list indexed on the ISO weekday number where each element
        is a tuple with the weekday name from the standard, the python
        `datetime.date.weekday` conversion, and the python `time.strftime`
        conversion.
    
    
    Properties
    ----------
    iso_implied
        This is an `isodate` object that is used to calculate implied
        values. This may be set to `None` which will result in all the
        `iso_*` properties that are implied to return `None`. The
        initial value for this property is the the same as returned by
        `isodate.today()` when the object was created.
        
        This will attempt to convert other types into an `isodate` object
        according to the following list (other types will be converted
        to a string via `str(value)` and processed like a string):
            - `datetime.date`: `isodate` created from properties.
            - `datetime.datetime`: `isodate` created from properties.
            - `str`: `parse_iso(value)`.
            - `int`: `fromtimestamp(value)`
            - `float`: `fromtimestamp(int(value))`.
            - `time.struct_time`: `fromtimestamp(time.mktime(value))`.
            - `tuple`: `fromtimestamp(time.mktime(value))`.
            - `list`: `fromtimestamp(time.mktime(tuple(value)))`
            - `dict`: `fromtimestamp(time.mktime(tuple(value.values)))`
        
        Setting `iso_implied` to `None` will affect all methods that are
        derived from `datetime.date`, thus calling those methods will
        result in undefined behavior. This case is meant for testing or
        if detailed information is desired about the original ISO string.
    
    iso_leap_year
        A boolean that indicates that this is a leap year.
    
    iso_expanded
        This is the expanded year value for years before 1 A.D. and
        after 9999 A.D.
    
    iso_century
        This is the century of the date.
    
    iso_year
        This is the year in the century of the date.
    
    iso_month
        This is the month of the date.
    
    iso_dayofmonth
        This is the day of month of the date.
    
    iso_dayofyear
        This is the day of year of the date. In truncated representations
        if the month is known but the day of month is not known then this
        will be the first day of the month; if the week is known but the
        day of week is not known then this will be the first day of the
        week.
    
    iso_weekyear
        This is the year that `iso_weekofyear` is in. This will be the
        same as the gregorian year except for dates that cross year
        boundaries then it may be the previous year if `iso_dayofweek`
        is Monday (1), Tuesday (2), or Wednesday (3); or in the following
        year if `iso_dayofweek` is Friday (5), Saturday (6), or Sunday (7).
    
    iso_weekofyear
        This is the week of year of the date. In truncated representations
        if the month is known but the day of month is not known then this
        will be the first week of the month.
        
        This may be a negative value which indicates that for the day
        represented the week of year and the day of week are in the
        previous year.
    
    iso_dayofweek
        This is the day of week of the date.
    
    year
        This is the same as `datetime.date.year` in value, but will
        return an implied year if this is reduced precision or truncated
        representation.
    
    month
        This is the same as `datetime.date.month` in value, but will
        return an implied month if this is reduced precision or truncated
        representation.
    
    day
        This is the same as `datetime.date.day` in value but will
        return an implied day if this is reduced precision or truncated
        representation.
    """
    
    def __init__(self,
                expanded=None, century=None, year=None,
                month=None, dayofmonth=None,
                dayofyear=None,
                weekyear=None, weekofyear=None, dayofweek=None):
        
        if (century is None and year is None and
                month is None and dayofmonth is None and
                dayofyear is None and
                weekyear is None and weekofyear is None and dayofweek is None):
            raise ValueError("At least one date component must be specified.")
        
        self.__orig_expanded = expanded
        self.__orig_century = century
        self.__orig_year = year
        self.__orig_month = month
        self.__orig_dayofmonth = dayofmonth
        self.__orig_dayofyear = dayofyear
        self.__orig_weekyear = weekyear
        self.__orig_weekofyear = weekofyear
        self.__orig_dayofweek = dayofweek
        
        if self.__today_cache is None:
            #Initial creation of today object
            assert century is not None
            assert year is not None
            assert month is not None
            assert dayofmonth is not None
            assert dayofyear is not None
            assert weekyear is not None
            assert weekofyear is not None
            assert dayofweek is not None
            self.iso_implied = None
        else:
            self.iso_implied = self.today()
    
    months = [
        (None,        0,  0,  (  0,   0), (  0,   0)),
        ("January",   31, 31, (  1,  31), (  1,  31)),
        ("February",  28, 29, ( 32,  59), ( 32,  60)),
        ("March",     31, 31, ( 60,  90), ( 61,  91)),
        ("April",     30, 30, ( 91, 120), ( 92, 121)),
        ("May",       31, 31, (121, 151), (122, 152)),
        ("June",      30, 30, (152, 181), (153, 182)),
        ("July",      31, 31, (182, 212), (183, 213)),
        ("August",    31, 31, (213, 243), (214, 244)),
        ("September", 30, 30, (244, 273), (245, 274)),
        ("October",   31, 31, (274, 304), (275, 305)),
        ("November",  30, 30, (305, 334), (306, 335)),
        ("December",  31, 31, (335, 365), (336, 366))
    ]
    
    weekdays = [
        None,
        ("Monday",    0, 1),
        ("Tuesday",   1, 2),
        ("Wednesday", 2, 3),
        ("Thursday",  3, 4),
        ("Friday",    4, 5),
        ("Saturday",  5, 6),
        ("Sunday",    6, 0),
    ]
    
    __today_expire = 0
    __today_cache = None
    @classmethod
    def today(cls):
        """Return a current local date.
        
        See `datetime.date.today` for more details.
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
        
        See `datetime.date.fromtimestamp` for more details.
        """
        dt = datetime.date.fromtimestamp(timestamp)
        return cls.fromdatetime(dt)

    @classmethod
    def fromordinal(cls, ordinal):
        """Return the date corresponding to the proleptic Gregorian ordinal,
        where January 1 of year 1 has ordinal 1.
        
        See `datetime.date.fromordinal` for more details.
        """
        if not 0 < ordinal <= datetime.date.max.toordinal():
            raise OverflowError("Date ordinal {0} out of range [0, {1}].".format(ordinal, datetime.date.max.toordinal()))
        dt = datetime.date.fromordinal(ordinal)
        return cls.fromdatetime(dt)
    
    @classmethod
    def fromdatetime(cls, dt):
        """Construct an isodate from a `datetime.date`, `datetime.datetime`,
        or any object duck typed to those objects."""
        tt = dt.timetuple()
        wy, woy, dow = dt.isocalendar()
        ret = cls(
            expanded=0, century=(dt.year // 100), year=(dt.year % 100),
            month=dt.month, dayofmonth=dt.day,
            dayofyear=tt.tm_yday,
            weekyear = wy, weekofyear=woy, dayofweek=dow
        )
        ret.iso_implied = None
        return ret
    
    @classmethod
    def compute_fields_from_ordinal(cls, ordinal):
        """Given an ordinal number of days from 1 Jan 0001 compute and
        return fields in order: extended, century, year, month, dayofmonth,
        dayofyear, weekofyear, dayofweek."""
        pass
    
    @classmethod
    def compute_all_fields(cls, expanded=None, century=None, year=None,
            month=None, dayofmonth=None, dayofyear=None,
            weekyear=None, weekofyear=None, dayofweek=None):
        """Given a set of ISO date fields compute all fields that are `None`
        and return the fields in order: expanded, century, year, month,
        dayofmonth, dayofyear, weekyear, weekofyear, dayofweek."""
        def month_from_dayofyear(cls, leap, dayofyear):
            mrangeoff = 3 if not leap else 4
            for i, m in enumerate(cls.months):
                if m[mrangeoff][0] <= dayofyear <= m[mrangeoff][1]:
                    return i, dayofyear - m[mrangeoff][0] + 1
            raise ValueError("Invalid day of year {0}.", dayofyear)
        
        def days_before_year(cls, year):
            return (year - 1) * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
        
        def week_1_monday(cls, year):
            fdy = days_before_year(cls, year) + 1
            fdw = (fdy + 6) % 7
            monday = fdy - fdw
            if fdw > 3: #Thursday
                monday += 7
            return monday
            
        def week_from_dayofyear(cls, expanded, century, year, dayofyear):
            weekyear = expanded * 10000 + century * 100 + year
            adjust = adjustment_to_jan_1_day_of_year(expanded, century, year)
            dow = (dayofyear - adjust) % 7
            if dow == 0:
                dow = 7
            week = (dayofyear - dow + 10) // 7
            if week == 0:
                weekyear -= 1
                pyd = 365 if not (weekyear % 4 == 0 and (weekyear % 100 != 0 or weekyear % 400 == 0)) else 366
                week = (pyd + dayofyear - dow + 10) // 7
            elif week == 53 and dow < 4:
                week = 1
            return weekyear, week, dow
        
        def adjustment_to_jan_1_day_of_year(expanded, century, year):
            yby = expanded * 10000 + century * 100 + year - 1
            yofc = yby % 100
            cby = yby - yofc
            gfac = yofc + yofc // 4
            jan1dow = 1 + (((((cby // 100) % 4) * 5) + gfac) % 7)
            return {1:0, 2:-1, 3:-2, 4:-3, 5:3, 6:2, 7:1}[jan1dow]
        
        if expanded is None:
            expanded = 0
        if century is None:
            century = 0
        if year is None:
            year = 1
        
        leap = (year % 4 == 0 and (century != 0 or century % 4 == 0))
        mrangeoff = 3 if not leap else 4
        
        if dayofyear is None and month is None and weekofyear is None:
            dayofyear = 1
        
        if dayofyear is not None:
            if dayofyear < 0 or dayofyear > cls.months[12][mrangeoff][1]:
                raise ValueError("Day of year ({0}) out of range.".format(dayofyear))
            month, dayofmonth = month_from_dayofyear(cls, leap, dayofyear)
            weekyear, weekofyear, dayofweek = week_from_dayofyear(cls, expanded, century, year, dayofyear)
        
        elif month is not None:
            if dayofmonth is None:
                dayofmonth = 1
            dayofyear = cls.months[month][mrangeoff][0] + dayofmonth - 1
            weekyear, weekofyear, dayofweek = week_from_dayofyear(cls, expanded, century, year, dayofyear)
        
        elif weekofyear is not None:
            if weekyear is None:
                weekyear = year
            if dayofweek is None:
                dayofweek = 1
            adjust = adjustment_to_jan_1_day_of_year(expanded, century, year)
            dayofyear = (weekofyear - 1) * 7 + dayofweek + adjust
            month, dayofmonth = month_from_dayofyear(cls, leap, dayofyear)
        
        return (expanded, century, year, month, dayofmonth, dayofyear,
                weekyear, weekofyear, dayofweek)
    
    
    ###
    ### This holds the regular expressions for each type of representation.
    ### It is a dictionary where the key is a tuple of has a hyphen and
    ### has a 'W' where the value is a dictionary of string size to a list
    ### of possible regular expressions.
    ###
    representations = {
        (False, False):{
            8:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})(?P<month>\d{2})(?P<dayofmonth>\d{2})')],
            7:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})(?P<dayofyear>\d{3})')],
            6:[ re.compile(r'(?ax)(?P<year>\d{2})(?P<month>\d{2})(?P<dayofmonth>\d{2})')],
            5:[ re.compile(r'(?ax)(?P<year>\d{2})(?P<dayofyear>\d{3})')],
            4:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})')],
            2:[ re.compile(r'(?ax)(?P<century>\d{2})')],
        },
        (False, True):{
            8:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})W(?P<weekofyear>\d{2})(?P<dayofweek>\d{1})')],
            7:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})W(?P<weekofyear>\d{2})')],
            6:[ re.compile(r'(?ax)(?P<year>\d{2})W(?P<weekofyear>\d{2})(?P<dayofweek>\d{1})')],
            5:[ re.compile(r'(?ax)(?P<year>\d{2})W(?P<weekofyear>\d{2})')]
        },
        (True, False):{
            10:[re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})-(?P<month>\d{2})-(?P<dayofmonth>\d{2})')],
            8:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})-(?P<dayofyear>\d{3})'),
                re.compile(r'(?ax)(?P<year>\d{2})-(?P<month>\d{2})-(?P<dayofmonth>\d{2})')],
            7:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})-(?P<month>\d{2})'),
                re.compile(r'(?ax)--(?P<month>\d{2})-(?P<dayofmonth>\d{2})')],
            6:[ re.compile(r'(?ax)-(?P<year>\d{2})-(?P<month>\d{2})'),
                re.compile(r'(?ax)--(?P<month>\d{2})(?P<dayofmonth>\d{2})')],
            5:[ re.compile(r'(?ax)(?P<year>\d{2})-(?P<dayofyear>\d{3})'),
                re.compile(r'(?ax)-(?P<year>\d{2})(?P<month>\d{2})'),
                re.compile(r'(?ax)---(?P<dayofmonth>\d{2})')],
            4:[ re.compile(r'(?ax)--(?P<month>\d{2})'),
                re.compile(r'(?ax)-(?P<dayofyear>\d{3})')],
            3:[re.compile(r'(?ax)-(?P<year>\d{2})')]
        },
        (True, True):{
            10:[re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})-W(?P<weekofyear>\d{2})-(?P<dayofweek>\d{1})')],
            
            8:[ re.compile(r'(?ax)(?P<century>\d{2})(?P<year>\d{2})-W(?P<weekofyear>\d{2})'),
                re.compile(r'(?ax)(?P<year>\d{2})-W(?P<weekofyear>\d{2})-(?P<dayofweek>\d{1})'),
                re.compile(r'(?ax)-(?P<yearofdec>\d{1})-W(?P<weekofyear>\d{2})-(?P<dayofweek>\d{1})')],
            6:[ re.compile(r'(?ax)(?P<year>\d{2})-W(?P<weekofyear>\d{2})'),
                re.compile(r'(?ax)-(?P<yearofdec>\d{1})W(?P<weekofyear>\d{2})(?P<dayofweek>\d{1})'),
                re.compile(r'(?ax)-(?P<yearofdec>\d{1})-W(?P<weekofyear>\d{2})'),
                re.compile(r'(?ax)-W(?P<weekofyear>\d{2})-(?P<dayofweek>\d{1})')],
            5:[ re.compile(r'(?ax)-(?P<yearofdec>\d{1})W(?P<weekofyear>\d{2})'),
                re.compile(r'(?ax)-W(?P<weekofyear>\d{2})(?P<dayofweek>\d{1})')],
            4:[ re.compile(r'(?ax)-W(?P<weekofyear>\d{2})'),
                re.compile(r'(?ax)-W-(?P<dayofweek>\d{1})')]
        }
    }
    
    @classmethod
    def parse_iso(cls, value, expand_digits=None):
        """Parse an ISO date string in `value` and return an `isodate`
        object.
        
        Expanded Representation
        -----------------------
        An expanded representation is a special case where the number
        of agreed upon digits in the representation to be specified in
        `expand_digits`. If `expand_digits` is `None` (default) and
        the value matches an expanded format then a `ValueError` shall
        be thrown.
        """
        value_org = value
        expanded = None
        if expand_digits:
            width = expand_digits + 1
            expanded = int(value[:width])
            value = value[width:]
        rep_type = (('-' in value), ('W' in value))
        if len(value) not in cls.representations[rep_type]:
            raise ValueError('Invalid representation "{0}".'.format(value_org))
        for rep_re in cls.representations[rep_type][len(value)]:
            mo = rep_re.match(value)
            if mo:
                parts = ["century", "year", "month", "dayofmonth", "dayofyear", "weekofyear", "dayofweek"]
                parts = [(k, int(mo.groupdict()[k])) for k in parts if k in mo.groupdict()]
                return cls(expanded=expanded, **dict(parts))
        else:
            raise ValueError('Invalid representation "{0}".'.format(value_org))
    
    @classmethod
    def is_leap_year(cls, expanded=None, century=None, year=None):
        """This will determine if a year is a leap year. If any component
        of the current year is not given then that information is derived
        from today. For example if `century` is given as 18, but not `year`
        then if today is 2012 the calculated year will be 1812."""
        if century is None:
            century = isodate.today().iso_century
        if year is None:
            year = isodate.today().iso_year
        return (year % 4 == 0 and (century != 0 or century % 4 == 0))
    
    @classmethod
    def days_in_month(cls, expanded, century, year, month):
        leap = cls.is_leap_year(expanded, century, year)
        return cls.months[month][2 if leap else 1]
    
    @classmethod
    def days_in_year(cls, expanded, century, year):
        return 365 if not cls.is_leap_year(expanded, century, year) else 366
    
    def __str__(self):
        """This is the same as calling `isoformat`."""
        return self.isoformat()

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
    
    def __eq__(self, other):
        if isinstance(other, isodate):
            return (self.iso_expanded == other.iso_expanded and
                    self.iso_century == other.iso_century and
                    self.iso_year == other.iso_year and
                    self.iso_dayofyear == other.iso_dayofyear)
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
    
    @property
    def iso_implied(self):
        return self.__implied
    
    @iso_implied.setter
    def iso_implied(self, value):
        if value is None:
            pass
        elif isinstance(value, isodate): #or isinstance(value, isodatetime):
            pass
        elif isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
            value = isodate.fromdatetime(value)
        elif isinstance(value, str):
            value = isodate.parse_iso(value)
        elif isinstance(value, int):
            value = isodate.fromtimestamp(value)
        elif isinstance(value, float):
            value = isodate.fromtimestamp(float(value))
        elif isinstance(value, time.struct_time):
            value = isodate.fromtimestamp(time.mktime(value))
        elif isinstance(value, tuple):
            value = isodate.fromtimestamp(time.mktime(value))
        elif isinstance(value, list):
            value = isodate.fromtimestamp(time.mktime(tuple(value)))
        elif isinstance(value, dict):
            value = isodate.fromtimestamp(time.mktime(tuple(value.values)))
        else:
            parse_iso(str(value))
        
        self.__implied = value
        if self.__implied:
            # Set all implied values based on the class documentation
            
            self.__expanded = self.__orig_expanded
            if self.__orig_century:
                self.__century = self.__orig_century
            else:
                self.__century = self.__implied.__century
            if self.__orig_year:
                self.__year = self.__orig_year
            else:
                self.__year = self.__implied.__year
            
            self.__dayofyear = None
            self.__month = None
            self.__dayofmonth = None
            self.__weekyear = None
            self.__weekofyear = None
            self.__dayofweek = None
            
            def set_implied_values(self):
                (   self.__expanded, self.__century, self.__year,
                    self.__month, self.__dayofmonth,
                    self.__dayofyear,
                    self.__weekyear, self.__weekofyear, self.__dayofweek
                ) = self.compute_all_fields(
                        expanded=self.__expanded,
                        century=self.__century,
                        year=self.__year,
                        dayofyear=self.__dayofyear,
                        month=self.__month,
                        dayofmonth=self.__dayofmonth,
                        weekyear=self.__weekyear,
                        weekofyear=self.__weekofyear,
                        dayofweek=self.__dayofweek)
            
            if self.__orig_dayofyear:
                self.__dayofyear = self.__orig_dayofyear
                set_implied_values(self)
            elif self.__orig_month:
                self.__month = self.__orig_month
                if self.__orig_dayofmonth:
                    self.__dayofmonth = self.__orig_dayofmonth
                else:
                    self.__dayofmonth = self.__implied.__dayofmonth
                set_implied_values(self)
            elif self.__orig_dayofmonth:
                self.__dayofmonth = self.__orig_dayofmonth
                if self.__orig_month:
                    self.__month = self.__orig_month
                else:
                    self.__month = self.__implied.__month
                set_implied_values(self)
            elif self.__orig_weekyear:
                self.__weekyear = self.__orig_weekyear
                if self.__orig_weekofyear:
                    self.__weekofyear = self.__orig_weekofyear
                else:
                    self.__weekofyear = self.__implied.__weekofyear                    
                if self.__orig_dayofweek:
                    self.__dayofweek = self.__orig_dayofweek
                else:
                    self.__dayofweek = self.__implied.__dayofweek
                set_implied_values(self)
            elif self.__orig_weekofyear:
                if self.__orig_weekyear:
                    self.__weekyear = self.__orig_weekyear
                else:
                    self.__weekyear = self.__implied.__weekyear
                self.__weekofyear = self.__orig_weekofyear
                if self.__orig_dayofweek:
                    self.__dayofweek = self.__orig_dayofweek
                else:
                    self.__dayofweek = self.__implied.__dayofweek
                set_implied_values(self)
            elif self.__orig_dayofweek:
                if self.__orig_weekyear:
                    self.__weekyear = self.__orig_weekyear
                else:
                    self.__weekyear = self.__implied.__weekyear
                if self.__orig_weekofyear:
                    self.__weekofyear = self.__orig_weekofyear
                else:
                    self.__weekofyear = self.__implied.__weekofyear
                self.__dayofweek = self.__orig_dayofweek
                set_implied_values(self)
            else:
                self.__dayofyear = self.__implied.__dayofyear
                set_implied_values(self)
        else:
            # This will result in undefined behavior for many methods
            self.__expanded = self.__orig_expanded
            self.__century = self.__orig_century
            self.__year = self.__orig_year
            self.__dayofyear = self.__orig_dayofyear
            self.__month = self.__orig_month
            self.__dayofmonth = self.__orig_dayofmonth
            self.__weekyear = self.__orig_weekyear
            self.__weekofyear = self.__orig_weekofyear
            self.__dayofweek = self.__orig_dayofweek

        yby = self.__expanded * 10000 + self.__century * 100 + self.__year - 1
        dby = yby * 365 + yby // 4 - yby // 100 + yby // 400
        self.__ordinal = dby + self.__dayofyear
        self.__iso_leap_year = self.is_leap_year(self.__expanded, self.__century, self.__year)
        
        # Validate all values for consistency
        validate = [
            "expanded", "century", "year",
            "month", "dayofmonth",
            "dayofyear",
            "weekyear", "weekofyear", "dayofweek",
        ]
        for name in validate:
            orig = getattr(self, "_isodate__orig_" + name)
            actu = getattr(self, "_isodate__" + name)
            if orig is not None and orig != actu:
                raise ValueError("Inconsistent arguments to isodate.")
        
    
    @property
    def iso_leap_year(self):
        return self.__iso_leap_year
    
    @property
    def iso_expanded(self):
        return self.__expanded
    
    @property
    def iso_century(self):
        return self.__century
    
    @property
    def iso_year(self):
        return self.__year
    
    @property
    def iso_month(self):
        return self.__month
    
    @property
    def iso_dayofmonth(self):
        return self.__dayofmonth
    
    @property
    def iso_dayofyear(self):
        return self.__dayofyear
    
    @property
    def iso_weekyear(self):
        return self.__weekyear
    
    @property
    def __iso_weekyear100(self):
        return self.iso_weekyear % 100 if self.iso_weekyear is not None else None
    
    @property
    def __iso_weekyear10(self):
        return self.iso_weekyear % 10 if self.iso_weekyear is not None else None
    
    @property
    def iso_weekofyear(self):
        return self.__weekofyear
    
    @property
    def iso_dayofweek(self):
        return self.__dayofweek
    
    #The following is a binary coded key that follows the following pattern:
    # - iso_expanded
    # - iso_century
    # - iso_year
    # - iso_month
    # - iso_day
    # - iso_dayofyear
    # - iso_weekofyear
    # - iso_dayofweek
    # - basic (1) vs extended formatting (0)
    # - week of year uses year of decade
    code2fmt = {
        #Calendar Formatting
        0b0110110001:"{0.iso_century:02d}{0.iso_year:02d}{0.iso_month:02d}{0.iso_dayofmonth:02d}",
        0b0110110000:"{0.iso_century:02d}{0.iso_year:02d}-{0.iso_month:02d}-{0.iso_dayofmonth:02d}",
        0b0110100001:"{0.iso_century:02d}{0.iso_year:02d}-{0.iso_month:02d}",
        0b0110000001:"{0.iso_century:02d}{0.iso_year:02d}",
        0b0100000001:"{0.iso_century:02d}",
        0b0010110001:"{0.iso_year:02d}{0.iso_month:02d}{0.iso_dayofmonth:02d}",
        0b0010110000:"{0.iso_year:02d}-{0.iso_month:02d}-{0.iso_dayofmonth:02d}",
        0b0010100001:"-{0.iso_year:02d}{0.iso_month:02d}",
        0b0010100000:"-{0.iso_year:02d}-{0.iso_month:02d}",
        0b0010000001:"-{0.iso_year:02d}",
        0b0000110001:"--{0.iso_month:02d}{0.iso_dayofmonth:02d}",
        0b0000110000:"--{0.iso_month:02d}-{0.iso_dayofmonth:02d}",
        0b0000100001:"--{0.iso_month:02d}",
        0b0000100000:"--{0.iso_month:02d}",
        0b0000010001:"---{0.iso_dayofmonth:02d}",
        0b1110110001:"{0.iso_expanded:0=+2d}{0.iso_century:02d}{0.iso_year:02d}{0.iso_month:02d}{0.iso_dayofmonth:02d}",
        0b1110110000:"{0.iso_expanded:0=+2d}{0.iso_century:02d}{0.iso_year:02d}-{0.iso_month:02d}-{0.iso_dayofmonth:02d}",
        0b1110100001:"{0.iso_expanded:0=+2d}{0.iso_century:02d}{0.iso_year:02d}-{0.iso_month:02d}",
        0b1110000001:"{0.iso_expanded:0=+2d}{0.iso_century:02d}{0.iso_year:02d}",
        0b1100000001:"{0.iso_expanded:0=+2d}{0.iso_century:02d}",

        #Ordinal Formatting
        0b0110001001:"{0.iso_century:02d}{0.iso_year:02d}{0.iso_dayofyear:03d}",
        0b0110001000:"{0.iso_century:02d}{0.iso_year:02d}-{0.iso_dayofyear:03d}",
        0b0010001001:"{0.iso_year:02d}{0.iso_dayofyear:03d}",
        0b0010001000:"{0.iso_year:02d}-{0.iso_dayofyear:03d}",
        0b0000001001:"-{0.iso_dayofyear:03d}",
        0b1110001001:"{0.iso_expanded:0=+2d}{0.iso_century:02d}{0.iso_year:02d}{0.iso_dayofyear:03d}",
        0b1110001000:"{0.iso_expanded:0=+2d}{0.iso_century:02d}{0.iso_year:02d}-{0.iso_dayofyear:03d}",

        #Week Formatting
        0b0111000111:"{0.iso_weekyear:04d}W{0.iso_weekofyear:02d}{0.iso_dayofweek:01d}",
        0b0111000110:"{0.iso_weekyear:04d}-W{0.iso_weekofyear:02d}-{0.iso_dayofweek:01d}",
        0b0111000101:"{0.iso_weekyear:04d}W{0.iso_weekofyear:02d}",
        0b0111000100:"{0.iso_weekyear:04d}-W{0.iso_weekofyear:02d}",
        0b0011000111:"{0.__iso_weekyear100:02d}W{0.iso_weekofyear:02d}{0.iso_dayofweek:01d}",
        0b0011000110:"{0.__iso_weekyear100:02d}-W{0.iso_weekofyear:02d}-{0.iso_dayofweek:01d}",
        0b0011000101:"{0.__iso_weekyear100:02d}W{0.iso_weekofyear:02d}",
        0b0011000100:"{0.__iso_weekyear100:02d}-W{0.iso_weekofyear:02d}",
        0b0001000111:"{0.__iso_weekyear10:01d}W{0.iso_weekofyear:02d}{0.iso_dayofweek:01d}",
        0b0001000110:"{0.__iso_weekyear10:01d}-W{0.iso_weekofyear:02d}-{0.iso_dayofweek:01d}",
        0b0001000101:"{0.__iso_weekyear10:01d}W{0.iso_weekofyear:02d}",
        0b0001000100:"{0.__iso_weekyear10:01d}-W{0.iso_weekofyear:02d}",
        0b0000000111:"-W{0.iso_weekofyear:02d}{0.iso_dayofweek:01d}",
        0b0000000110:"-W{0.iso_weekofyear:02d}-{0.iso_dayofweek:01d}",
        0b0000000101:"-W{0.iso_weekofyear:02d}",
        0b0000000011:"{0.iso_dayofweek:01d}",
        0b1111000111:"{0.iso_expanded:0=+2d}{0.iso_weekyear:04d}W{0.iso_weekofyear:02d}{0.iso_dayofweek:01d}",
        0b1111000110:"{0.iso_expanded:0=+2d}{0.iso_weekyear:04d}-W{0.iso_weekofyear:02d}-{0.iso_dayofweek:01d}",
        0b1111000101:"{0.iso_expanded:0=+2d}{0.iso_weekyear:04d}W{0.iso_weekofyear:02d}",
        0b1111000100:"{0.iso_expanded:0=+2d}{0.iso_weekyear:04d}-W{0.iso_weekofyear:02d}",
    }

    def isoformat(self, representation=CALENDAR, basic=False,
                reduced=None, truncated=None, expanded=True):
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
                    - `reduced=MONTH` for specific year and month §5.2.1.3 (b)
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
            
                - `DECADE` for year, week, and day in an implied century §5.2.3.3 (a).
                    - `reduced=WEEKOFYEAR` for year and week in an implied century §5.2.3.3 (b)
            
                - `YEAR` for year of implied decade, week, and day §5.2.3.3 (c).
                    - `reduced=WEEKOFYEAR` for year of implied decade and week §5.2.3.3 (d)
                
                - `WEEKOFYEAR` for week and day of implied year §5.2.3.3 (e).
                    - `reduced=WEEKOFYEAR` for week only of implied year §5.2.3.3 (f)
            
                - `DAYOFWEEK` for day of an implied week §5.2.3.3 (g).
        
        Expanded representations are assumed and will be created if
        `expanded` is true and `iso_expanded` is not 0. If `expanded`
        is false then an expanded represenation will not be created.
        No truncation is allowed in an expanded representation so if
        a truncated respresentation is selected then expanded is turned
        off.
        
        This will duck type to `datetime.date.isoformat()` if called with
        no arguments.
        """
        if reduced is None:
            reduced = (0b1111111111, 0b1111111111)
        if truncated is None:
            truncated = (0b1111111111, 0b1111111111)
        
        code = representation & reduced[0] & truncated[1]
        if not basic:
            code = code & 0b1111111110
        if not (expanded and self.iso_expanded):
            code = code & 0b0111111111
        if not basic and code not in self.code2fmt:
            code = code | 0b0000000001
        if code not in self.code2fmt:
            __log__.debug("{0:b}".format(code))
            raise ValueError("Invalid ISO 8601 date representation.")
        fmt = self.code2fmt[code]
        return fmt.format(self)
    
    
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
    
    def replace(self, year=None, month=None, day=None):
        e = self.iso_expanded
        c = self.iso_century
        y = self.iso_year
        m = self.iso_month
        dom = self.iso_dayofmonth
        doy = self.iso_dayofyear
        wy = self.iso_weekyear
        woy = self.iso_weekofyear
        dow = self.iso_dayofweek
        if year:
            c = year // 100
            y = year % 100
            wy = None
        if month:
            m = month
            doy = None
            woy = None
            dow = None
        if day:
            dom = day
            doy = None
            dow = None
        ret = isodate(expanded=e, century=c, year=y,
                month=m, dayofmonth=dom,
                dayofyear=doy,
                weekyear=wy, weekofyear=woy, dayofweek=dow)
        return ret
    
    def timetuple(self):
        return (self.year, self.month, self.day, 0, 0, 0, self.weekday(), self.iso_dayofyear, -1)
    
    def toordinal(self):
        return self.__ordinal
    
    def weekday(self):
        return self.__dayofweek - 1
    
    def isoweekday(self):
        return self.__dayofweek
    
    def isocalendar(self):
        return (self.__weekyear, self.__weekofyear, self.__dayofweek)
        
    def ctime(self):
        return self.strftime("%a %b %d %H:%M:%S %Y")
    
    def strftime(self, format):
        return time.strftime(format, self.timetuple())


### Initialize the class
isodate.today()


