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
import http.client
import yaml

__all__ = ["HTTPClient"]

class HTTPClient():
    """When given a YAML document this will connect with the ERChime
    server and submit a pre-canned request response with validation."""
    def __init__(self, host="localhost", port="8008"):
        self.conn = http.client.HTTPConnection(host, int(port))
    
    def close(self):
        self.conn.close()
        self.conn = None
    
    def request(self, doc_req):
        m = doc_req['method']
        p = doc_req['path']
        h = doc_req['headers'][0]
        b = doc_req['body'].encode('utf-8')
        self.conn.request(m, p, body=b, headers=h)
        resp = self.conn.getresponse()
        return (resp.status, resp.getheaders(), resp.read())
    
    def validate(self, path):
        with open(path) as fp:
            for doc in yaml.load_all(fp):
                status, headers, body = self.request(doc['request'])
                print(status)
                print(headers)
                print(body)
        
