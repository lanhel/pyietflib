#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""ISO code validation."""
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
    raise Exception("Language-Tag requires Python 3.2 or higher.")

__all__ = [
    'valid_ISO639_1', 'valid_ISO639_2',
    'valid_ISO3166_1_alpha2', 'valid_ISO3166_1_alpha3', 'valid_ISO3166_1_numeric'
]

__todo__ = """
    1. Convert ISO 639 into a real registry of languages.
    2. Convert ISO 3166 into a real registry of regions.
    3. Convert ISO 15924 into a real registry of scripts.
    4. Add validation for ISO 15924
        a. http://www.unicode.org/iso15924/codelists.html
"""

###
### Language codes
###

iso639 = [
    ('ab', 'abk'), ('aa', 'aar'), ('af', 'afr'), ('ak', 'aka'), ('sq', 'sqi'),
    ('am', 'amh'), ('ar', 'ara'), ('an', 'arg'), ('hy', 'hye'), ('as', 'asm'),
    ('av', 'ava'), ('ae', 'ave'), ('ay', 'aym'), ('az', 'aze'), ('bm', 'bam'),
    ('ba', 'bak'), ('eu', 'eus'), ('be', 'bel'), ('bn', 'ben'), ('bh', 'bih'),
    ('bi', 'bis'), ('bs', 'bos'), ('br', 'bre'), ('bg', 'bul'), ('my', 'mya'),
    ('ca', 'cat'), ('ch', 'cha'), ('ce', 'che'), ('ny', 'nya'), ('zh', 'zho'),
    ('cv', 'chv'), ('kw', 'cor'), ('co', 'cos'), ('cr', 'cre'), ('hr', 'hrv'),
    ('cs', 'ces'), ('da', 'dan'), ('dv', 'div'), ('nl', 'nld'), ('dz', 'dzo'),
    ('en', 'eng'), ('eo', 'epo'), ('et', 'est'), ('ee', 'ewe'), ('fo', 'fao'),
    ('fj', 'fij'), ('fi', 'fin'), ('fr', 'fra'), ('ff', 'ful'), ('gl', 'glg'),
    ('ka', 'kat'), ('de', 'deu'), ('el', 'ell'), ('gn', 'grn'), ('gu', 'guj'),
    ('ht', 'hat'), ('ha', 'hau'), ('he', 'heb'), ('hz', 'her'), ('hi', 'hin'),
    ('ho', 'hmo'), ('hu', 'hun'), ('ia', 'ina'), ('id', 'ind'), ('ie', 'ile'),
    ('ga', 'gle'), ('ig', 'ibo'), ('ik', 'ipk'), ('io', 'ido'), ('is', 'isl'),
    ('it', 'ita'), ('iu', 'iku'), ('ja', 'jpn'), ('jv', 'jav'), ('kl', 'kal'),
    ('kn', 'kan'), ('kr', 'kau'), ('ks', 'kas'), ('kk', 'kaz'), ('km', 'khm'),
    ('ki', 'kik'), ('rw', 'kin'), ('ky', 'kir'), ('kv', 'kom'), ('kg', 'kon'),
    ('ko', 'kor'), ('ku', 'kur'), ('kj', 'kua'), ('la', 'lat'), ('lb', 'ltz'),
    ('lg', 'lug'), ('li', 'lim'), ('ln', 'lin'), ('lo', 'lao'), ('lt', 'lit'),
    ('lu', 'lub'), ('lv', 'lav'), ('gv', 'glv'), ('mk', 'mkd'), ('mg', 'mlg'),
    ('ms', 'msa'), ('ml', 'mal'), ('mt', 'mlt'), ('mi', 'mri'), ('mr', 'mar'),
    ('mh', 'mah'), ('mn', 'mon'), ('na', 'nau'), ('nv', 'nav'), ('nb', 'nob'),
    ('nd', 'nde'), ('ne', 'nep'), ('ng', 'ndo'), ('nn', 'nno'), ('no', 'nor'),
    ('ii', 'iii'), ('nr', 'nbl'), ('oc', 'oci'), ('oj', 'oji'), ('cu', 'chu'),
    ('om', 'orm'), ('or', 'ori'), ('os', 'oss'), ('pa', 'pan'), ('pi', 'pli'),
    ('fa', 'fas'), ('pl', 'pol'), ('ps', 'pus'), ('pt', 'por'), ('qu', 'que'),
    ('rm', 'roh'), ('rn', 'run'), ('ro', 'ron'), ('ru', 'rus'), ('sa', 'san'),
    ('sc', 'srd'), ('sd', 'snd'), ('se', 'sme'), ('sm', 'smo'), ('sg', 'sag'),
    ('sr', 'srp'), ('gd', 'gla'), ('sn', 'sna'), ('si', 'sin'), ('sk', 'slk'),
    ('sl', 'slv'), ('af', 'Soo'), ('st', 'sot'), ('es', 'spa'), ('su', 'sun'),
    ('sw', 'swa'), ('ss', 'ssw'), ('sv', 'swe'), ('ta', 'tam'), ('te', 'tel'),
    ('tg', 'tgk'), ('th', 'tha'), ('ti', 'tir'), ('bo', 'bod'), ('tk', 'tuk'),
    ('tl', 'tgl'), ('tn', 'tsn'), ('to', 'ton'), ('tr', 'tur'), ('ts', 'tso'),
    ('tt', 'tat'), ('tw', 'twi'), ('ty', 'tah'), ('ug', 'uig'), ('uk', 'ukr'),
    ('ur', 'urd'), ('uz', 'uzb'), ('ve', 'ven'), ('vi', 'vie'), ('vk', 'vik'),
    ('vo', 'vol'), ('wa', 'wln'), ('cy', 'cym'), ('wo', 'wol'), ('fy', 'fry'),
    ('xh', 'xho'), ('yi', 'yid'), ('yo', 'yor'), ('za', 'zha'), ('zu', 'zul')
]
iso639_1 = [two for two, three in iso639]
iso639_1.sort()
iso639_2 = [three for two, three in iso639]
iso639_2.sort()
iso639_2_extended = ['gan', 'cmn', 'yue']

