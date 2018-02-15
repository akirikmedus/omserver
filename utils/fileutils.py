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

    return hashlib.sha1(license).hexdigest().upper()


def test_getHash_():
    print ("=== getHash ===")

    if("8812FA2CC436AF0CC2B0C372CE43A6763E57A547" == getHash("fileutils.txt")):
        print("OK")
    else:
        print("Failed")
        print(getHash("fileutils.txt"))

    if ("D2036C0C1905D1591D7087C6D7DD4989A3F5B8C4" == getHash("license.dat")):
        print("OK")
    else:
        print("Failed")
        print(getHash("license.dat"))


if __name__ == '__main__':
    test_getHash_()

