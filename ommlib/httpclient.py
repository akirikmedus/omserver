# httpclient.py

import urllib
import urllib2
import logging

logger = logging.getLogger('omserver.httpclient')


def licenseCheck(productkey, mc, regtype, lichashcode, ts):
    url = "http://pacs-stor.com/support/licact/registrationCheck.php"

    params = {
        'productKey': productkey,  #'1234-5678',
        'mc': mc,                  #'12345678',
        'regtype': regtype,        #'VERIFY', #'GET_LICENSE'
        'licHashCode': lichashcode,
        'ts': ts
    }

    querystring = urllib.urlencode(params)

    req = urllib2.Request(url, querystring)
    resp = urllib2.urlopen(req)
    data = resp.read()

    logger.info(data)