def valid_ISO639_1(code):
    """Is `code` a valid ISO 639-1 two character language code."""
    code = str(code)
    if len(code) != 2:
        return False
    return code in iso639_1

def valid_ISO639_2(code):
    """Is `code` a valid ISO 639-2 three character language code."""
    code = str(code)
    if len(code) != 3:
        return False
    if code in ['mul', 'und', 'mis', 'zxx']:
        return True
    if code[0] == 'q' and code[2] not in ['u', 'v', 'w', 'x', 'y', 'z']:
        return True
    if code in iso639_2_extended:
        return True
    return code in iso639_2


###
### Region (country) codes
###

iso3166_assigned = [
    ('AD', 'AND', '020'), ('AE', 'ARE', '784'), ('AF', 'AFG', '004'),
    ('AG', 'ATG', '028'), ('AI', 'AIA', '660'), ('AL', 'ALB', '008'),
    ('AM', 'ARM', '051'), ('AN', 'ANT', '530'), ('AO', 'AGO', '024'),
    ('AQ', 'ATA', '010'), ('AR', 'ARG', '032'), ('AS', 'ASM', '016'),
    ('AT', 'AUT', '040'), ('AU', 'AUS', '036'), ('AW', 'ABW', '533'),
    ('AX', 'ALA', '248'), ('AZ', 'AZE', '031'), ('BA', 'BIH', '070'),
    ('BB', 'BRB', '052'), ('BD', 'BGD', '050'), ('BE', 'BEL', '056'),
    ('BF', 'BFA', '854'), ('BG', 'BGR', '100'), ('BH', 'BHR', '048'),
    ('BI', 'BDI', '108'), ('BJ', 'BEN', '204'), ('BM', 'BMU', '060'),
    ('BN', 'BRN', '096'), ('BO', 'BOL', '068'), ('BR', 'BRA', '076'),
    ('BS', 'BHS', '044'), ('BT', 'BTN', '064'), ('BV', 'BVT', '074'),
    ('BW', 'BWA', '072'), ('BY', 'BLR', '112'), ('BZ', 'BLZ', '084'),
    ('CA', 'CAN', '124'), ('CC', 'CCK', '166'), ('CD', 'COD', '180'),
    ('CF', 'CAF', '140'), ('CG', 'COG', '178'), ('CH', 'CHE', '756'),
    ('CI', 'CIV', '384'), ('CK', 'COK', '184'), ('CL', 'CHL', '152'),
    ('CM', 'CMR', '120'), ('CN', 'CHN', '156'), ('CO', 'COL', '170'),
    ('CR', 'CRI', '188'), ('CS', 'SCG', '891'), ('CU', 'CUB', '192'),
    ('CV', 'CPV', '132'), ('CX', 'CXR', '162'), ('CY', 'CYP', '196'),
    ('CZ', 'CZE', '203'), ('DE', 'DEU', '276'), ('DJ', 'DJI', '262'),
    ('DK', 'DNK', '208'), ('DM', 'DMA', '212'), ('DO', 'DOM', '214'),
    ('DZ', 'DZA', '012'), ('EC', 'ECU', '218'), ('EE', 'EST', '233'),
    ('EG', 'EGY', '818'), ('EH', 'ESH', '732'), ('ER', 'ERI', '232'),
    ('ES', 'ESP', '724'), ('ET', 'ETH', '231'), ('FI', 'FIN', '246'),
    ('FJ', 'FJI', '242'), ('FK', 'FLK', '238'), ('FM', 'FSM', '583'),
    ('FO', 'FRO', '234'), ('FR', 'FRA', '250'), ('GA', 'GAB', '266'),
    ('GB', 'GBR', '826'), ('GD', 'GRD', '308'), ('GE', 'GEO', '268'),
    ('GF', 'GUF', '254'), ('GH', 'GHA', '288'), ('GI', 'GIB', '292'),
    ('GL', 'GRL', '304'), ('GM', 'GMB', '270'), ('GN', 'GIN', '324'),
    ('GP', 'GLP', '312'), ('GQ', 'GNQ', '226'), ('GR', 'GRC', '300'),
    ('GS', 'SGS', '239'), ('GT', 'GTM', '320'), ('GU', 'GUM', '316'),
    ('GW', 'GNB', '624'), ('GY', 'GUY', '328'), ('HK', 'HKG', '344'),
    ('HM', 'HMD', '334'), ('HN', 'HND', '340'), ('HR', 'HRV', '191'),
    ('HT', 'HTI', '332'), ('HU', 'HUN', '348'), ('ID', 'IDN', '360'),
    ('IE', 'IRL', '372'), ('IL', 'ISR', '376'), ('IN', 'IND', '356'),
    ('IO', 'IOT', '086'), ('IQ', 'IRQ', '368'), ('IR', 'IRN', '364'),
    ('IS', 'ISL', '352'), ('IT', 'ITA', '380'), ('JM', 'JAM', '388'),
    ('JO', 'JOR', '400'), ('JP', 'JPN', '392'), ('KE', 'KEN', '404'),
    ('KG', 'KGZ', '417'), ('KH', 'KHM', '116'), ('KI', 'KIR', '296'),
    ('KM', 'COM', '174'), ('KN', 'KNA', '659'), ('KP', 'PRK', '408'),
    ('KR', 'KOR', '410'), ('KW', 'KWT', '414'), ('KY', 'CYM', '136'),
    ('KZ', 'KAZ', '398'), ('LA', 'LAO', '418'), ('LB', 'LBN', '422'),
    ('LC', 'LCA', '662'), ('LI', 'LIE', '438'), ('LK', 'LKA', '144'),
    ('LR', 'LBR', '430'), ('LS', 'LSO', '426'), ('LT', 'LTU', '440'),
    ('LU', 'LUX', '442'), ('LV', 'LVA', '428'), ('LY', 'LBY', '434'),
    ('MA', 'MAR', '504'), ('MC', 'MCO', '492'), ('MD', 'MDA', '498'),
    ('MG', 'MDG', '450'), ('MH', 'MHL', '584'), ('MK', 'MKD', '807'),
    ('ML', 'MLI', '466'), ('MM', 'MMR', '104'), ('MN', 'MNG', '496'),
    ('MO', 'MAC', '446'), ('MP', 'MNP', '580'), ('MQ', 'MTQ', '474'),
    ('MR', 'MRT', '478'), ('MS', 'MSR', '500'), ('MT', 'MLT', '470'),
    ('MU', 'MUS', '480'), ('MV', 'MDV', '462'), ('MW', 'MWI', '454'),
    ('MX', 'MEX', '484'), ('MY', 'MYS', '458'), ('MZ', 'MOZ', '508'),
    ('NA', 'NAM', '516'), ('NC', 'NCL', '540'), ('NE', 'NER', '562'),
    ('NF', 'NFK', '574'), ('NG', 'NGA', '566'), ('NI', 'NIC', '558'),
    ('NL', 'NLD', '528'), ('NO', 'NOR', '578'), ('NP', 'NPL', '524'),
    ('NR', 'NRU', '520'), ('NU', 'NIU', '570'), ('NZ', 'NZL', '554'),
    ('OM', 'OMN', '512'), ('PA', 'PAN', '591'), ('PE', 'PER', '604'),
    ('PF', 'PYF', '258'), ('PG', 'PNG', '598'), ('PH', 'PHL', '608'),
    ('PK', 'PAK', '586'), ('PL', 'POL', '616'), ('PM', 'SPM', '666'),
    ('PN', 'PCN', '612'), ('PR', 'PRI', '630'), ('PS', 'PSE', '275'),
    ('PT', 'PRT', '620'), ('PW', 'PLW', '585'), ('PY', 'PRY', '600'),
    ('QA', 'QAT', '634'), ('RE', 'REU', '638'), ('RO', 'ROU', '642'),
    ('RU', 'RUS', '643'), ('RW', 'RWA', '646'), ('SA', 'SAU', '682'),
    ('SB', 'SLB', '090'), ('SC', 'SYC', '690'), ('SD', 'SDN', '736'),
    ('SE', 'SWE', '752'), ('SG', 'SGP', '702'), ('SH', 'SHN', '654'),
    ('SI', 'SVN', '705'), ('SJ', 'SJM', '744'), ('SK', 'SVK', '703'),
    ('SL', 'SLE', '694'), ('SM', 'SMR', '674'), ('SN', 'SEN', '686'),
    ('SO', 'SOM', '706'), ('SR', 'SUR', '740'), ('ST', 'STP', '678'),
    ('SV', 'SLV', '222'), ('SY', 'SYR', '760'), ('SZ', 'SWZ', '748'),
    ('TC', 'TCA', '796'), ('TD', 'TCD', '148'), ('TF', 'ATF', '260'),
    ('TG', 'TGO', '768'), ('TH', 'THA', '764'), ('TJ', 'TJK', '762'),
    ('TK', 'TKL', '772'), ('TL', 'TLS', '626'), ('TM', 'TKM', '795'),
    ('TN', 'TUN', '788'), ('TO', 'TON', '776'), ('TR', 'TUR', '792'),
    ('TT', 'TTO', '780'), ('TV', 'TUV', '798'), ('TW', 'TWN', '158'),
    ('TZ', 'TZA', '834'), ('UA', 'UKR', '804'), ('UG', 'UGA', '800'),
    ('UM', 'UMI', '581'), ('US', 'USA', '840'), ('UY', 'URY', '858'),
    ('UZ', 'UZB', '860'), ('VA', 'VAT', '336'), ('VC', 'VCT', '670'),
    ('VE', 'VEN', '862'), ('VG', 'VGB', '092'), ('VI', 'VIR', '850'),
    ('VN', 'VNM', '704'), ('VU', 'VUT', '548'), ('WF', 'WLF', '876'),
    ('WS', 'WSM', '882'), ('YE', 'YEM', '887'), ('YT', 'MYT', '175'),
    ('ZA', 'ZAF', '710'), ('ZM', 'ZMB', '894'), ('ZW', 'ZWE', '716')
]
iso3166_assigned_alpha2 = [v[0] for v in iso3166_assigned]
iso3166_assigned_alpha3 = [v[1] for v in iso3166_assigned]
iso3166_assigned_numeric3 = [v[2] for v in iso3166_assigned]

