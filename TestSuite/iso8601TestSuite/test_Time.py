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

class TestTime(unittest.TestCase):
    """This will test ISO 8601 §5.3 time parsing and formatting."""
    
    def assert_time(self, basic, extended, reduced=None, truncated=None,
            hour=None, minute=None, second=None,
            decimal=None, preferred_mark=True,
            tz=None):
        
        test = isotime.parse_iso(basic)
        self.assertEqual(hour, test.hour)
        self.assertEqual(minute, test.minute)
        self.assertEqual(second, test.second)
        self.assertEqual(decimal, test.microsecond)
        self.assertEqual(tz, test.tzinfo)
        
        fmt = "{0:02d}:{1:02d}:{2:02d}"
        if decimal:
            fmt = fmt + ".{3:06d}"
        if tz.total_seconds() == 0:
            fmt = fmt + "Z"
        elif tz.total_seconds() // 60 % 60 == 0:
            fmt = fmt + "{4:+2d}"
        else:
            fmt = fmt + "{4:+2d}:{5:2d}"
        isostr = fmt.format(
            hour, minute, second, decimal,
            tz.total_seconds() // 60 // 60, tz.total_seconds() // 60 % 60)
        self.assertEqual(isostr, str(test))
        self.assertEqual(isostr, test.iso_format())
        self.assertEqual(basic, test.iso_format(reduced=reduced, truncated=truncated))
        if extended:
            self.assertEqual(basic, test.iso_format(basic=False, reduced=reduced, truncated=truncated))
    
    @unittest.skip("Waiting for implementation.")
    def test_functionality(self):
        """Basic functaionality tests over all representations."""
        t1 = isotime.parse_iso("23:20:50")
        t2 = isotime.parse_iso("07:13:27")
        t3 = isotime.parse_iso("23:20:50")
        
        self.assertEqual(t1, t3)
        self.assertNotEqual(t1, t2)
        self.assertGreater(t1, t2)
        self.assertGreaterEqual(t1, t2)
        self.assertGreaterEqual(t1, t3)
        self.assertLess(t2, t1)
        self.assertLessEqual(t2, t1)
    
    @unittest.skip("Waiting for implementation.")
    def test_complete(self):
        """ISO 8601 §5.3.1.1 Complete representation."""
        self.assert_time("232050", "23:20:50", hour=23, minute=20, second=50)
    
    @unittest.skip("Waiting for implementation.")
    def test_reduced_hourminute(self):
        """ISO 8601 §5.3.1.2 (a) A specific hour and minute."""
        self.assert_time("2320", "23:20", hour=23, minute=20, reduced=MINUTE)
    
    @unittest.skip("Waiting for implementation.")
    def test_reduced_hour(self):
        """ISO 8601 §5.3.1.2 (b) A specific hour."""
        self.assert_time("23", None, hour=23, reduced=HOUR)
    
    @unittest.skip("Waiting for implementation.")
    def test_decimal_second(self):
        """ISO 8601 §5.3.1.3 (a) A specific hour, minute and second and a decimal fraction of the second."""
        self.assert_time("232050,3547", "23:20:50,3547", hour=23, minute=20, second=50, decimal=3547)
        self.assert_time("232050.3547", "23:20:50.3547", hour=23, minute=20, second=50, decimal=3547, preferred_mark=False)
    
    @unittest.skip("Waiting for implementation.")
    def test_decimal_minute(self):
        """ISO 8601 §5.3.1.3 (b) A specific hour and minute and a decimal fraction of the minute."""
        self.assert_time("2320,3547", "23:20,3547", hour=23, minute=20, decimal=3547, reduced=MINUTE)
        self.assert_time("2320.3547", "23:20.3547", hour=23, minute=20, decimal=3547, preferred_mark=False, reduced=MINUTE)

    @unittest.skip("Waiting for implementation.")
    def test_decimal_mour(self):
        """ISO 8601 §5.3.1.3 (c) A specific hour and a decimal fraction of the hour."""
        self.assert_time("23,3547", None, hour=23, decimal=3547, reduced=HOUR)
        self.assert_time("23.3547", None, hour=23, decimal=3547, preferred_mark=False, reduced=HOUR)
    
    @unittest.skip("Waiting for implementation.")
    def test_truncated_minutesecond(self):
        """ISO 8601 §5.3.1.4 (a) A specific minute and second of the implied hour."""
        self.assert_time("-2050", "-20:50", minute=20, second=50, truncated=MINUTE)
    
    @unittest.skip("Waiting for implementation.")
    def test_truncated_minute(self):
        """ISO 8601 §5.3.1.4 (b) A specific minute of the implied hour."""
        self.assert_time("-20", None, minute=20, truncated=MINUTE, reduced=MINUTE)
    
    @unittest.skip("Waiting for implementation.")
    def test_truncated_second(self):
        """ISO 8601 §5.3.1.4 (c) A specific second of the implied minute."""
        self.assert_time("--50", None, second=50, truncated=SECOND)
    
    @unittest.skip("Waiting for implementation.")
    def test_truncated_minuteseconddecimal(self):
        """ISO 8601 §5.3.1.4 (d) A specific minute and second of the implied hour and decimal fraction of the second."""
        self.assert_time("-2050,3547", "-20:50,3547", minute=20, second=50, decimal=3547, truncated=MINUTE)
        self.assert_time("-2050.3547", "-20:50.3547", minute=20, second=50, decimal=3547, preferred_mark=False, truncated=MINUTE)
    
    @unittest.skip("Waiting for implementation.")
    def test_truncated_minutedecimal(self):
        """ISO 8601 §5.3.1.4 (e) A specific minute of the implied hour and decimal fraction of the minute."""
        self.assert_time("-20,3547", "-20,3547", minute=20, decimal=3547, truncated=MINUTE, reduced=MINUTE)
        self.assert_time("-20.3547", None, minute=20, decimal=3547, preferred_mark=False, truncated=MINUTE, reduced=MINUTE)
    
    @unittest.skip("Waiting for implementation.")
    def test_truncated_seconddecimal(self):
        """ISO 8601 §5.3.1.4 (f) A specific second of the implied minute and decimal fraction of the second."""
        self.assert_time("--50,3547", None, second=50, decimal=3547, truncated=SECOND)
        self.assert_time("--50.3547", None, second=50, decimal=3547, preferred_mark=False, truncated=SECOND)
    
    @unittest.skip("Waiting for implementation.")
    def test_utf(self):
        """ISO 8601 §5.3.3 Coordinated Universal Time (UTC)"""
        utc = datetime.timedelta(hours=0)
        
        self.assert_time("232050Z", "23:20:50Z", hour=23, minute=20, second=50, tz=utc)
        self.assert_time("2320Z", "23:20Z", hour=23, minute=20, tz=utc, reduced=MINUTE)
        self.assert_time("23Z", None, hour=23, tz=utc, reduced=HOUR)
        self.assert_time("232050,3547Z", "23:20:50,3547Z", hour=23, minute=20, second=50, decimal=3547, tz=utc)
        self.assert_time("232050.3547Z", "23:20:50.3547Z", hour=23, minute=20, second=50, decimal=3547, preferred_mark=False, tz=utc)
        self.assert_time("2320,3547Z", "23:20,3547Z", hour=23, minute=20, decimal=3547, tz=utc, reduced=MINUTE)
        self.assert_time("2320.3547Z", "23:20.3547Z", hour=23, minute=20, decimal=3547, preferred_mark=False, tz=utc, reduced=MINUTE)
        self.assert_time("23,3547Z", None, hour=23, decimal=3547, tz=utc, reduced=HOUR)
        self.assert_time("23.3547Z", None, hour=23, decimal=3547, preferred_mark=False, tz=utc, reduced=HOUR)
        
        self.assertRaises(ValueError, isotime.parse_iso, "-2050Z")
        self.assertRaises(ValueError, isotime.parse_iso, "-20:50Z")
        self.assertRaises(ValueError, isotime.parse_iso, "-20Z")
        self.assertRaises(ValueError, isotime.parse_iso, "--50Z")
        self.assertRaises(ValueError, isotime.parse_iso, "-20Z")
        
        self.assertRaises(ValueError, isotime.parse_iso, "-2050,3547Z")
        self.assertRaises(ValueError, isotime.parse_iso, "-20:50,3547Z")
        self.assertRaises(ValueError, isotime.parse_iso, "-20,3547Z")
        self.assertRaises(ValueError, isotime.parse_iso, "--50,3547Z")
    
    @unittest.skip("Waiting for implementation.")
    def test_tz(self):
        """ISO 8601 §5.3.4 Local time and Coordinated Universal Time."""
        tzh = datetime.timedelta(hours=1)
        tzm = datetime.timedelta(hours=1, minutes=27)
        
        self.assert_time("232050+0127", "23:20:50+01:27", hour=23, minute=20, second=50, tz=tzm)
        self.assert_time("232050+01", "23:20:50+01", hour=23, minute=20, second=50, tz=tzh)
        self.assert_time("232050,3547+0127", "23:20:50,3547+01:27", hour=23, minute=20, second=50, decimal=3547, tz=tzm)
        self.assert_time("232050.3547+01", "23:20:50.3547+01", hour=23, minute=20, second=50, decimal=3547, preferred_mark=False, tz=tzh)

        self.assert_time("2320+0127", "23:20+01:27", hour=23, minute=20, second=50, reduced=MINUTE, tz=tzm)
        self.assert_time("2320+01", "23:20+01", hour=23, minute=20, second=50, reduced=MINUTE, tz=tzh)
        self.assert_time("2320,3547+0127", "23:20,3547+01:27", hour=23, minute=20, second=50, decimal=3547, reduced=MINUTE, tz=tzm)
        self.assert_time("2320.3547+01", "23:20.3547+01", hour=23, minute=20, second=50, decimal=3547, preferred_mark=False, reduced=MINUTE, tz=tzh)

        self.assert_time("23+0127", "23+01:27", hour=23, minute=20, second=50, reduced=HOUR, tz=tzm)
        self.assert_time("23+01", None, hour=23, minute=20, second=50, reduced=HOUR, tz=tzh)
        self.assert_time("23,3547+0127", "23,3547+01:27", hour=23, minute=20, second=50, decimal=3547, reduced=HOUR, tz=tzm)
        self.assert_time("23.3547+01", None, hour=23, minute=20, second=50, decimal=3547, preferred_mark=False, reduced=HOUR, tz=tzh)

        self.assertRaises(ValueError, isotime.parse_iso, "-2050+0127")
        self.assertRaises(ValueError, isotime.parse_iso, "-20:50+0127")
        self.assertRaises(ValueError, isotime.parse_iso, "-20+0127")
        self.assertRaises(ValueError, isotime.parse_iso, "--50+0127")
        self.assertRaises(ValueError, isotime.parse_iso, "-20+0127")
        
        self.assertRaises(ValueError, isotime.parse_iso, "-2050,3547+0127")
        self.assertRaises(ValueError, isotime.parse_iso, "-20:50,3547+0127")
        self.assertRaises(ValueError, isotime.parse_iso, "-20,3547+0127")
        self.assertRaises(ValueError, isotime.parse_iso, "--50,3547+0127")




