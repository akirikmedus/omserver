#!/usr/bin/python

import sys
import logging
import logging.handlers
import ommlib.ommdb as db
import ommlib.httpclient as hc
import utils.fileutils as fu
import utils.strutils as su
from time import gmtime, strftime
import os.path
import socket
import fcntl
import struct
import netifaces  # yum install python-netifaces


#logger = logging.getLogger(__name__)
logger = logging.getLogger('omserver')


def initLogger(): # done
    logging.basicConfig(level=logging.INFO)
    handler = logging.handlers.RotatingFileHandler("omserver.log", 'a', 4096, 3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def getMacAddress(): # done
    ifname = netifaces.interfaces()[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    address = ':'.join(['%02x' % ord(char) for char in info[18:24]])
    return address.replace(':','-')


def deleteLicenseFile(fileName): # done
    logger.info('deleting file: ' + fileName)
    try:
        os.remove(fileName)
    except Exception:
        logger.error('Failed to delete file '+fileName, exc_info=False)


def saveLicenseFile(fileName, license): # done
    logger.info('saving license file: ' + fileName)
    try:
        f = open(fileName, 'w')
        f.write(license)
        f.close()
    except Exception:
        logger.error('Failed to save file '+fileName, exc_info=False)


def onNoLicense(bDemoLicense, licenseFile, strTime, status, message, messagecode):  # done
    logger.info('onNoLicense')

    if not messagecode:
        db.setUserReplyString(strTime + '|' + status + '|' + message, '')
    else:
        db.setUserReplyString(strTime + '|' + status + '|' + messagecode, '')

    if not bDemoLicense:
        deleteLicenseFile(licenseFile)
        db.forseUpdatePrivBasedOnLicensing()


def onNewLicense(licenseFile, license, licensecoderm): # done
    logger.info('onNewLicense')

    db.hideDisabled(False)
    # licenseCodeLcNew = su.getHash(license)

    saveLicenseFile(licenseFile, license)
    licenseCodeLcNewFile = fu.getHash(licenseFile)
    if licensecoderm != licenseCodeLcNewFile:
        logger.error("Hash code don't match. Received: " + licensecoderm + " from file: " + licenseCodeLcNewFile)

    db.forseUpdatePrivBasedOnLicensing()
    db.forseUpdateMaxBasedOnLicensing()

    # fu.updateWatcherBasedOnLicensing() - no need

    db.setUserReplyString('', '')


def onTransferComplete(licenseFile, license, licensecoderm): # done
    logger.info('onTransferComplete')

    # licenseCodeLcNew = su.getHash(license)

    db.hideDisabled(False)

    saveLicenseFile(licenseFile, license)
    licenseCodeLcNewFile = fu.getHash(licenseFile)
    if licensecoderm != licenseCodeLcNewFile:
        logger.error("Hash code don't match. Received: " + licensecoderm + " from file: " + licenseCodeLcNewFile)

    db.forseUpdatePrivBasedOnLicensing()

    db.setUserReplyString('', '')


def onOk():  # done
    logger.info('onOk')
    db.setUserReplyString('', '')
    #done here


def onPossibleTransfer(strTime, status, message, messagecode):  # done
    logger.info('onPossibleTransfer')

    if not messagecode:
        db.setUserReplyString(strTime + '|' + status + '|' + message, '')
    else:
        db.setUserReplyString(strTime + '|' + status + '|' + messagecode, '')


def onFailed(productKey, strTime, status, message, messagecode):  # done
    logger.info('onFailed')

    if not productKey:  # no produce key means DEMO:
        # do nothing
        i = 0
    else:
        if not messagecode:
            db.setUserReplyString(strTime + '|' + status + '|' + message, '')
        else:
            db.setUserReplyString(strTime + '|' + status + '|' + messagecode, '')


def onTransferFailed(strTime, status, message, messagecode):  # done
    logger.info('onTransferFailed')

    if not messagecode:
        db.setUserReplyString(strTime + '|' + status + '|' + message, '')
    else:
        db.setUserReplyString(strTime + '|' + status + '|' + messagecode, '')


def onTransferDenied(strTime, status, message, messagecode):  # done
    logger.info('onTransferDenied')

    if not messagecode:
        db.setUserReplyString(strTime + '|' + status + '|' + message, '')
    else:
        db.setUserReplyString(strTime + '|' + status + '|' + messagecode, '')


def onLicenseDisabled(strTime, status, message, messagecode, licenseFile):  # done
    logger.info('onLicenseDisabled')

    if not messagecode:
        db.setUserReplyString(strTime + '|' + status + '|' + message, '')
    else:
        db.setUserReplyString(strTime + '|' + status + '|' + messagecode, '')

    deleteLicenseFile(licenseFile)
    db.hideDisabled(True)


def onCorrupted(licenseFile, strTime, status, message, messagecode, productKey, macaddress, strTimeStamp):
    logger.info('onCorrupted')

    request = 'GET_LICENSE'
    (gotit, data) = hc.getLicenseInfo(productKey, macaddress, request, hash, strTimeStamp)
    logger.info('FROM POST:' + data)

    if (not gotit):
        str = strTime + '|FAILED_IN_POST|FAILED_IN_POST_MSG|'
        db.reportLicenseCheck('Failed in POST', str)
        return False

    (gotit, message, messagecode, messagestring, status, licensecoderm, license, licenselen,
     messtimestamp) = su.parseLicenseReturn(data)
    logger.info('message:' + message + '; status:' + status)

    if (not gotit):
        str = strTime + '|FAILED_IN_POST|FAILED_IN_POST_MSG|Corrupted return from server'
        db.reportLicenseCheck('Corrupted return from server', str)
        return False

    str = strTime + '|' + status + '|' + messagecode + '|' + message
    db.reportLicenseCheck('', str)

    if ('LICENSE_ISSUED' == status):
        return onNewLicense(licenseFile, license, licensecoderm)


def main():
    strTime = strftime("%Y%m%d%H%M", gmtime())
    # logger.info(strTime)
    strTimeStamp = strftime("%Y%m%d%H%M%S", gmtime())
    # logger.info('time:'+strTimeStamp)

    db.checkDBtables()

    licenseFile = "/opt/OMTCmm/cf/license.dat"

    medusHomeDir = r'/opt/OMTCmm/'

    bLicense = os.path.isfile(licenseFile)
    bDemoLicense = not bLicense
    #if bLicense:
    #    logger.info("License file exist")
    #else:
    #    logger.info("License file not found - " + licenseFile)

    macaddress = getMacAddress()
    logger.info('mac address: ' + macaddress)

    siteid = db.getSiteID()
    logger.info('site id: ' + siteid)

    productKey = db.getProductKey()
    logger.info('product key: ' + productKey)

    hash = ''
    if bLicense:
        hash = fu.getHash(licenseFile)
        logger.info('license file hash = ' + hash)
        #bDemoLicense = readFile(licenseFile).GetStrValue('CUSTOMER', 'SiteKey') == 'DEMO'

    request = 'VERIFY'
    response = db.GetLicenseCheckResponse()       # TRANSFER or HARDWARE_CHANGE
    if '' != response:
        request = response
    else:
        if(bDemoLicense):
            request = 'GET_LICENSE'
        else:
            request = 'VERIFY'

    (gotit, data) = hc.getLicenseInfo(productKey, macaddress, request, hash, strTimeStamp)
    logger.info('FROM POST:' + data)

    if not gotit:
        str = strTime + '|FAILED_IN_POST|FAILED_IN_POST_MSG|'
        db.reportLicenseCheck('Failed in POST', str)
        return False

    (gotit, message, messagecode, messagestring, status, licensecoderm, license, licenselen, messtimestamp) = su.parseLicenseReturn(data)
    logger.info('message:'+message+'; status:'+status)

    if not gotit:
        str = strTime + '|FAILED_IN_POST|FAILED_IN_POST_MSG|Corrupted return from server'
        db.reportLicenseCheck('Corrupted return from server', str)
        return False

    str = strTime + '|' + status + '|' + messagecode + '|' + message
    db.reportLicenseCheck('', str)

    if 'PRODUCT_KEY_NOT_REGISTERED' == status or 'NO_LICENSE' == status:
        onNoLicense(bDemoLicense, licenseFile, strTime, status, message, messagecode)

    elif 'LICENSE_ISSUED' == status:
        onNewLicense(licenseFile, license, licensecoderm)

    elif 'OK' == status:
        onOk()

    elif 'POSSIBLE_TRANSFER' == status:
        onPossibleTransfer(strTime, status, message, messagecode)

    elif 'FAILED' == status:
        onFailed(productKey, strTime, status, message, messagecode)

    elif 'TRANSFER_FAILED' == status:
        onTransferFailed(strTime, status, message, messagecode)

    elif 'TRANSFER_DENIED' == status:
        onTransferDenied(strTime, status, message, messagecode)

    elif 'TRANSFER_COMPLETE' == status:
        onTransferComplete(licenseFile, license, licensecoderm)

    elif 'LICENSE_DISABLED' == status:
        onLicenseDisabled(strTime, status, message, messagecode, licenseFile)

    elif 'CORRUPTED' == status:
        onCorrupted(licenseFile, strTime, status, message, messagecode, productKey, macaddress, strTimeStamp)

    else:
        logger.error('something is wrong, should not be here')


def test():
    print ("===  U N I T   T E S T  ===")
    db.test_getSiteID_()
    db.test_reportLicenseCheck_()


if __name__ == '__main__':

    if len(sys.argv) > 1 and "test" == sys.argv[1]:
        test()
    else:
        initLogger()
        logger.info("===   Start   ===")
        main()
        logger.info("=== All  Done ===")