iso3166_user = [
    'AA', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QU',
    'QV', 'QW', 'QX', 'QY', 'QZ', 'XA', 'XB', 'XC', 'XD', 'XE',
    'XF', 'XG', 'XH', 'XI', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XO', 
    'XP', 'XQ', 'XR', 'XS', 'XT', 'XU', 'XV', 'XW', 'XX', 'XY',
    'XZ', 'ZZ',
]

def valid_ISO3166_1_alpha2(code):
    """Is `code` a valid ISO 3166-1 two character region code in the
    officially assigned or user assigned space. This will return
    `False` if code is in exceptionally, transitionally, and
    indeterminately reserved spaces, or is not used, or is unassigned.
    """
    code = str(code)
    if len(ode) != 2:
        return False
    if code in iso3166_user:
        return True
    return code in iso3166_assigned_alpha2

def valid_ISO3166_1_alpha3(code):
    """Is `code` a valid ISO 3166-1 three character region code in the
    officially assigned or user assigned space. This will return
    `False` if code is in exceptionally, transitionally, and
    indeterminately reserved spaces, or is not used, or is unassigned.
    """
    code = str(code)
    if len(code) != 2:
        return False
    if code[0:1] == 'AA':
        return True
    if code[0] == 'Q' and code[1] in ['MNOPQRSTUVWXYZ']:
        return True
    if code[0] == 'X' or code[0] == 'Z':
        return True
    return code in iso3166_assigned_alpha3

def valid_ISO3166_1_numeric(code):
    """Is `code` a valid ISO 3166-1 three digit region code in the
    officially assigned space.
    """
    code = str(code)
    if len(code) != 3:
        return False
    return code in iso3166_assigned_numeric3





