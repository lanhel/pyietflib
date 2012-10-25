#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""ISO 8601 Date Unit Test."""
__author__ = ('Lance Finn Helsten',)
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
__docformat__ = "reStructuredText en"

import datetime
import unittest

from pyietflib.iso8601 import *

class TestDateCalendar(unittest.TestCase):
    """This will test ISO 8601 §5.2.1 calendar date parsing and
    formatting."""
    
    def assert_date(self, basic, extended, reduced=None, truncated=None,
            expanded=None, century=None, year=None, month=None, dayofmonth=None):
        
        now = datetime.date(1967, 3, 13)
        
        expand_len = None if expanded is None else len(str(expanded))
        t_expanded = expanded if expanded is not None else 0
        t_century = century if century is not None else now.year // 100
        t_year = year if year is not None else now.year % 100
        t_month = month if month is not None else now.month
        t_dayofmonth = dayofmonth if dayofmonth is not None else now.day
        
        bdate = isodate.parse_iso(basic, expand_digits=expand_len)
        bdate.iso_implied = now
        
        self.assertEqual(t_expanded, bdate.iso_expanded)
        self.assertEqual(t_century, bdate.iso_century)
        self.assertEqual(t_year, bdate.iso_year)
        
        self.assertEqual(t_month, bdate.iso_month)
        self.assertEqual(t_dayofmonth, bdate.iso_dayofmonth)
        
        if expanded is None:
            self.assertEqual("{0:02d}{1:02d}-{2:02d}-{3:02d}".format(t_century, t_year, t_month, t_dayofmonth), bdate.isoformat())
            self.assertEqual("{0:02d}{1:02d}-{2:02d}-{3:02d}".format(t_century, t_year, t_month, t_dayofmonth), str(bdate))
            self.assertEqual("{0:02d}{1:02d}{2:02d}{3:02d}".format(t_century, t_year, t_month, t_dayofmonth), bdate.isoformat(basic=True))
        
        self.assertEqual(basic, bdate.isoformat(representation=CALENDAR,
                reduced=reduced, truncated=truncated, basic=True,
                expanded=(expanded is not None)))
        
        if extended:
            self.assertEqual(extended, bdate.isoformat(representation=CALENDAR,
                    reduced=reduced, truncated=truncated, basic=False,
                    expanded=(expanded is not None)))
            bdate = isodate.parse_iso(basic, expand_digits=expand_len)
            self.assertEqual(bdate, isodate.parse_iso(extended, expand_digits=expand_len))
    
    def test_computation(self):
        """Test the compuation methods for all ISO date fields."""
        
        self.assertEqual((0, 19, 66, 8, 29), isodate.calendar_from_ordinal(0, 19, 66, 241))
        self.assertEqual((0, 19, 66, 241), isodate.ordinal_from_calendar(0, 19, 66, 8, 29))
        
        self.assertRaises(ValueError, isodate.compute_all_fields, dayofyear=-1)
        self.assertRaises(ValueError, isodate.compute_all_fields, dayofyear=366)
        
        ### Check some basic day of year calculations
        self.assertEqual((0, 0, 1,  1,  1,   1,  0, 0, 1,  1, 1), isodate.compute_all_fields())
        self.assertEqual((0, 0, 1,  1,  1,   1,  0, 0, 1,  1, 1), isodate.compute_all_fields(dayofyear=1))
        self.assertEqual((0, 0, 1,  1,  2,   2,  0, 0, 1,  1, 2), isodate.compute_all_fields(dayofyear=2))
        self.assertEqual((0, 0, 1,  1,  3,   3,  0, 0, 1,  1, 3), isodate.compute_all_fields(dayofyear=3))
        self.assertEqual((0, 0, 1,  1,  4,   4,  0, 0, 1,  1, 4), isodate.compute_all_fields(dayofyear=4))
        self.assertEqual((0, 0, 1,  1,  5,   5,  0, 0, 1,  1, 5), isodate.compute_all_fields(dayofyear=5))
        self.assertEqual((0, 0, 1,  1,  6,   6,  0, 0, 1,  1, 6), isodate.compute_all_fields(dayofyear=6))
        self.assertEqual((0, 0, 1,  1,  7,   7,  0, 0, 1,  1, 7), isodate.compute_all_fields(dayofyear=7))
        self.assertEqual((0, 0, 1,  1,  8,   8,  0, 0, 1,  2, 1), isodate.compute_all_fields(dayofyear=8))
        self.assertEqual((0, 0, 1,  1, 30,  30,  0, 0, 1,  5, 2), isodate.compute_all_fields(dayofyear=30))
        self.assertEqual((0, 0, 1,  1, 31,  31,  0, 0, 1,  5, 3), isodate.compute_all_fields(dayofyear=31))
        self.assertEqual((0, 0, 1,  2,  1,  32,  0, 0, 1,  5, 4), isodate.compute_all_fields(dayofyear=32))
        self.assertEqual((0, 0, 1, 12, 29, 363,  0, 0, 1, 52, 6), isodate.compute_all_fields(dayofyear=363))
        self.assertEqual((0, 0, 1, 12, 30, 364,  0, 0, 1, 52, 7), isodate.compute_all_fields(dayofyear=364))
        self.assertEqual((0, 0, 1, 12, 31, 365,  0, 0, 1,  1, 1), isodate.compute_all_fields(dayofyear=365))
        self.assertEqual((0, 0, 2,  1,  1,   1,  0, 0, 2,  1, 2), isodate.compute_all_fields(year=2, dayofyear=1))
        self.assertEqual((0, 0, 2,  1,  2,   2,  0, 0, 2,  1, 3), isodate.compute_all_fields(year=2, dayofyear=2))
        self.assertEqual((0, 0, 2,  1,  3,   3,  0, 0, 2,  1, 4), isodate.compute_all_fields(year=2, dayofyear=3))
        
        ### Check the week calculations
        self.assertEqual((0, 0,  1,  1,  1,   1, 0, 0, 1,  1, 1), isodate.compute_all_fields(year=1))
        self.assertEqual((0, 0,  2,  1,  1,   1, 0, 0, 2,  1, 2), isodate.compute_all_fields(year=2))
        self.assertEqual((0, 0,  3,  1,  1,   1, 0, 0, 3,  1, 3), isodate.compute_all_fields(year=3))
        self.assertEqual((0, 0,  4,  1,  1,   1, 0, 0, 4,  1, 4), isodate.compute_all_fields(year=4))
        self.assertEqual((0, 0,  5,  1,  1,   1, 0, 0, 4, 53, 6), isodate.compute_all_fields(year=5))
        self.assertEqual((0, 0,  6,  1,  1,   1, 0, 0, 5, 52, 7), isodate.compute_all_fields(year=6))
        self.assertEqual((0, 0,  7,  1,  1,   1, 0, 0, 7,  1, 1), isodate.compute_all_fields(year=7))
        self.assertEqual((0, 0,  8,  1,  1,   1, 0, 0, 8,  1, 2), isodate.compute_all_fields(year=8))
        self.assertEqual((0, 0,  9,  1,  1,   1, 0, 0, 9,  1, 4), isodate.compute_all_fields(year=9))
        self.assertEqual((0, 0, 10,  1,  1,   1, 0, 0, 9, 53, 5), isodate.compute_all_fields(year=10))
        self.assertEqual((0, 0, 11,  1,  1,   1, 0, 1, 0, 52, 6), isodate.compute_all_fields(year=11))
        self.assertEqual((0, 0, 12,  1,  1,   1, 0, 1, 1, 52, 7), isodate.compute_all_fields(year=12))
        self.assertEqual((0, 0, 13,  1,  1,   1, 0, 1, 3,  1, 2), isodate.compute_all_fields(year=13))
        self.assertEqual((0, 0, 14,  1,  1,   1, 0, 1, 4,  1, 3), isodate.compute_all_fields(year=14))
        self.assertEqual((0, 0, 15,  1,  1,   1, 0, 1, 5,  1, 4), isodate.compute_all_fields(year=15))
        self.assertEqual((0, 0, 16,  1,  1,   1, 0, 1, 5, 53, 5), isodate.compute_all_fields(year=16))
        self.assertEqual((0, 0, 17,  1,  1,   1, 0, 1, 6, 52, 7), isodate.compute_all_fields(year=17))
        self.assertEqual((0, 0, 18,  1,  1,   1, 0, 1, 8,  1, 1), isodate.compute_all_fields(year=18))
        self.assertEqual((0, 0, 19,  1,  1,   1, 0, 1, 9,  1, 2), isodate.compute_all_fields(year=19))
        
        ### Check other calculations
        self.assertEqual((0, 19, 66, 8, 29, 241, 19, 6, 6, 35, 1), isodate.compute_all_fields(century=19, year=66, month=8, dayofmonth=29))
    
    def test_functionality(self):
        """Basic functionality tests over all representations."""
        test = isodate.parse_iso("1966-08-29")
        self.assertEqual(0, test.iso_expanded)
        self.assertEqual(19, test.iso_century)
        self.assertEqual(66, test.iso_year)
        self.assertEqual(8, test.iso_month)
        self.assertEqual(29, test.iso_dayofmonth)
        self.assertEqual(241, test.iso_dayofyear)
        self.assertEqual(19, test.iso_weekcentury)
        self.assertEqual(6, test.iso_weekdecade)
        self.assertEqual(6, test.iso_weekyearofdec)
        self.assertEqual(35, test.iso_weekofyear)
        self.assertEqual(1, test.iso_dayofweek)
        
        self.assertEqual(1966, test.year)
        self.assertEqual(8, test.month)
        self.assertEqual(29, test.day)
        self.assertEqual((1966, 8, 29, 0, 0, 0, 0, 241, -1), tuple(test.timetuple()))
        self.assertEqual(717942, test.toordinal())
        self.assertEqual(0, test.weekday())
        self.assertEqual(1, test.isoweekday())
        self.assertEqual((1966, 35, 1), test.isocalendar())
        self.assertEqual("1966-08-29", test.isoformat(representation=CALENDAR))
        self.assertEqual("19660829", test.isoformat(representation=CALENDAR, basic=True))
        self.assertEqual("1966-241", test.isoformat(representation=ORDINAL))
        self.assertEqual("1966241", test.isoformat(representation=ORDINAL, basic=True))
        self.assertEqual("1966-W35-1", test.isoformat(representation=WEEK))
        self.assertEqual("1966W351", test.isoformat(representation=WEEK, basic=True))
        self.assertEqual("Mon Aug 29 00:00:00 1966", test.ctime())
        self.assertEqual("Mon Aug 29 00:00:00 1966", test.strftime("%a %b %d %H:%M:%S %Y"))
        
        self.assertEqual("1966-08-29", str(test))
        self.assertEqual(b"\x00\x13\x42\x08\x1d", bytes(test))
        self.assertEqual("1966-08-29", "{0}".format(test))
        self.assertEqual("1966-08-29", "{0:s}".format(test))
        self.assertEqual("  1966-08-29", "{0:12c}".format(test))
        self.assertEqual("    19660829", "{0:>#12c}".format(test))
        self.assertEqual("1966-08-29  ", "{0:<12c}".format(test))
        self.assertEqual(" 1966-08-29 ", "{0:^12c}".format(test))
        self.assertEqual("   19660829  ", "{0:^#13c}".format(test))
        self.assertEqual("1966-08", "{0:.7c}".format(test))
        self.assertEqual("+01966-08-29", "{0:-c}".format(test))
        self.assertEqual("1966-241", "{0:o}".format(test))
        self.assertEqual("1966-W35-1", "{0:w}".format(test))
        
        testadd = test + datetime.timedelta(days=1)
        self.assertEqual(19, testadd.iso_century)
        self.assertEqual(66, testadd.iso_year)
        self.assertEqual(8, testadd.iso_month)
        self.assertEqual(30, testadd.iso_dayofmonth)
        self.assertEqual(242, testadd.iso_dayofyear)
        self.assertEqual(19, testadd.iso_weekcentury)
        self.assertEqual(6, testadd.iso_weekdecade)
        self.assertEqual(6, testadd.iso_weekyearofdec)
        self.assertEqual(35, testadd.iso_weekofyear)
        self.assertEqual(2, testadd.iso_dayofweek)
        
        testsub = test - datetime.timedelta(days=1)
        self.assertEqual(19, testadd.iso_century)
        self.assertEqual(66, testadd.iso_year)
        self.assertEqual(8, testadd.iso_month)
        self.assertEqual(28, testsub.iso_dayofmonth)
        self.assertEqual(240, testsub.iso_dayofyear)
        self.assertEqual(19, testsub.iso_weekcentury)
        self.assertEqual(6, testsub.iso_weekdecade)
        self.assertEqual(6, testsub.iso_weekyearofdec)
        self.assertEqual(34, testsub.iso_weekofyear)
        self.assertEqual(7, testsub.iso_dayofweek)
        
        testrep = test.replace(1967, 9, 3)
        self.assertIsNot(test, testrep)
        self.assertEqual(19, testrep.iso_century)
        self.assertEqual(67, testrep.iso_year)
        self.assertEqual(9, testrep.iso_month)
        self.assertEqual(3, testrep.iso_dayofmonth)
        self.assertEqual(246, testrep.iso_dayofyear)
        self.assertEqual(19, testrep.iso_weekcentury)
        self.assertEqual(6, testrep.iso_weekdecade)
        self.assertEqual(7, testrep.iso_weekyearofdec)
        self.assertEqual(35, testrep.iso_weekofyear)
        self.assertEqual(7, testrep.iso_dayofweek)

        self.assertRaises(ValueError, isodate, century=20, year=66, month=8, dayofmonth=29, dayofyear=241, weekofyear=35, dayofweek=1)
        self.assertRaises(ValueError, isodate, century=19, year=67, month=8, dayofmonth=29, dayofyear=241, weekofyear=35, dayofweek=1)
        self.assertRaises(ValueError, isodate, century=19, year=66, month=9, dayofmonth=29, dayofyear=241, weekofyear=35, dayofweek=1)
        self.assertRaises(ValueError, isodate, century=19, year=66, month=8, dayofmonth=30, dayofyear=241, weekofyear=35, dayofweek=1)
        self.assertRaises(ValueError, isodate, century=19, year=66, month=8, dayofmonth=29, dayofyear=242, weekofyear=35, dayofweek=1)
        self.assertRaises(ValueError, isodate, century=19, year=66, month=8, dayofmonth=29, dayofyear=241, weekofyear=36, dayofweek=1)
        self.assertRaises(ValueError, isodate, century=19, year=66, month=8, dayofmonth=29, dayofyear=241, weekofyear=35, dayofweek=2)
    
    def test_complete(self):
        """ISO 8601 §5.2.1.1 Complete representation."""
        self.assert_date("19660829", "1966-08-29", century=19, year=66, month=8, dayofmonth=29)
    
    def test_reduced_month(self):
        """ISO 8601 §5.2.1.2 (a) Representation with reduced precision."""
        self.assert_date("1966-08", None, reduced=MONTH, century=19, year=66, month=8)
    
    def test_reduced_year(self):
        """ISO 8601 §5.2.1.2 (b) Representation with reduced precision."""
        self.assert_date("1966", None, reduced=YEAR, century=19, year=66)
    
    def test_reduced_century(self):
        """ISO 8601 §5.2.1.2 (c) Representation with reduced precision."""
        self.assert_date("19", None, reduced=CENTURY, century=19)
    
    def test_truncated_implied_century_day(self):
        """ISO 8601 §5.2.1.3 (a) Truncated representations."""
        self.assert_date("660829", "66-08-29", truncated=YEAR, year=66, month=8, dayofmonth=29)
    
    def test_truncated_implied_century_yearmonth(self):
        """ISO 8601 §5.2.1.3 (b) Truncated representations."""
        self.assert_date("-6608", "-66-08", reduced=MONTH, truncated=YEAR, year=66, month=8)
    
    def test_truncated_implied_century_year(self):
        """ISO 8601 §5.2.1.3 (c) Truncated representations."""
        self.assert_date("-66", "-66", year=66, reduced=YEAR, truncated=YEAR)
    
    def test_truncated_implied_year_day(self):
        """ISO 8601 §5.2.1.3 (d) Truncated representations."""
        self.assert_date("--0829", "--08-29", month=8, dayofmonth=29, truncated=MONTH)
    
    def test_truncated_implied_year_month(self):
        """ISO 8601 §5.2.1.3 (e) Truncated representations."""
        self.assert_date("--08", None, month=8, reduced=MONTH, truncated=MONTH)
    
    def test_truncated_implied_month(self):
        """ISO 8601 §5.2.1.3 (f) Truncated representations."""
        self.assert_date("---29", None, dayofmonth=29, truncated=DAYOFMONTH)
    
    def test_expanded_day(self):
        """ISO 8601 §5.2.1.4 (a) Expanded representations."""
        self.assert_date("+2219660829", "+221966-08-29", expanded=22, century=19, year=66, month=8, dayofmonth=29)
    
    def test_expanded_month(self):
        """ISO 8601 §5.2.1.4 (b) Expanded representations."""
        self.assert_date("+221966-08", None, expanded=22, century=19, year=66, month=8, reduced=MONTH)
    
    def test_expanded_year(self):
        """ISO 8601 §5.2.1.4 (c) Expanded representations."""
        self.assert_date("+221966", "+221966", expanded=22, century=19, year=66, reduced=YEAR)
    
    def test_expanded_century(self):
        """ISO 8601 §5.2.1.4 (d) Expanded representations."""
        self.assert_date("+2219", "+2219", expanded=22, century=19, reduced=CENTURY)



