#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""ERChime HTTP validation system."""
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

__all__ = ["HTTPValidationMethods", "HTTPValidationHeader"]

import sys
import os
import io
import time
import urllib
import http.client
import unittest
import string
import base64
import binascii


class HTTPValidationHeader():
    """Mixin class that will aid in validating common HTTP response
    headers.
    
    .. WARNING::
       This should only be used with classes that inherit from
       ``unittest.TestCase``.
    """
    
    def validate_header_server(self, resp):
        """Validate the ``Server`` header of the HTTP response.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        """
        self.assertIn("Server", resp.info())
        self.assertEquals("erchime/1.0 Python/3.2", resp.info()['Server'])

    
    def validate_header_date(self, resp, deltamax=1.0):
        """Validate the ``Date`` header of the HTTP response.
        
        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        deltamax
            The maximum variation between the current time and the time
            in the header. The default is 1.0 s.
        """
        self.assertIn("Date", resp.info())
        hstp = time.strptime(resp.info()['Date'], "%a, %d %b %Y %H:%M:%S %Z")
        cstp = time.gmtime()
        self.assertAlmostEqual(time.mktime(cstp), time.mktime(hstp), delta=deltamax)
    
    
    def validate_header_dnt(self, resp):
        """Validate the ``DNT`` header of the HTTP response.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        """
        self.assertIn("DNT", resp.info())
        self.assertEquals("0", resp.info()['DNT'])

    
    def validate_header_p3p(self, resp):
        """Validate the ``P3P`` header of the HTTP response.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        """
        self.assertIn("P3P", resp.info())
        self.assertEquals('policyref="http://localhost:8008/w3c/p3p.xml"', resp.info()['P3P'])
            
    
    def validate_header_x_powered_by(self, resp):
        """Validate the ``X-Powered-By`` header of the HTTP response.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        """
        self.assertIn("X-Powered-By", resp.info())
        self.assertEquals("Python/3.2", resp.info()['X-Powered-By'])
            
    
    def validate_header_last_modified(self, resp, testdate=None):
        """Validate the ``Last-Modified`` header of the HTTP response for
        proper format, and that it is before the given time.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        testdate
            Timestamp the last modified header should be less than or
            equal to. If ``None`` then current time is used.
        """
        self.assertIn("Last-Modified", resp.info())
        hstp = time.strptime(resp.info()['Last-Modified'], "%a, %d %b %Y %H:%M:%S %Z")
        if testdate is None:
            testdate = time.gmtime()
        self.assertGreaterEqual(time.mktime(testdate), time.mktime(hstp))
    
    
    def validate_header_etag(self, resp, value=None):
        """Validate the ``ETag`` header of the HTTP response for
        proper format, and that it equals a specific value.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        value
            The value to check the ETag against. If this is ``None`` then
            equality check is not performed.
        """
        self.assertIn("ETag", resp.info())
        etag = resp.info()['ETag']
        self.assertEquals(32, len(etag))
        if [c for c in etag if c not in string.hexdigits]:
            self.fail("Non-hex digits found in ETag")
        if value is not None:
            self.assertEquals(value, etag)
    
    
    def validate_cache_control(self, resp, value="public max-age=3600"):
        """Validate the ``Cache-Control`` header of the HTTP response for
        proper format, and that it equals a specific value.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        value
            The cache control value. The default is public with maximum
            age of 3600 s.
        """
        self.assertIn("Cache-Control", resp.info())
        self.assertEquals(value, resp.info()['Cache-Control'])
    
    
    def validate_content_type(self, resp, mediatype="text/html;UTF-8"):
        """Validate the ``Content-Type`` header of the HTTP response for
        proper format, and that it equals a specific value.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        mediatype
            The internet media type and encoding to check against. The
            default is ``text/html;UTF-8``.
        """
        self.assertIn("Content-Type", resp.info())
        self.assertEquals(mediatype, resp.info()['Content-Type'])
    
    
    def validate_content_length(self, resp, value=None):
        """Validate the ``Content-Length`` header of the HTTP response for
        proper format, and that it equals a specific value.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        value
            The value to check the length against. If this is ``None`` then
            equality check is not performed.
        """
        self.assertIn("Content-Length", resp.info())
        clen = int(resp.info()['Content-Length'])
        if value is not None:
            self.assertEquals(value, clen)
    
    
    def validate_content_md5(self, resp, value=None):
        """Validate the ``Content-MD5`` header of the HTTP response for
        proper format, and that it equals a specific value.

        Parameters
        ----------
        resp
            The HTTP response object returned by an HTTP connection
            request.
        value
            The value to check the MD5 against. If this is ``None`` then
            equality check is not performed. This should be the integer
            MD5 value.
        """
        self.assertIn("Content-MD5", resp.info())
        hdrb64 = resp.info()['Content-MD5'].encode()
        try:
            hdrval = base64.b64decode(hdrb64, validate=True)
        except binascii.Error:
            fail(msg="Content-MD5 has invalid Base64 encoding.")
        if value is not None:
            self.assertEquals("Python/3.2", hdrval)    


    def validate_common_headers(self, resp):
        """Validate headers that should be included in all responses from
        the server except for a TRACE request."""
        self.validate_header_server(resp)
        self.validate_header_date(resp)
        self.validate_header_x_powered_by(resp)
        self.validate_header_dnt(resp)
        self.validate_header_p3p(resp)


