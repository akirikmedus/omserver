#!/usr/bin/python

import sys
import string
import logging
import ommlib.ommdb as db
import ommlib.httpclient as hc
import utils.fileutils as fu
from time import gmtime, strftime
import os.path

logger = logging.getLogger(__name__)


def init():
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler("testpython.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


if __name__ == '__main__':
    srTime = strftime("%Y%m%d%H%M", gmtime())
    strTimeStamp = strftime("%Y%m%d%H%M%S", gmtime())
    print strTimeStamp
    lisenceFile = "/opt/OMTCmm/cf/license.dat"
    if os.path.isfile(lisenceFile):
        print("File exist")
    else:
        print("File not found")

    init()
    db.getSiteID()
    hc.licenseCheck()
    print fu.getHash("")
    logger.info("DONE")
