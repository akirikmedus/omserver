# ommdb.py

import string
import Sybase
import pkgutil
import re
import logging

#logger = logging.getLogger(__name__)
logger = logging.getLogger('omserver.ommdb')

def getSiteID():
    logger.info("getSiteID")

    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        c.execute("select site_id, name, type from sites")
        logger.info(string.join([row[0] for row in c.fetchall()], '\n'))
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('Failed', exc_info=True)
