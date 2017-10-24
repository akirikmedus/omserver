# httpclient.py

import urllib
import urllib2
import logging

logger = logging.getLogger('omserver.httpclient')

def licenseCheck():
    url = "http://pacs-stor.com/support/licact/registrationCheck.php"

    params = {
        'productKey' : '1234-5678',
        'mc' : '12345678',
        'regtype' : 'VERIFY'
    }

    querystring = urllib.urlencode(params)

    req = urllib2.Request(url, querystring)
    resp = urllib2.urlopen(req)
    data = resp.read()

    logger.info(data)

