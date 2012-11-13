#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""RFC6350 Unit Test."""
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

import sys
import os
import io
import string
import datetime
import unittest

from pyietflib.rfc6350 import *
import pyietflib.iso8601 as iso8601

def encode_to_stream(s, eol='\r\n', maxline=75, foldws=" "):
    """Convert all native linesep to the `eol` value (testing), encode
    to UTF-8, and fold the lines to `maxline` length then return a
    byte stream. On a folded line the leading whitespace is a single
    space, but may be changed with `foldws`."""
    
    def generator(s, eol, maxline, foldws):
        fold = (eol + foldws).encode("UTF-8")
        eol = eol.encode("UTF-8")
        linelen = 0
        for c in s:
            if c == os.linesep:
                ybytes = eol
                linelen = 0
            elif c in string.whitespace:
                ybytes = c.encode("UTF-8")
            elif linelen > maxline:
                ybytes = fold + c.encode("UTF-8")
                linelen = 0
            else:
                ybytes = c.encode("UTF-8")
        
            for b in ybytes:
                linelen = linelen + 1
                yield b
    
    gen = generator(s, eol, maxline, foldws)
    bytea = bytearray(gen)
    return io.BytesIO(bytea)


class vCardTest(unittest.TestCase):
    
    def test_line_folding(self):
        """Test a vCard line delimiting and folding."""
        x = parse_vcard(io.BytesIO(b"""
BEGIN:VCARD
VERSION:4.0
NOTE:This is a long descrip
 \t tion that exists o
  n a long line. Price is 27\xc2
    \xa2 or 27 cents.
END:VCARD
""".replace(os.linesep.encode("UTF-8"), b'\r\n')))
        self.assertEquals("This is a long description that exists on a long line. Price is 27¢ or 27 cents.", x["NOTE"][0].value)
    
    
    @unittest.skip("This is causing an 'int' object is not subscriptable error.")
    def test_encoding(self):
        self.assertRaises(ValueError, parse_vcard, b"""\xc2\xc0\r\n""")
    
    
    
    def test_eol(self):
        """Test that vCard handles EOL correctly."""
        v = """
BEGIN:VCARD
VERSION:4.0
NOTE:Checking how various EOL are handl
 ed on long lines.
END:VCARD
"""
        self.assertIsNotNone(parse_vcard(encode_to_stream(v, eol='\r\n')))
        self.assertRaises(ValueError, parse_vcard, encode_to_stream(v, eol='\r'))
        self.assertRaises(ValueError, parse_vcard, encode_to_stream(v, eol='\n'))
    
    
    
    def test_no_BEGIN(self):
        """Test that vCard handles EOL correctly."""
        self.assertRaises(ValueError, parse_vcard, encode_to_stream("""
BEGINXYZ:VCARD
VERSION:4.0
NOTE:Missing BEGIN
END:VCARD
"""))



    def test_no_VERSION(self):
        """Test that vCard handles EOL correctly."""
        self.assertRaises(ValueError, parse_vcard, encode_to_stream("""
BEGIN:VCARD
NOTE:Missing Version
END:VCARD
"""))



    def test_invalid_version(self):
        """Test that vCard handles EOL correctly."""
        self.assertRaises(ValueError, parse_vcard, encode_to_stream("""
BEGIN:VCARD
VERSION:3.0
NOTE:Invalid Version
END:VCARD
"""))



    def test_no_END(self):
        """Test that vCard handles EOL correctly."""
        self.assertRaises(ValueError, parse_vcard, encode_to_stream("""
BEGIN:VCARD
VERSION:4.0
NOTE:Mising END
"""))



    def test_no_contentline(self):
        """Test for empty vCard."""
        self.assertRaises(ValueError, parse_vcard, encode_to_stream("""
BEGIN:VCARD
VERSION:4.0
END:VCARD
"""))



    def test_minimal(self):
        """Test a vCard with only required parameters and properties."""
        x = parse_vcard(encode_to_stream("""
BEGIN:VCARD
VERSION:4.0
NOTE:This is a minimal vCard.
END:VCARD
"""))
        self.assertEquals("4.0", x.version)
        self.assertEquals("This is a minimal vCard.", x["NOTE"][0].value)



    def test_params(self):
        """Test a vCard with only required parameters and properties."""
        x = parse_vcard(encode_to_stream("""
BEGIN:VCARD
VERSION:4.0
NOTE;VALUE=uri;TYPE="work,voice";PREF=1:This is a minimal vCard with params.
END:VCARD
"""))
        self.assertEquals("4.0", x.version)
        self.assertEquals("This is a minimal vCard with params.", x["NOTE"][0].value)
        
        note = x["NOTE"][0]
        
        self.assertEquals(3, len(note.parameters))
        self.assertEquals("VALUE", note.parameters[0].name)
        self.assertEquals("uri", note.parameters[0].value)

        self.assertEquals("TYPE", note.parameters[1].name)
        self.assertEquals(["work", "voice"], note.parameters[1].value)

        self.assertEquals("PREF", note.parameters[2].name)
        self.assertEquals(1, note.parameters[2].value)


    @unittest.skip("Complete Complete First")
    def test_rfc_author(self):
        """Test RFC 6350 author's vCard."""
        x = parse_vcard(encode_to_stream("""
BEGIN:VCARD
VERSION:4.0
FN:Simon Perreault
N:Perreault;Simon;;;ing. jr,M.Sc.
BDAY:--0203
ANNIVERSARY:20090808T1430-0500
GENDER:M
LANG;PREF=1:fr
LANG;PREF=2:en
ORG;TYPE=work:Viagenie
ADR;TYPE=work:;Suite D2-630;2875 Laurier;
 Quebec;QC;G1V 2M2;Canada
TEL;VALUE=uri;TYPE="work,voice";PREF=1:tel:+1-418-656-9254;ext=102
TEL;VALUE=uri;TYPE="work,cell,voice,video,text":tel:+1-418-262-6501
EMAIL;TYPE=work:simon.perreault@viagenie.ca
GEO;TYPE=work:geo:46.772673,-71.282945
KEY;TYPE=work;VALUE=uri:
 http://www.viagenie.ca/simon.perreault/simon.asc
TZ:-0500
URL;TYPE=home:http://nomis80.org
END:VCARD
"""))
        self.assertEquals("4.0", x.version)
        self.assertEquals(1, len(x["LANG"][0].parameters))
        
        self.assertEquals("Simon Perreault", x["FN"][0].value)
        self.assertEquals(0, len(x["FN"][0].parameters))
        
        self.assertEquals("Perreault;Simon;;;ing. jr,M.Sc.", x["N"][0].value)
        self.assertEquals(0, len(x["N"][0].parameters))
        
        self.assertEquals(iso8601.isodate(month=2, dayofmonth=3), iso8601.isodate.parse_iso(x["BDAY"][0].value))
        self.assertEquals(0, len(x["BDAY"][0].parameters))
        
        self.assertEquals(iso8601.isodatetime(century=20, year=9, month=8, dayofmonth=8, hour=14, minute=30, tz=-5), iso8601.isodate.parse_iso(x["ANNIVERSARY"][0].value))
        self.assertEquals(0, len(x["ANNIVERSARY"][0].parameters))
        
        self.assertEquals("M", x["GENDER"][0].value)
        self.assertEquals(0, len(x["GENDER"][0].parameters))
        
        self.assertEquals("fr", x["LANG"][0].value)
        self.assertEquals(1, len(x["LANG"][0].parameters))
        self.assertEquals("PREF", x["LANG"][0].parameters[0].name)
        self.assertEquals("1", x["LANG"][0].parameters[0].value)
        
        self.assertEquals("en", x["LANG"][1].value)
        self.assertEquals(1, len(x["LANG"][0].parameters))
        self.assertEquals("PREF", x["LANG"][0].parameters[0].name)
        self.assertEquals("2", x["LANG"][0].parameters[0].value)
        
        self.assertEquals("Viagenie", x["ORG"][0].value)
        self.assertEquals(1, len(x["ORG"][0].parameters))
        self.assertEquals("TYPE", x["ORG"][0].parameters[0].name)
        self.assertEquals(["work"], x["ORG"][0].parameters[0].value)
        
        self.assertEquals("Suite D2-630;2875 Laurier;Quebec;QC;G1V 2M2;Canada", x["ADR"][0].value)
        self.assertEquals(1, len(x["ADR"][0].parameters))
        self.assertEquals("TYPE", x["ADR"][0].parameters[0].name)
        self.assertEquals(["work"], x["ADR"][0].parameters[0].value)
        
        self.assertEquals(rfc3966.TelURI("tel:+1-418-656-9254;ext=102"), x["TEL"][0].value)
        self.assertEquals(2, len(x["TEL"][0].parameters))
        self.assertEquals("VALUE", x["TEL"][0].parameters[0].name)
        self.assertEquals("uri", x["TEL"][0].parameters[0].value)
        self.assertEquals("TYPE", x["TEL"][0].parameters[0].name)
        self.assertEquals(["work","voice"], x["TEL"][0].parameters[0].value)
        
        self.assertEquals(rfc3966.TelURI("tel:+1-418-262-6501"), x["TEL"][1].value)
        self.assertEquals(2, len(x["TEL"][0].parameters))
        self.assertEquals("VALUE", x["TEL"][0].parameters[0].name)
        self.assertEquals("uri", x["TEL"][0].parameters[0].value)
        self.assertEquals("TYPE", x["TEL"][0].parameters[0].name)
        self.assertEquals(["work","cell","voice","video","text"], x["TEL"][0].parameters[0].value)
        
        self.assertEquals(rfc6068.MailtoURI("mailto:simon.perreault@viagenie.ca"), x["EMAIL"][0].value)
        self.assertEquals(1, len(x["EMAIL"][0].parameters))
        self.assertEquals("TYPE", x["EMAIL"][0].parameters[0].name)
        self.assertEquals(["work"], x["EMAIL"][0].parameters[0].value)
        
        self.assertEquals(rfc5870.GeoURI("geo:46.772673,-71.282945"), x["GEO"][0].value)
        self.assertEquals(1, len(x["GEO"][0].parameters))
        self.assertEquals("TYPE", x["GEO"][0].parameters[0].name)
        self.assertEquals(["work"], x["GEO"][0].parameters[0].value)
        
        self.assertEquals(rfc2616.HttpURL("http://www.viagenie.ca/simon.perreault/simon.asc"), x["KEY"][0].value)
        self.assertEquals(1, len(x["KEY"][0].parameters))
        self.assertEquals("TYPE", x["KEY"][0].parameters[0].name)
        self.assertEquals(["work"], x["KEY"][0].parameters[0].value)
        
        self.assertEquals("-0500", x["TZ"][0].value)
        
        self.assertEquals(rfc2616.HttpURL("http://nomis80.org"), x["URL"][0].value)
        self.assertEquals(1, len(x["URL"][0].parameters))
        self.assertEquals("TYPE", x["URL"][0].parameters[0].name)
        self.assertEquals(["home"], x["URL"][0].parameters[0].value)

