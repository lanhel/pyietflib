#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Parser for vCard v4 as defined in RFC6350"""
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

import abnf


#======================================
# 3.3 ABNF Format Definitions

class Parser(abnf.Parser):
    def __init__(self, *argv, **kwarg):
        abnf.Parser.__init__(self, *argv, **kwarg)
        self.start = 'vcard-entity'

@abnf.rule(Parser, 'vcard-entity = 1*vcard')
def vcard_entity(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''vcard =
    "BEGIN:VCARD" CRLF
    "VERSION:4.0" CRLF
    1*contentline
    "END:VCARD" CRLF
    ''')
def vcard(parser, rule, values):
    print(rule.__name__, parser)


@abnf.rule(Parser, 'contentline = [group "."] name *(";" param) ":" value CRLF')
def contentline(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'group = 1*(ALPHA / DIGIT / "-")')
def group(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''name
    = "SOURCE" / "KIND" / "FN" / "N" / "NICKNAME"
    / "PHOTO" / "BDAY" / "ANNIVERSARY" / "GENDER" / "ADR" / "TEL"
    / "EMAIL" / "IMPP" / "LANG" / "TZ" / "GEO" / "TITLE" / "ROLE"
    / "LOGO" / "ORG" / "MEMBER" / "RELATED" / "CATEGORIES"
    / "NOTE" / "PRODID" / "REV" / "SOUND" / "UID" / "CLIENTPIDMAP"
    / "URL" / "KEY" / "FBURL" / "CALADRURI" / "CALURI" / "XML"
    / iana-token / x-name
    ''')
def name(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'iana-token = 1*(ALPHA / DIGIT / "-")')
def iana_token(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'x-name = "x-" 1*(ALPHA / DIGIT / "-")')
def x_name(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''param
    = language-param / value-param / pref-param / pid-param
    / type-param / geo-parameter / tz-parameter / sort-as-param
    / calscale-param / any-param
    ; Allowed parameters depend on property name.
    ''')
def param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'param-value = *SAFE-CHAR / DQUOTE *QSAFE-CHAR DQUOTE')
def param_value(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'any-param = (iana-token / x-name) "=" param-value *("," param-value)')
def any_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''NON-ASCII
    = %xC2-DF 1(%x80-8F) ;UTF8 2 byte sequence
    / %xE0-EF 2(%x80-8F) ;UTF8 3 byte sequence
    / %xF0-F4 3(%x80-8F) ;UTF8 4 byte sequence
    ''')
def NON_ASCII(parser, rule, values):
    'UTF8-{2,3,4} are defined in [RFC3629]'
    print(rule.__name__, parser)

@abnf.rule(Parser, 'QSAFE-CHAR = WSP / "!" / %x23-7E / NON-ASCII')
def QSAFE_CHAR(parser, rule, values):
    'Any character except CTLs, DQUOTE'
    print(rule.__name__, parser)

@abnf.rule(Parser, 'SAFE-CHAR = WSP / "!" / %x23-39 / %x3C-7E / NON-ASCII')
def SAFE_CHAR(parser, rule, values):
    'Any character except CTLs, DQUOTE, ";", ":"'
    print(rule.__name__, parser)

@abnf.rule(Parser, 'VALUE-CHAR = WSP / VCHAR / NON-ASCII')
def VALUE_CHAR(parser, rule, values):
     'Any textual character'
     print(rule.__name__, parser)
 

#======================================
# 4 Property Value Data Types

@abnf.rule(Parser, '''value
    = text
    / text-list
    / date-list
    / time-list
    / date-time-list
    / date-and-or-time-list
    / timestamp-list
    / boolean
    / integer-list
    / float-list
    / URI               ; from Section 3 of [RFC3986]
    / utc-offset
    / Language-Tag
    / iana-valuespec
    ; Actual value type depends on property name and VALUE parameter.
    ''')
def value(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'text = *TEXT-CHAR')
def text(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''TEXT-CHAR
    = "\\\\" / "\," / "\\n" / WSP / NON-ASCII
    / %x21-2B / %x2D-5B / %x5D-7E
    ; Backslashes, commas, and newlines must be encoded.
    ''')
def TEXT_CHAR(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''component
    = "\\\\" / "\," / "\;" / "\\n" / WSP
    / NON-ASCII
    / %x21-2B / %x2D-3A / %x3C-5B / %x5D-7E
    ''')
def component(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'list-component = component *("," component)')
def list_component(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'text-list = text *("," text)')
def text_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'date-list = date *("," date)')
def date_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'time-list = time *("," time)')
def time_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'date-time-list = date-time *("," date-time)')
def date_time_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'date-and-or-time-list = date-and-or-time *("," date-and-or-time)')
def date_and_or_time_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'timestamp-list = timestamp *("," timestamp)')
def timestamp_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'integer-list = integer *("," integer)')
def integer_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'float-list = float *("," float)')
def float_list(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'boolean = "TRUE" / "FALSE"')
def boolean(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'integer = [sign] 1*DIGIT')
def integer(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'float = [sign] 1*DIGIT ["." 1*DIGIT]')
def float(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'sign = "+" / "-"')
def sign(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'year = 4DIGIT  ; 0000-9999')
def year(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'month = 2DIGIT  ; 01-12')
def month(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'day = 2DIGIT  ; 01-28/29/30/31 depending on month and leap year')
def day(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'hour = 2DIGIT  ; 00-23')
def hour(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'minute = 2DIGIT  ; 00-59')
def minute(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'second = 2DIGIT  ; 00-58/59/60 depending on leap second')
def second(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'zone = utc-designator / utc-offset')
def zone(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'utc-designator = %x5A  ; uppercase "Z"')
def utc_designator(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''date
    = year    [month  day]
    / year "-" month
    / "--"     month [day]
    / "--"     "-"    day
    ''')
def date(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''date-noreduc
    = year month  day
    / "--" month  day
    / "--" "-"    day
    ''')
