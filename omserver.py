#!/usr/bin/python

import sys
import string
import logging
import ommlib.ommdb as db

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
    init()
    db.testdb()
    logger.info("DONE")
