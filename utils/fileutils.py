# fileutils.py

import hashlib
import logging
import os.path

logger = logging.getLogger('omserver.fileutils')

def getHash(filename):
    ''' returns hash for a file content
        empty string is files does not exist
        Ready to use
    '''

    if not os.path.isfile(filename):
        logger.error("File doesn't exist: " + filename)
        return ""

    f = open(filename, 'r')
    license = f.read()
    f.close()

    return hashlib.sha1(license).hexdigest()


def test_getHash_():
    print ("=== getHash ===")

    if("8812fa2cc436af0cc2b0c372ce43a6763e57a547" == getHash("fileutils.txt")):
        print("OK")
    else:
        print("Failed")
        print(getHash("fileutils.txt"))


if __name__ == '__main__':
    test_getHash_()

