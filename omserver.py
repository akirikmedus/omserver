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
    #logging.basicConfig(level=logging.ERROR)
    handler = logging.handlers.RotatingFileHandler("omserver.log", 'a', 1024, 3)
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

def main():
    srTime = strftime("%Y%m%d%H%M", gmtime())
    strTimeStamp = strftime("%Y%m%d%H%M%S", gmtime())
    #print strTimeStamp

    lisenceFile = "/opt/OMTCmm/cf/license.dat"
    if os.path.isfile(lisenceFile):
        logger.info("License file exist")
    else:
        logger.info("License file not found - " + lisenceFile)

    db.getSiteID()
    hc.licenseCheck()
    logger.info(fu.getHash(""))
    #logger.info(getHwAddr("ens33"))
    print (getMacAddress())


if __name__ == '__main__':
    initLogger()
    logger.info("===   Start   ===")
    main()
    logger.info("=== All  Done ===")
