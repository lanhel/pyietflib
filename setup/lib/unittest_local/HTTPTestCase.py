#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""ERChime HTTP client system."""
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
from datetime import *
import unittest
import http.client
import socket
import hashlib
import difflib
import base64
import yaml

__all__ = ["HTTPTestCase", "HTTPTestSuite"]

class HTTPTestSuite(unittest.TestSuite):
    """Load a sequence of tests from a path to a YAML test file and create
    HTTPTestCase for each document."""
    def __init__(self, path):
        path = os.path.normpath(path)
        relp = os.path.relpath(path, start="build/accept/lib")
        with open(path) as fp:
            tests = [HTTPTestCase(relp, i, d) for i, d in enumerate(yaml.load_all(fp))]
        super().__init__(tests)

class HTTPTestCase(unittest.TestCase):
    """When given a YAML document this will connect with the ERChime
    server and submit a pre-canned request response with validation.
    
    Document Schema
    ---------------
    request:
        method:     <HTTP method>
        path:       <URL path fragment>
        headers:    <Dictionary of HTTP request header keys and values>
        body:       <HTTP content body>
    response:
        status:     <HTTP numeric status code>
        headers:    <Dictionary of HTTP response header keys and values>
        body:       <HTTP response content body
    
    Request Headers
    ---------------
    Content-Type
        Used to encode the body.
    
    Content-Length
        Automatically generated from the encoding of the body.
    
    Date
        Automatically generated as the current time.
    
    
    Response Headers
    ----------------
    Server
        Checked against a predfined string: e.g. `erchime/1.0 Python/3.2.2`.
    
    Date
        Checked against the current time with a small delta.
        
    DNT
        Checked against string: `0`
            
    Cache-Control
        Checked against string: `public max-age=3600`. Unless overriden
        in the response.
    
    P3P
        Checked against string: `policyref="http://localhost:8008/w3c/p3p.xml"`.

    Content-Length
        Will be checked against the actual content buffer size.

    Content-MD5
        Will be calculated against the actual content buffer and compared.

    X-XSS-Protection
        Checked against string: `1; mode=block`
    
    X-Content-Type-Options
        Checked against string: `nosniff`
    
    X-Powered-By
        Checked against string: `Python/3.2.2`

    X-Frame-Options
        Checked against string: `deny`

    
    Dynamic Header Values
    ---------------------
    ETag
        If the 'ETag' header value is `python:<str>` in the YAML document
        then the `<str>` will be given to `exec` for execution. Within
        that execution block the variable `ETag` must be set and will
        be used as the test value. This test case is stored in the
        variable `test_case` for use by the executable string.
    """
    def __init__(self, path, index, doc):
        super().__init__()
        self.path = path
        self.index = index
        self.doc_yaml = doc
        self.doc_req = doc['request']
        self.doc_resp = doc['response']
        
        if 'headers' not in self.doc_req or self.doc_req['headers'] is None:
            self.doc_req['headers'] = {}
        if 'body' not in self.doc_req:
            self.doc_req['body'] = None
        
        if 'headers' not in self.doc_resp or self.doc_resp['headers'] is None:
            self.doc_resp['headers'] = {}
        if 'body' not in self.doc_resp:
            self.doc_resp['body'] = None
    
    def shortDescription(self):
        return "YAML: {0.path} [{0.index}] {1[method]} {1[path]}".format(self, self.doc_req)

    def setUp(self):
        self.host = "localhost"
        self.port = 8008
        self.conn = http.client.HTTPConnection(self.host, port=int(self.port), timeout=1.0)
    
    def tearDown(self):
        active_testcase = None
    
    def runTest(self):
        req_date = datetime.strptime(self.date_time_string(), "%a, %d %b %Y %H:%M:%S %Z")
        status, headers, body = self.request()

        #Check the status
        self.assertEqual(status, self.doc_resp['status'], msg='Incorrect status.')

        if sys.version_info[2] == 0:
            py_version = "Python/{0[0]}.{0[1]}".format(sys.version_info)
        else:
            py_version = "Python/{0[0]}.{0[1]}.{0[2]}".format(sys.version_info)        
        
        #Check the headers
        test_headers = self.doc_resp['headers']
        test_headers['Server'] = "erchime/1.0 {0}".format(py_version)
        test_headers['DNT'] = "0"
        if 'Cache-Control' not in test_headers:
            test_headers['Cache-Control'] = "public max-age=3600"
        test_headers['P3P'] = 'policyref="http://localhost:8008/w3c/p3p.xml"'
        test_headers['X-XSS-Protection'] = "1; mode=block"
        test_headers['X-Content-Type-Options'] = "nosniff"
        test_headers['X-Powered-By'] = py_version
        test_headers['X-Frame-Options'] = "deny"
        for k, v in test_headers.items():
            self.assertTrue(k in headers, msg="Header {0} missing.".format(k))
            if k == 'ETag' and v.startswith("python:"):
                exp = v.split(':')[1]
                locvars = {"test_case":self}
                exec(exp, globals(), locvars)
                etag = locvars['ETag']
                self.assertEqual(headers[k], etag, msg="Header {0} invalid.".format(k))
            else:
                self.assertEqual(headers[k], v, msg="Header {0} invalid.".format(k))
            
        self.assertTrue('Date' in headers, msg="Header Date missing.")
        resp_date = datetime.strptime(headers['Date'], "%a, %d %b %Y %H:%M:%S %Z")
        now_date = datetime.utcnow()
        self.assertLess(resp_date, now_date, "Response date after now.")
        self.assertGreaterEqual(resp_date, req_date, "Response date before request date.")

        #Check the body
        if len(body) > 0:
            self.assertEquals(int(headers['Content-Length']), len(body), msg="Content-Length not equal to body length")

            self.assertTrue('Content-MD5' in headers, msg="Header Content-MD5 missing.")
            md5 = hashlib.md5()
            md5.update(body)
            md5 = str(base64.b64encode(md5.digest()), encoding="UTF-8")
            self.assertEquals(headers["Content-MD5"], md5, msg="Header Content-MD5 invalid.")
        
            encoding = self.split_content_type(headers)[1]
            body = body.decode(encoding)
            body = body.replace("\r\n", "\n")
            body = body.replace("\r", "\n")
            if self.doc_resp["body"].strip() != body.strip():
                a = self.doc_resp["body"].strip().split("\n")
                b = body.strip().split("\n")
                msg = difflib.context_diff(a, b, fromfile='Expected', tofile="Actual", lineterm="")
                msg = "Unexpected response body.\n" + "\n".join(msg)
                self.fail(msg)

    def filepath_etag(self, filepath):
        date = datetime.fromtimestamp(os.path.getmtime(filepath))
        tag = "Path: {0}\nmtime: {1}".format(filepath, date.isoformat())
        etag = hashlib.md5()
        etag.update(tag.encode("UTF-8"))
        return etag.hexdigest()
    
    def date_time_string(self, dt=None):
        if dt is None:
            dt = datetime.now()
        return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    def split_content_type(self, headers):
        try:
            ct = headers['Content-Type']
            if ';' in ct:
                t, cs = ct.split(';')
                if not cs:
                    cs = 'charset=utf8'
                scratch, cs = cs.split('=')
                return (t.strip(), cs.strip())
            else:
                return (ct.strip(), "iso-8859-4")
        except:
            self.fail("Invalid Content-Type: {0}".format(ct))
    
    def request(self):
        """Make a single request against the connection."""
        method = self.doc_req['method']
        path = self.doc_req['path']
        
        headers = self.doc_req['headers']
        headers['Date'] = self.date_time_string()
        
        body = self.doc_req['body']
        if body is not None:
            encoding = self.split_content_type(headers)[1]
            body = body.encode(encoding)
            headers['Content-Length'] = len(body)
        
        try:
            self.conn.request(method, path, body=body, headers=headers)
            resp = self.conn.getresponse()
        except socket.timeout as err:
            return (None, None, None)
        else:
            resp_status = resp.status
            resp_headers = dict(resp.getheaders())
            if int(resp_headers.get("Content-Length", "0")) > 0:
                resp_body = resp.read()
            else:
                resp_body = ""
            return (resp_status, resp_headers, resp_body)
                