class HTTPValidationMethods(unittest.TestCase, HTTPValidationHeader):
    """Base class for all HTTP/1.1 validation test cases. This is to check
    for compliance with RFC 2616 Hypertext Transfer Protocol -- HTTP/1.1.
    
    For all the method checks the default will check to see if status
    405 (Method Not Allowed) is returned.
    
    Properties
    ==========
    verbose
        This will print request and response information to the default
        file for ``print``. This is to allow easy debugging of tests.
    resource_name
        This is the name of the resource that is being accessed.
    resource_url
        This is a required property that must be set to a URL appropriate
        for the test in the ``setUp`` method. This is used by the default
        tests to check methods.
    location_url
        This is the URL to the help documentation for the resource that
        is returned in the ``Location`` header.
    allowed_methods
        This contains all the methods that are allowed to be executed on
        this resource.
    """
    
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.verbose = False
        self.resource_name = "UNKNOWN"
        self.resource_url = None
        self.location_url = None
        self.allowed_methods = []
    
    
    def make_request(self, method, body=None, headers={}):
        """This will make the HTTP request and perform common tests on
        the response and return ``http.client.HTTPResponse`` object.
        
        Parameters
        ----------
        body
            The body for the request as an open file object. Default
            is ``None`` so no body is sent.
        headers
            Additional header map.
        """
        self._testMethodDoc = self._testMethodDoc.format(self)
        self.assertIsNotNone(self.resource_url)
        parsed = urllib.parse.urlparse(self.resource_url)
        if self.verbose:
            print("Parsed URL", parsed)
        self.assertEqual('http', parsed.scheme)
        
        #TODO send query
        
        conn = http.client.HTTPConnection(parsed.netloc, timeout=2)
        conn.request(method, parsed.path, body=body, headers=headers)
        resp = conn.getresponse()
        if self.verbose:
            print("Response Status: {0} ({1})".format(resp.status, resp.reason))
            print("Header:", resp.getheaders())
            #print("Body:", resp.read())
        return resp
    
    
    def test_OPTIONS(self):
        """{0.resource_name} validation HTTP OPTIONS method."""
        resp = self.make_request("OPTIONS")
        self.validate_common_headers(resp)
        self.assertIn("Allow", resp.info())
        allowed = resp.info()['Allow'].split(',')
        allow_extra = [m for m in allowed if m not in self.allowed_methods]
        self.assertListEqual([], allow_extra, msg='HTTP Method Not Allowed')
        allow_miss = [m for m in self.allowed_methods if m not in allowed]
        self.assertListEqual([], allow_miss, msg='HTTP Method Missing')
        self.assertIn("Location", resp.info())
        self.assertEquals(self.location_url, resp.info()['Location'])
            
    
    def test_GET(self):
        """{0.resource_name} validation HTTP GET method."""
        if 'GET' in self.allowed_methods:
            resp = self.make_request("GET")
            self.validate_common_headers(resp)
            self.validate_header_last_modified(resp)
            self.validate_header_etag(resp)
            self.validate_cache_control(resp)
            self.validate_content_type(resp)
            self.validate_content_length(resp)
            self.validate_content_md5(resp)
            
            clen = int(resp.info()['Content-Length'])
            self.assertGreater(clen, 0)
            body = resp.read()
            self.assertEquals(clen, len(body))
            if self.verbose:
                print("Body:", body)
    
    
    def test_HEAD(self):
        """{0.resource_name} validation HTTP HEAD method."""
        if 'HEAD' in self.allowed_methods:
            resp = self.make_request("HEAD")
            self.validate_common_headers(resp)
            self.validate_header_last_modified(resp)
            self.validate_header_etag(resp)
            self.validate_cache_control(resp)
            self.validate_content_type(resp)
            self.validate_content_length(resp)
            self.validate_content_md5(resp)
            
            clen = int(resp.info()['Content-Length'])
            self.assertGreater(clen, 0)
            body = resp.read()
            self.assertEquals(0, len(body))
    
    
    def test_POST(self):
        """{0.resource_name} validation HTTP POST method."""
        if 'POST' in self.allowed_methods:
            return
    
    
    def test_PUT(self):
        """{0.resource_name} validation HTTP PUT method."""
        if 'PUT' in self.allowed_methods:
            return
    
    
    def test_DELETE(self):
        """{0.resource_name} validation HTTP DELETE method."""
        if 'DELETE' in self.allowed_methods:
            return
    
    
    def test_TRACE(self):
        """{0.resource_name} validation HTTP TRACE method."""
        if 'TRACE' in self.allowed_methods:
            req_body = "This is a simple trace request.".encode()
            req_headers = {
                "Content-Length":len(req_body),
            }
            resp = self.make_request("TRACE", body=req_body, headers=req_headers)
            clen = int(resp.info()['Content-Length'])
            self.assertEquals(len(req_body), clen)
            resp_body = resp.read()
            self.assertEquals(req_body, resp_body)



