=========
pyietflib
=========

A library that will convert IETF RFC and STD text representations
(e.g. vCard) into python objects, and for writing those objects back
to text representations.

This allows for easy creation and interpretation of RESTful resources
that are well defined by an IANA media type.

For example a request is made for a `text/vcard;version=4.0;charset=UTF-8`
resource. The RESTful server could gather all the information together
and put it into an rfc6350 object and then print that object to the
output text stream in accordance with RFC 6350.


.. |date| date:: %Y-%m-%d %H:%M:%S %Z
.. footer::
    | Copyright (C) 2011 Lance Finn Helsten;
    | Licensed under Apache License, Version 2.0.;
    | Document generated: |date|.

