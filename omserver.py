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

#logger = logging.getLogger(__name__)
logger = logging.getLogger('omserver')

def initLogger():
    logging.basicConfig(level=logging.ERROR)
    handler = logging.handlers.RotatingFileHandler("omserver.log", 'a', 1024, 3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

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


if __name__ == '__main__':
    initLogger()
    logger.info("===   Start   ===")
    main()
    logger.info("=== All  Done ===")