class TestDateOrdinal(unittest.TestCase):
    """This will test ISO 8601 ordinal date parsing and formatting."""
    def assert_date(self, basic, extended, reduced=None, truncated=None,
            expanded=None, century=None, year=None, dayofyear=None):
        
        now = datetime.date(1967, 3, 13)
        
        expand_len = None if expanded is None else len(str(expanded))
        t_expanded = expanded if expanded is not None else 0
        t_century = century if century is not None else now.year // 100
        t_year = year if year is not None else now.year % 100
        t_dayofyear = dayofyear if dayofyear is not None else now.timetuple().tm_yday
        
        bdate = isodate.parse_iso(basic, expand_digits=expand_len)
        bdate.iso_implied = now
        
        self.assertEqual(t_expanded, bdate.iso_expanded)
        self.assertEqual(t_century, bdate.iso_century)
        self.assertEqual(t_year, bdate.iso_year)
        self.assertEqual(t_dayofyear, bdate.iso_dayofyear)
                
        self.assertEqual(basic, bdate.isoformat(representation=ORDINAL,
                reduced=reduced, truncated=truncated, basic=True,
                expanded=(expanded is not None)))
        
        if extended:
            self.assertEqual(extended, bdate.isoformat(representation=ORDINAL,
                    reduced=reduced, truncated=truncated, basic=False,
                    expanded=(expanded is not None)))
            bdate = isodate.parse_iso(basic, expand_digits=expand_len)
            self.assertEqual(bdate, isodate.parse_iso(extended, expand_digits=expand_len))

    def test_complete(self):
        """ISO 8601 §5.2.2.1 Complete representation."""
        self.assert_date("1966241", "1966-241", century=19, year=66, dayofyear=241)

    def test_truncated_implied_century(self):
        """ISO 8601 §5.2.2.2 (a) A specific year and day in the implied century."""
        self.assert_date("66241", "66-241", year=66, dayofyear=241, truncated=YEAR)

    def test_truncated_implied_year(self):
        """ISO 8601 §5.2.2.2 (b) Day only in the implied year."""
        self.assert_date("-241", None, dayofyear=241, truncated=DAYOFYEAR)

    def test_expanded_day(self):
        """ISO 8601 §5.2.2.3 Expanded representations."""
        self.assert_date("+221966241", "+221966-241", expanded=22, century=19, year=66, dayofyear=241)



