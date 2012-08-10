#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Parser for RFC 5646 Tags for Identifying Languages"""
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
    raise Exception("pyvcard requires Python 3.2 or higher.")
import re
import ply.lex as lex

ALPHA = br'[A-Za-z]'
DIGIT = br'\d'
HEXDIGIT = br'[0-9A-F]'
DQUOTE = br'"'
SP = br' '
HTAB = br'\t'
WSP = br'[ \t]'
LWSP = br'(\r\n)?( \t)*'
CR = br'\r'
LF = br'\n'
CRLF = br'\r\n'

Language-Tag  = langtag             ; normal language tags
               / privateuse          ; private use tag
               / grandfathered       ; grandfathered tags

langtag       = language
             ["-" script]
             ["-" region]
             *("-" variant)
             *("-" extension)
             ["-" privateuse]

language      = 2*3ALPHA            ; shortest ISO 639 code
             ["-" extlang]       ; sometimes followed by
                                 ; extended language subtags
           / 4ALPHA              ; or reserved for future use
           / 5*8ALPHA            ; or registered language subtag

extlang       = 3ALPHA              ; selected ISO 639 codes
             *2("-" 3ALPHA)      ; permanently reserved

script        = 4ALPHA              ; ISO 15924 code

region        = 2ALPHA              ; ISO 3166-1 code
           / 3DIGIT              ; UN M.49 code

variant       = 5*8alphanum         ; registered variants
           / (DIGIT 3alphanum)

extension     = singleton 1*("-" (2*8alphanum))

                                 ; Single alphanumerics
                                 ; "x" reserved for private use
singleton     = DIGIT               ; 0 - 9
           / %x41-57             ; A - W
           / %x59-5A             ; Y - Z
           / %x61-77             ; a - w
           / %x79-7A             ; y - z

privateuse    = "x" 1*("-" (1*8alphanum))

grandfathered = irregular           ; non-redundant tags registered
           / regular             ; during the RFC 3066 era

irregular     = "en-GB-oed"         ; irregular tags do not match
           / "i-ami"             ; the 'langtag' production and
           / "i-bnn"             ; would not otherwise be
           / "i-default"         ; considered 'well-formed'
           / "i-enochian"        ; These tags are all valid,
           / "i-hak"             ; but most are deprecated
           / "i-klingon"         ; in favor of more modern
           / "i-lux"             ; subtags or subtag
           / "i-mingo"           ; combination
           / "i-navajo"
           / "i-pwn"
           / "i-tao"
           / "i-tay"
           / "i-tsu"
           / "sgn-BE-FR"
           / "sgn-BE-NL"
           / "sgn-CH-DE"

regular       = "art-lojban"        ; these tags match the 'langtag'
           / "cel-gaulish"       ; production, but their subtags
           / "no-bok"            ; are not extended language
           / "no-nyn"            ; or variant subtags: their meaning
           / "zh-guoyu"          ; is defined by their registration
           / "zh-hakka"          ; and all of these are deprecated
           / "zh-min"            ; in favor of a more modern
           / "zh-min-nan"        ; subtag or sequence of subtags
           / "zh-xiang"

alphanum      = (ALPHA / DIGIT)     ; letters and numbers
