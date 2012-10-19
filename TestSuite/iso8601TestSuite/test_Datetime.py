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

class TestDatetime(unittest.TestCase):
    """This will test ISO 8601 §5.4 date and time combinations. This does
    not test date or time in detail, only that they are created."""
    
    def assert_datetime(self, date, time, value):
        x = isodatetime.parse_iso(value)
        self.assertEqual(date, x.date())
        self.assertEqual(time, x.time())
    
    def test_functionality(self):
        """Basic functionality tests over all representations."""
        date = datetime.date(1966, 8, 29)
        time = datetime.time(12, 35, 32, 0, datetime.timezone.utc)
        dt  = datetime.datetime(1966, 8, 29, 12, 35, 32, 0, datetime.timezone.utc)
        
        self.assertEqual(dt, isodatetime(
            century=19, year=66, month=8, dayofmonth=29,
            hour=12, minute=35, second=32, tzinfo=datetime.timezone.utc))
        self.assertEqual(dt, isodatetime(
            century=19, year=66, dayofyear=241,
            hour=12, minute=35, second=32, tzinfo=datetime.timezone.utc))
        self.assertEqual(dt, isodatetime(
            weekcentury=19, weekdecade=6, weekyearofdec=6, weekofyear=35, dayofweek=1,
            hour=12, minute=35, second=32, tzinfo=datetime.timezone.utc))
        
        test = isodatetime(century=19, year=66, month=8, day=29,
                hour=5, minute=35, second=32,
                tzinfo=datetime.timezone(datetime.timedelta(hours=-6)))
        
        self.assertEqual(1966, test.year)
        self.assertEqual(8, test.month)
        self.assertEqual(29, test.day)
        self.assertEqual((1966, 8, 29, 0, 0, 0, 0, 241, -1), tuple(test.timetuple()))
        self.assertEqual(717942, test.toordinal())
        self.assertEqual(0, test.weekday())
        self.assertEqual(1, test.isoweekday())
        self.assertEqual((1966, 35, 1), test.isocalendar())
        self.assertEqual("1966-08-29T05:35:32-06:00", str(test))
        self.assertEqual("1966-08-29T05:35:32-06:00", test.isoformat())
        self.assertEqual("1966-08-29T05:35:32-06:00", test.isoformat(representation=CALENDAR))
        self.assertEqual("19660829T053532-0600", test.isoformat(representation=CALENDAR, basic=True))
        self.assertEqual("1966-241T05:35:32-06:00", test.isoformat(representation=ORDINAL))
        self.assertEqual("1966241T053532-0600", test.isoformat(representation=ORDINAL, basic=True))
        self.assertEqual("1966-W35-1T05:35:32-06:00", test.isoformat(representation=WEEK))
        self.assertEqual("1966W351T053532-0600", test.isoformat(representation=WEEK, basic=True))
        self.assertEqual("Mon Aug 29 05:35:32 1966", test.ctime())
        self.assertEqual("Mon Aug 29 05:35:32 1966", test.strftime("%a %b %d %H:%M:%S %Y"))
        
        self.assertEqual(datetime.datetime.today(), isodatetime.today())
        self.assertEqual(datetime.datetime.now(), isodatetime.now())
        self.assertEqual(datetime.datetime.utcnow(), isodatetime.utcnow())
        self.assertEqual(datetime.datetime.fromtimestamp(453265), isodatetime.fromtimestamp(453265))
        self.assertEqual(datetime.datetime.utcfromtimestamp(453265), isodatetime.utcfromtimestamp(453265))
        self.assertEqual(datetime.datetime.fromordinal(21234), isodatetime.utcfromtimestamp(21234))
        self.assertEqual(datetime.datetime.combine(date, time), isodatetime.combine(date, time))
        self.assertEqual(
            datetime.datetime.strptime("Mon Aug 29 05:35:32 1966", "%a %b %d %H:%M:%S %Y"),
            isodatetime.strptime("Mon Aug 29 05:35:32 1966", "%a %b %d %H:%M:%S %Y"))

    def test_complete(self):
        """ISO 8601 §5.4.1 Complete representation."""
        date = datetime.date(1966, 8, 29)
        timeutc = datetime.time(12, 35, 32, 0, datetime.timezone.utc)
        timesix = datetime.time( 5, 35, 32, 0, datetime.timezone(datetime.timedelta(hours=-6)))
        timeloc = datetime.time( 5, 35, 32, 0)
        
        self.assert_datetime(date, timeloc, "19660829T053532")
        self.assert_datetime(date, timeutc, "19660829T123532Z")
        self.assert_datetime(date, timesix, "19660829T053532-0600")
        self.assert_datetime(date, timesix, "19660829T053532-06")
        self.assert_datetime(date, timeloc, "1966-08-29T05:35:32")
        self.assert_datetime(date, timeutc, "1966-08-29T12:35:32Z")
        self.assert_datetime(date, timesix, "1966-08-29T05:35:32-06:00")
        self.assert_datetime(date, timesix, "1966-08-29T05:35:32-06")
        
        self.assert_datetime(date, timeloc, "1966241T053532")
        self.assert_datetime(date, timeutc, "1966241T123532Z")
        self.assert_datetime(date, timesix, "1966241T053532-0600")
        self.assert_datetime(date, timesix, "1966241T053532-06")
        self.assert_datetime(date, timeloc, "1966-241T05:35:32")
        self.assert_datetime(date, timeutc, "1966-241T12:35:32Z")
        self.assert_datetime(date, timesix, "1966-241T05:35:32-0600")
        self.assert_datetime(date, timesix, "1966-241T05:35:32-06")

        print("SPAM~_~_~~_~__~_~_~_~_~~_~_~_~_~_~_~_")
        self.assert_datetime(date, timeloc, "1966W351T053532")
        self.assert_datetime(date, timeutc, "1966W351T123532Z")
        self.assert_datetime(date, timesix, "1966W351T053532-0600")
        self.assert_datetime(date, timesix, "1966W351T053532-06")
        self.assert_datetime(date, timeloc, "1966-W35-1T05:35:32")
        self.assert_datetime(date, timeutc, "1966-W35-1T12:35:32Z")
        self.assert_datetime(date, timesix, "1966-W35-1T05:35:32-0600")
        self.assert_datetime(date, timesix, "1966-W35-1T05:35:32-06")


