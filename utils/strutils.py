# strutils.py

import logging
import hashlib


logger = logging.getLogger('omserver.strutils')


def getHash(str):
    # logger = logging.getLogger('omserver.strutils.getHash')
    # return (hashlib.sha1("The quick brown fox jumps over the lazy dog").hexdigest())
    return hashlib.sha1(str).hexdigest()


def parseLicenseReturn(data):
    '''Parse http reply from licensing server
        Ready to use
    '''

    gotit = message =  messagecode =  messagestring = status = licensecoderm = license = licenselen = messtimestamp = ""

    for l in data.split("\n"):
        #logger.info(l)
        if(-1 != l.find('msg:^')):
            message = l[5:]
            messagecode, messagestring = message.split("|")
        elif(-1 != l.find('status:^')):
            status = l[8:]
        elif (-1 != l.find('licHashCode:^')):
            licensecoderm = l[13:]
        elif (-1 != l.find('licCount:^')):
            licenselen = l[10:]
        elif (-1 != l.find('ts:^')):
            messtimestamp = l[4:]
        elif (-1 != l.find('licString:^')):
            index = data.find('licString:^')
            if(index > 0):
                license = data[index+11:]
            index = license.find('endOfLicString')
            if(index > 0):
                license = license[:index]

    return (True, message, messagecode, messagestring, status, licensecoderm, license, licenselen, messtimestamp)
