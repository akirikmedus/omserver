# fileutils.py

import hashlib
import logging
import os.path


def getHash(filename):
    logger = logging.getLogger('omserver.fileutils.getHash')
    # logger.info("getHash" + filename)

    if not os.path.isfile(filename):
        logger.error("File doesn't exist: " + filename)
        return ""

    f = open(filename, 'r')
    license = f.read()
    f.close()

    return hashlib.sha1(license).hexdigest()