def date_noreduc(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'date-complete = year month  day')
def date_complete(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''time
    = hour [minute [second]] [zone]
    /  "-"  minute [second]  [zone]
    /  "-"   "-"    second   [zone]
    ''')
def time(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'time-notrunc = hour [minute [second]] [zone]')
def time_notrunc(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'time-complete = hour minute second [zone]')
def time_complete(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'time-designator = %x54 ; uppercase "T"')
def time_designator(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'date-time = date-noreduc time-designator time-notrunc')
def date_time(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'timestamp = date-complete time-designator time-complete')
def timestamp(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'date-and-or-time = date-time / date / time-designator time')
def date_and_or_time(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'utc-offset = sign hour [minute]')
def utc_offset(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'Language-Tag = <Language-Tag, defined in [RFC5646], Section 2.1>')
def Language_Tag(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''
    iana-valuespec = <value-spec, see Section 12>
    ; a publicly defined valuetype format, registered
    ; with IANA, as defined in Section 12 of this
    ; document.
    ''')
def iana_valuespec(parser, rule, values):
    print(rule.__name__, parser)


#======================================
# 5 Property Parameters

@abnf.rule(Parser, 'language-param = "LANGUAGE=" Language-Tag')
def language_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'value-param = "VALUE=" value-type')
def value_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''value-type
    = "text"
    / "uri"
    / "date"
    / "time"
    / "date-time"
    / "date-and-or-time"
    / "timestamp"
    / "boolean"
    / "integer"
    / "float"
    / "utc-offset"
    / "language-tag"
    / iana-token  ; registered as described in section 12
    / x-name
    ''')
def value_type(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''pref-param = "PREF=" (1*2DIGIT / "100")
    ; An integer between 1 and 100.
    ''')
def pref_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'altid-param = "ALTID=" param-value')
def altid_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'pid-param = "PID=" pid-value *("," pid-value)')
def pid_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'pid-value = 1*DIGIT ["." 1*DIGIT]')
def pid_value(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'type-param = "TYPE=" type-value *("," type-value)')
def type_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''type-value
    = "work" / "home" / type-param-tel
    / type-param-related / iana-token / x-name
    ; This is further defined in individual property sections.
    ''')
def type_value(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'mediatype-param = "MEDIATYPE=" mediatype')
def mediatype_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, '''mediatype = type-name "/" subtype-name *( ";" attribute "=" value )
    ; "attribute" and "value" are from [RFC2045]
    ; "type-name" and "subtype-name" are from [RFC4288]
    ''')
def mediatype(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'calscale-param = "CALSCALE=" calscale-value')
def calscale_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'calscale-value = "gregorian" / iana-token / x-name')
def calscale_value(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'sort-as-param = "SORT-AS=" sort-as-value')
def sort_as_param(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'sort-as-value = param-value *("," param-value)')
def sort_as_value(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'geo-parameter = "GEO=" DQUOTE URI DQUOTE')
def geo_parameter(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'tz-parameter = "TZ=" (param-value / DQUOTE URI DQUOTE)')
def tz_parameter(parser, rule, values):
    print(rule.__name__, parser)

@abnf.rule(Parser, 'empty = ')
def empty(self):
    print('Parser.empty')


if __name__ == '__main__':
    import io
    
    data = b'''\
BEGIN:VCARD
VERSION:4.0
UID:urn:uuid:4fbe8971-0bc3-424c-9c26-36c3e1eff6b1
FN;PID=1.1:J. Doe
N:Doe;J.;;;
EMAIL;PID=1.1:jdoe@example.com
EMAIL;PID=2.1:boss@example.com
TEL;PID=1.1;VALUE=uri:tel:+1-555-555-5555
TEL;PID=2.1;VALUE=uri:tel:+1-666-666-6666
CLIENTPIDMAP:1;urn:uuid:53e374d9-337e-4727-8803-a1e9c14e0556
END:VCARD

BEGIN:VCARD
VERSION:4.0
UID:urn:uuid:4fbe8971-0bc3-424c-9c26-36c3e1eff6b1
FN;PID=1.1:J. Doe
N:Doe;J.;;;
EMAIL;PID=1.1:jdoe@example.com
EMAIL;PID=2.2:ceo@example.com
TEL;PID=1.1;VALUE=uri:tel:+1-555-555-5555
TEL;PID=2.2;VALUE=uri:tel:+1-666-666-6666
CLIENTPIDMAP:1;urn:uuid:53e374d9-337e-4727-8803-a1e9c14e0556
CLIENTPIDMAP:2;urn:uuid:1f762d2b-03c4-4a83-9a03-75ff658a6eee
END:VCARD
        '''
    
    fd = io.BytesIO(data)
    p = Parser(fd, text=False)
    for x in p:
        print(x)
    print(p["vcard-entity"])
    print(p["vcard-entity"].ruledef)
    
    

