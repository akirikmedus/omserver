#!/usr/bin/python

import sys
import string
import logging
import logging.handlers
import ommlib.ommdb as db
import ommlib.httpclient as hc
import utils.fileutils as fu
from time import gmtime, strftime
import os.path
import socket
import fcntl
import struct
import netifaces

#logger = logging.getLogger(__name__)
logger = logging.getLogger('omserver')

def initLogger():
    logging.basicConfig(level=logging.INFO)
    handler = logging.handlers.RotatingFileHandler("omserver.log", 'a', 4096, 3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def getMacAddress():
    ifname = netifaces.interfaces()[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    address = ':'.join(['%02x' % ord(char) for char in info[18:24]])
    return address.replace(':','-')



def deleteLicenseFile(fileName):
    logger.info(fileName)


def main():
    strTime = strftime("%Y%m%d%H%M", gmtime())
    # logger.info(strTime)
    strTimeStamp = strftime("%Y%m%d%H%M%S", gmtime())
    # logger.info(strTimeStamp)

    lisenceFile = "/opt/OMTCmm/cf/license.dat"

    medusHomeDir = r'/opt/OMTCmm/'

    bLicense = os.path.isfile(lisenceFile)
    bDemoLicense = not bLicense
    #if bLicense:
    #    logger.info("License file exist")
    #else:
    #    logger.info("License file not found - " + lisenceFile)

    macaddress = getMacAddress()
    logger.info(macaddress)

    siteid = db.getSiteID()
    logger.info(siteid)

    productKey = db.getProductKey()
    logger.info(productKey)

    hash = ''
    if bLicense:
        hash = fu.getHash(lisenceFile)
        logger.info(hash)
        #bDemoLicense = readFile(lisenceFile).GetStrValue('CUSTOMER', 'SiteKey') == 'DEMO'

    request = 'VERIFY'
    response = db.GetLicenseCheckResponse()       # TRANSFER or HARDWARE_CHANGE
    if('' != response):
        request = response
    else:
        if(bDemoLicense):
            request = 'GET_LICENSE'
        else:
            request = 'VERIFY'

    gotit = hc.getLicenseInfo(productKey, macaddress, request, hash, strTimeStamp)

    if(not gotit):
        str = ''
        db.reportLicenseCheck(str, str)
        return

    gotit = parseLicenseReturn()

    if(not gotit):
        str = ''
        db.reportLicenseCheck(str, str)
        return

    str = ''
    db.reportLicenseCheck(str, str)

    status = ''

    if('PRODUCT_KEY_NOT_REGISTERED' == status or 'NO_LICENSE' == status):
        db.setUserReplyString('')

        if(not bDemoLicense):
            deleteLicenseFile(lisenceFile)
            db.forseUpdatePrivBasedOnLicensing()

        return

    if('LICENSE_ISSUED' == status):
        db.hideDisabled(0)#false

        return

    if('OK' == status):
        db.setUserReplyString('')

        return

    if ('POSSIBLE_TRANSFER' == status):
        db.setUserReplyString('')

        return

    if ('FAILED' == status):
        db.setUserReplyString('')

        return

    if ('TRANSFER_FAILED' == status):
        db.setUserReplyString('')

        return

    if ('TRANSFER_DENIED' == status):
        db.setUserReplyString('')

        return

    if ('TRANSFER_COMPLETE' == status):
        db.setUserReplyString('')

        return

    if ('LICENSE_DISABLED' == status):
        db.setUserReplyString('')

        return

    if ('CORRUPTED' == status):
        db.setUserReplyString('')

        return

if __name__ == '__main__':
    initLogger()
    logger.info("===   Start   ===")
    main()
    logger.info("=== All  Done ===")
