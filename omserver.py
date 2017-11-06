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


def parseLicenseReturn(data):
    gotit = message =  messagecode =  messagestring = status = licensecoderm = license = licenselen = messtimestamp = ""


    return (True, message, messagecode, messagestring, status, licensecoderm, license, licenselen, messtimestamp)


def getMacAddress():
    ifname = netifaces.interfaces()[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    address = ':'.join(['%02x' % ord(char) for char in info[18:24]])
    return address.replace(':','-')


def deleteLicenseFile(fileName):
    logger.info('delete file: ' + fileName)


def onNoLicense(bDemoLicense, lisenceFile):
    logger.info('onNoLicense')
    db.setUserReplyString('')

    if (not bDemoLicense):
        deleteLicenseFile(lisenceFile)
        db.forseUpdatePrivBasedOnLicensing()


def onNewLicense():
    db.hideDisabled(0)#false


def onOk():
    db.setUserReplyString('')


def onPossibleTransfer():
    db.setUserReplyString('')


def onFailed():
    db.setUserReplyString('')


def onTransferFailed():
    db.setUserReplyString('')


def onTransferDenied():
    db.setUserReplyString('')

def onTransferComplete():
    db.setUserReplyString('')


def onLicenseDisabled():
    db.setUserReplyString('')


def onCorrupted():
    db.setUserReplyString('')


def main():
    strTime = strftime("%Y%m%d%H%M", gmtime())
    # logger.info(strTime)
    strTimeStamp = strftime("%Y%m%d%H%M%S", gmtime())
    # logger.info('time:'+strTimeStamp)

    lisenceFile = "/opt/OMTCmm/cf/license.dat"

    medusHomeDir = r'/opt/OMTCmm/'

    bLicense = os.path.isfile(lisenceFile)
    bDemoLicense = not bLicense
    #if bLicense:
    #    logger.info("License file exist")
    #else:
    #    logger.info("License file not found - " + lisenceFile)

    macaddress = getMacAddress()
    logger.info('mac address: ' + macaddress)

    siteid = db.getSiteID()
    logger.info('site id: ' + siteid)

    productKey = db.getProductKey()
    logger.info('product key: ' + productKey)

    hash = ''
    if bLicense:
        hash = fu.getHash(lisenceFile)
        logger.info('license file hash = ' + hash)
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

    (gotit, data) = hc.getLicenseInfo(productKey, macaddress, request, hash, strTimeStamp)

    if(not gotit):
        str = strTime + '|FAILED_IN_POST|FAILED_IN_POST_MSG|'
        db.reportLicenseCheck('Failed in POST', str)
        return False

    (gotit, message, messagecode, messagestring, status, licensecoderm, license, licenselen, messtimestamp) = parseLicenseReturn(data)

    if(not gotit):
        str = strTime + '|FAILED_IN_POST|FAILED_IN_POST_MSG|Corrupted return from server'
        db.reportLicenseCheck('Corrupted return from server', str)
        return False

    str = strTime + '|' + status + '|' + messagecode + '|' + message
    db.reportLicenseCheck('', str)

    if('PRODUCT_KEY_NOT_REGISTERED' == status or 'NO_LICENSE' == status):
        onNoLicense(bDemoLicense, lisenceFile)

    elif('LICENSE_ISSUED' == status):
        onNewLicense()

    elif('OK' == status):
        onOk()

    elif ('POSSIBLE_TRANSFER' == status):
        onPossibleTransfer()

    elif ('FAILED' == status):
        onFailed()

    elif ('TRANSFER_FAILED' == status):
        onTransferFailed()

    elif ('TRANSFER_DENIED' == status):
        onTransferDenied()

    elif ('TRANSFER_COMPLETE' == status):
        onTransferComplete()

    elif ('LICENSE_DISABLED' == status):
        onLicenseDisabled()

    elif ('CORRUPTED' == status):
        onCorrupted()

    else:
        logger.error('something is wrong, should not be here')

if __name__ == '__main__':
    initLogger()
    logger.info("===   Start   ===")
    main()
    logger.info("=== All  Done ===")