class TestDateWeek(unittest.TestCase):
    """This will test ISO 8601 week date parsing and formatting."""
    def assert_date(self, basic, extended, reduced=None, truncated=None,
            expanded=None, century=None, decade=None, year=None,
            weekofyear=None, dayofweek=None):
        
        now = datetime.date(1967, 3, 13)
        
        expand_len = None if expanded is None else len(str(expanded))
        t_expanded = expanded if expanded is not None else 0
        t_century = century if century is not None else now.isocalendar()[0] // 100
        t_decade = decade if decade is not None else now.isocalendar()[0] % 100 // 10
        t_year = year if year is not None else now.isocalendar()[0] % 10
        t_weekofyear = weekofyear if weekofyear is not None else now.isocalendar()[1]
        t_dayofweek = dayofweek if dayofweek is not None else now.isocalendar()[2]
        
        bdate = isodate.parse_iso(basic, expand_digits=expand_len)
        bdate.iso_implied = now
                
        self.assertEqual(t_expanded, bdate.iso_expanded)
        self.assertEqual(t_century, bdate.iso_weekcentury)
        self.assertEqual(t_decade, bdate.iso_weekdecade)
        self.assertEqual(t_year, bdate.iso_weekyearofdec)
        self.assertEqual(t_weekofyear, bdate.iso_weekofyear)
        self.assertEqual(t_dayofweek , bdate.iso_dayofweek )
                
        self.assertEqual(basic, bdate.isoformat(representation=WEEK,
                reduced=reduced, truncated=truncated, basic=True,
                expanded=(expanded is not None)))
        
        if extended:
            self.assertEqual(extended, bdate.isoformat(representation=WEEK,
                    reduced=reduced, truncated=truncated, basic=False,
                    expanded=(expanded is not None)))
            bdate = isodate.parse_iso(basic, expand_digits=expand_len)
            self.assertEqual(bdate, isodate.parse_iso(extended, expand_digits=expand_len))

    def test_computation(self):
        """Test the compuation methods for all ISO date fields."""
        
        self.assertEqual((19, 6, 6, 35, 1), isodate.weekdate_from_ordinal(0, 19, 66, 241))
        self.assertEqual((0, 19, 66, 241), isodate.ordinal_from_weekdate(19, 6, 6, 35, 1))
        
        self.assertRaises(ValueError, isodate.compute_all_fields, weekofyear=-1)
        self.assertRaises(ValueError, isodate.compute_all_fields, weekofyear=54)
        
        ### Check some basic day of year calculations
        self.assertEqual((0, 19, 66, 8, 29, 240, 19, 6, 6, 35, 1),
            isodate.compute_all_fields(
                weekcentury=19, weekdecade=6, weekyearofdec=6,
                weekofyear=35, dayofweek=1))

    def test_complete(self):
        """ISO 8601 §5.2.3.1 Complete representation."""
        self.assert_date("1966W351", "1966-W35-1", century=19, decade=6, year=6, weekofyear=35, dayofweek=1)

    def test_reduced_week(self):
        """ISO 8601 §5.2.3.2 Reduced precision specific week."""
        self.assert_date("1966W35", "1966-W35", century=19, decade=6, year=6, weekofyear=35, reduced=WEEKOFYEAR)

    def test_truncated_implied_century_yearweekday(self):
        """ISO 8601 §5.2.3.3 (a) Year, week and day in the implied century."""
        self.assert_date("66W351", "66-W35-1", decade=6, year=6, weekofyear=35, dayofweek=1, truncated=DECADE, reduced=DAYOFWEEK)

    def test_truncated_implied_century_yearweek(self):
        """ISO 8601 §5.2.3.3 (b) Year and week only in the implied century."""
        self.assert_date("66W35", "66-W35", decade=6, year=6, weekofyear=35, truncated=DECADE, reduced=WEEKOFYEAR)
    
    def test_truncated_implied_decade_weekday(self):
        """ISO 8601 §5.2.3.3 (c) Year of the implied decade, week and day only."""
        self.assert_date("-6W351", "-6-W35-1", year=6, weekofyear=35, dayofweek=1, truncated=YEAR, reduced=DAYOFWEEK)

    def test_truncated_implied_decade_week(self):
        """ISO 8601 §5.2.3.3 (d) Year of the implied decade and week only."""
        self.assert_date("-6W35", "-6-W35", year=6, weekofyear=35, truncated=YEAR, reduced=WEEKOFYEAR)

    def test_truncated_implied_year_weekday(self):
        """ISO 8601 §5.2.3.3 (e) Week and day only of the implied year."""
        self.assert_date("-W351", "-W35-1", weekofyear=35, dayofweek=1, truncated=WEEKOFYEAR, reduced=DAYOFWEEK)

    def test_truncated_implied_year_week(self):
        """ISO 8601 §5.2.3.3 (f) Week only of the implied year."""
        self.assert_date("-W35", None, weekofyear=35, truncated=WEEKOFYEAR, reduced=WEEKOFYEAR)

    def test_truncated_implied_week(self):
        """ISO 8601 §5.2.3.3 (g) Day only of the implied week."""
        self.assert_date("-W-1", None, dayofweek=1, truncated=DAYOFWEEK, reduced=DAYOFWEEK)

    def test_expanded_day(self):
        """ISO 8601 §5.2.3.4 (a) A specific day."""
        self.assert_date("+221966W351", "+221966-W35-1", expanded=22, century=19, decade=6, year=6, weekofyear=35, dayofweek=1, reduced=DAYOFWEEK)

    def test_expanded_day(self):
        """ISO 8601 §5.2.3.4 (b) A specific week."""
        print("SPAM_+_+_+_+_+_+_+_+_+_+_+_+_+")
        self.assert_date("+221966W35", "+221966-W35", expanded=22, century=19, decade=6, year=6, weekofyear=35, reduced=WEEKOFYEAR)



