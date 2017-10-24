# fileutils.py

import hashlib
import logging
import os.path


def getHash(filename):
    #logger = logging.getLogger(__name__)
    logger = logging.getLogger('omserver.fileutils.getHash')
    logger.info("getHash" + filename)

    #print (hashlib.sha1("The quick brown fox jumps over the lazy dog").hexdigest())

    if not os.path.isfile(filename):
        logger.error("File doesn't exist: " + filename)
        return

    return hashlib.sha1("Nobody inspects the spanish repetition").hexdigest()


