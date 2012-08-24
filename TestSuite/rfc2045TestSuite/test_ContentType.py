#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""RFC2045 Unit Test."""
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
import locale
import unittest

from rfc2045 import *

class TestContentType(unittest.TestCase):
    """This will test RFC 2045 Multipurpose Internet Mail Extensions
    (MIME) Part One: Format of Internet Message Bodies, section 5
    `Content-Type` header field."""
    
    def test_required_format(self):
        """Check that required parts of RFC2045 Content-Type are processed
        correctly."""
        x = ContentType('text/plain')
        self.assertEqual('text', x.type)
        self.assertEqual('plain', x.subtype)
        self.assertTrue(x.type_iana)
        self.assertFalse(x.type_ietf)
        self.assertFalse(x.type_private)
        self.assertTrue(x.subtype_iana)
        self.assertFalse(x.subtype_ietf)
        self.assertFalse(x.subtype_private)
        self.assertEqual('text/plain', str(x))
        
        y = ContentType('TeXt/pLaIn')
        self.assertEqual('text', y.type)
        self.assertEqual('plain', y.subtype)
        self.assertTrue(x.type_iana)
        self.assertFalse(y.type_ietf)
        self.assertFalse(y.type_private)
        self.assertTrue(y.subtype_iana)
        self.assertFalse(y.subtype_ietf)
        self.assertFalse(y.subtype_private)
        self.assertEqual('text/plain', str(x))
        
        self.assertEqual(x, y)
        
        self.assertRaises(ValueError, ContentType, 'text/')
        self.assertRaises(ValueError, ContentType, '/plain')
        self.assertRaises(ValueError, ContentType, 'te/xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te;xt/plain', rfc4288=True)
    
    def test_type_invalid_type(self):
        """Check that unknown types are rejected."""
        self.assertRaises(ValueError, ContentType, 'spam/eggs')
    
    def test_type_nonstandard(self):
        """Check that a non-standard (`X-` or `x-`) extension Content-Type
        is properly marked."""
        x = ContentType('x-spam/x-eggs')
        self.assertEqual('x-spam', x.type)
        self.assertEqual('x-eggs', x.subtype)
        self.assertFalse(x.type_iana)
        self.assertFalse(x.type_ietf)
        self.assertTrue(x.type_private)
        self.assertFalse(x.subtype_iana)
        self.assertFalse(x.subtype_ietf)
        self.assertTrue(x.subtype_private)
        
        x = ContentType('X-spam/X-eggs')
        self.assertEqual('x-spam', x.type)
        self.assertEqual('x-eggs', x.subtype)
        self.assertFalse(x.type_iana)
        self.assertFalse(x.type_ietf)
        self.assertTrue(x.type_private)
        self.assertFalse(x.subtype_iana)
        self.assertFalse(x.subtype_ietf)
        self.assertTrue(x.subtype_private)
        
    def test_parameters(self):
        """Check that parameters are correctly parsed."""
        x = ContentType('text/plain;charset=utf-8')
        self.assertEqual('text', x.type)
        self.assertEqual('plain', x.subtype)
        self.assertTrue(x.type_iana)
        self.assertFalse(x.type_ietf)
        self.assertFalse(x.type_private)
        self.assertTrue(x.subtype_iana)
        self.assertFalse(x.subtype_ietf)
        self.assertFalse(x.subtype_private)
        self.assertEqual('utf-8', x['charset'])
        self.assertEqual('text/plain;charset=utf-8', str(x))
        
        y = ContentType('text/plain;charset="UTF-8"')
        self.assertEqual(x, y)
        self.assertEqual('text/plain;charset=utf-8', str(y))
        
        z = ContentType('text/plain  \t\t   ;\t \t  \t\tcharset="uTf-8"')
        self.assertEqual(x, z)
        self.assertEqual('text/plain;charset=utf-8', str(z))
        
    
    def test_parameters_ctrls(self):
        """Check that parameter values with spaces or ctrls are properly
        rejected."""
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a\tb')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a\nb')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a\rb')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a\bb')
        
    def test_parameters_tspecials(self):
        """Check that parameter values with token special characters
        are properly detected if not in quoted string."""
        x = ContentType(r'text/plain;charset="()<>@,;:\/[]?="')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a(b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a)b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a<b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a>b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a@b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a,b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a;b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a:b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a\\b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a"b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a/b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a[b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a]b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a?b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a=b')
        self.assertRaises(ValueError, ContentType, 'text/plain;charset=a)b')
    
    def test_text_parameters(self):
        """Check valid and default parameters for `text/*`."""
        x = ContentType('text/plain')
        self.assertEqual('us-ascii', x['charset'])
    
    def test_image_parameters(self):
        """Check valid and default parameters for `image/*`."""
        x = ContentType('image/jpeg')
        self.assertEquals(0, len(x.keys()))
    
    def test_audio_parameters(self):
        """Check valid and default parameters for `audio/*`."""
        x = ContentType('audio/basic')
        self.assertEquals(0, len(x.keys()))
    
    def test_video_parameters(self):
        """Check valid and default parameters for `video/*`."""
        x = ContentType('video/mpeg')
        self.assertEquals(0, len(x.keys()))
    
    def test_application_parameters(self):
        """Check valid and default parameters for `application/*`."""
        x = ContentType('application/octet-stream')
        self.assertEqual(None, x['type'])
        self.assertEqual('8', x['padding'])
        
        x = ContentType('application/postscript')
        self.assertEquals(0, len(x.keys()))
    
    @unittest.skip("Untested for version 1")
    def test_message_parameters(self):
        """Check valid and default parameters for `message/*`."""
        pass
    
    @unittest.skip("Untested for version 1")
    def test_multipart_parameters(self):
        """Check valid and default parameters for `multipart/*`."""
        pass
    

class TestContentType_RFC4288(unittest.TestCase):
    """This will test the more restrictive RFC 4288 Media Type
    Specifications and Registration Procedures for type and subtype
    names."""
    
    def test_nolimits(self):
        """Check that the RFC2045 has no RFC4288 limits."""
        #x = ContentType('a'*128 + '/plain')
        #x = ContentType('text/' + 'a'*128)
        
        self.assertRaises(ValueError, ContentType, 'te@xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla@in', rfc4288=True)
    
    def test_limits(self):
        """Check that required parts of RFC4288 limits are handled."""
        x = ContentType('tE!#$&.+-^_Xt/pL!#$&.+-^_AiN', rfc4288=True)
        self.assertEqual('te!#$&.+-^_xt', x.type)
        self.assertEqual('pl!#$&.+-^_ain', x.subtype)
        
        self.assertRaises(ValueError, ContentType, 'a'*128 + '/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'aaaa/' + 'a'*128, rfc4288=True)
        
        self.assertRaises(ValueError, ContentType, 'te@xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te%xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te*xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te(xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te)xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te=xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te[xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te]xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te{xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te}xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te|xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te\\xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te:xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, "te'xt/plain", rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te"xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te<xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te>xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te,xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te~xt/plain', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'te`xt/plain', rfc4288=True)
        
        self.assertRaises(ValueError, ContentType, 'text/pla@in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla%in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla*in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla(in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla)in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla[in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla]in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla{in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla}in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla|in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla//in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla:in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, "text/pla'in", rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla"in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla<in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla>in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla,in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla~in', rfc4288=True)
        self.assertRaises(ValueError, ContentType, 'text/pla`in', rfc4288=True)
        

