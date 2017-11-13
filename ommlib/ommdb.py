# ommdb.py

import ConfigParser
import Sybase
import pkgutil
import re
import logging
import os.path

# logger = logging.getLogger(__name__)
logger = logging.getLogger('omserver.ommdb')

def getOneValue(sql):
    # logger.info("getOneValue")

    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        c.execute(sql)
        data = c.fetchall()
        return data[0][0] # first row, first column
        #return (string.join([row[0] for row in c.fetchall()], '\n'))
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('Failed', exc_info=False)


def executeSql(sql):
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        logger.info("executeSql. SQL: "+sql)
        c.execute(sql)
        return c.rowcount
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('Failed', exc_info=False)


def getSiteID():
    sql = "SELECT site_id, name, type FROM sites"
    return getOneValue(sql)


def getProductKey():
    # logger.info("getProductKey")
    return '1234-5678';

    sql = "SELECT value FROM tm_prefs WHERE name = 'GLOBAL' AND param = 'DeviceID'"
    return getOneValue(sql)


def setUserReplyString(request, response):
    # logger.info("setUserReplyString")

    sql = "UPDATE tm_prefs SET value ='" + request + "' WHERE name = 'LCS' AND param = 'request'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs values ('LCS', 'request', '" + request + "')"
        executeSql(sql)

    sql = "UPDATE tm_prefs SET value ='" + response + "' WHERE name = 'LCS' AND param = 'response'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs values ('LCS', 'response', '" + response + "')"
        executeSql(sql)


def updatePrivBasedOnLicensing(): # TODO
    i = 1


def forseUpdatePrivBasedOnLicensing(licenseFile):
    logger.info("forseUpdatePrivBasedOnLicensing")

    if not os.path.isfile(licenseFile):
        logger.error("File path {} does not exists.".format(licenseFile))

    sql = "update user_privileges_lc set licensed = 0"
    executeSql(sql)

    bInPrivs = False
    with open(licenseFile) as fp:
        for line in fp:
            if line == '[PRIVILEGES]':
                bInPrivs = True
            if not bInPrivs:
                continue
            else:
                s = line.split('=')
                sql = "update user_privileges_lc set licensed = 1 where privilege = '" + s + "'"
                executeSql(sql)
    fp.close

    return updatePrivBasedOnLicensing()


def forseUpdateMaxBasedOnLicensing(licenseFile):
    logger.info("forseUpdateMaxBasedOnLicensing")

    config = ConfigParser.RawConfigParser()
    config.read(licenseFile)

    sss = config.getint("CAPACITY", "PACSMaxImageCount")
    sql = "UPDATE tm_prefs SET value ='" + sss + "' WHERE name = 'GLOBAL' AND param = 'pic'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pic', '" + sss + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxPushDestinations")
    sql = "UPDATE tm_prefs SET value ='" + sss + "' WHERE name = 'GLOBAL' AND param = 'pid'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pid', '" + sss + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxModalities")
    sql = "UPDATE tm_prefs SET value ='" + sss + "' WHERE name = 'GLOBAL' AND param = 'pim'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pim', '" + sss + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxQandR")
    sql = "UPDATE tm_prefs SET value ='" + sss + "' WHERE name = 'GLOBAL' AND param = 'piq'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'piq', '" + sss + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxClients")
    sql = "UPDATE tm_prefs SET value ='" + sss + "' WHERE name = 'GLOBAL' AND param = 'pil'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pil', '" + sss + "')"
        executeSql(sql)

def GetLicenseCheckResponse():
    return ''

def reportLicenseCheck(sToLog, sToDB):
    if('' == sToLog):
        logger.info(sToLog)

    if('' == sToDB):
        sql = "UPDATE tm_prefs SET value ='" + sToDB + "' WHERE name = 'LCS' AND param = 'last_check'"
        if executeSql(sql) < 1:
            sql = "INSERT INTO tm_prefs values ('LCS', 'last_check', '" + sToDB + "')"
            executeSql(sql)


def hideDisabled(disabled):
    logger.info("hideDisabled")
    str = "0"
    if disabled:
        str = "1"
    filename = "/opt/OMTCmm/lib/omm23.jar"
    f = open(filename, 'w')
    f.write(str)
    f.close()


def isDisabled():
    logger.info("isDisabled")
    filename = "/opt/OMTCmm/lib/omm23.jar"
    f = open(filename, 'r')
    str = f.read()
    f.close()
    return str == "1"


def checkDBtables():
    okay = False
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        c.execute("select name from tm_prefs")
        data = c.fetchall()
        # name = data[0][0]  # first row, first column
        okay = True
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        okay = False

    if not okay:
        sql = "create table tm_prefs (name varchar(64) not null, param varchar(64) not null, value varchar(255) null, primary key (name, param) )"
        try:
            c.execute(sql)
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logger.error('Failed', exc_info=True)


