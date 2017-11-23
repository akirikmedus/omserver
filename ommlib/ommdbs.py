# ommdbs.py

import ConfigParser
import pkgutil
import re
import logging
import os.path
import sybpydb

# logger = logging.getLogger(__name__)
logger = logging.getLogger('omserver.ommdbs')


testProductKey = """16C1-036E-19CE-03D6"""


def getOneValue(sql):
    # logger.info("getOneValue")

    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = sybpydb.connect(servername=values[0], user=values[1], password=values[2])
        c = db.cursor()
        c.execute("use us")
        # print("executeSql. SQL: "+sql)
        # logger.info("executeSql. SQL: " + sql)
        c.execute(sql)
        # print(c.rowcount)
        data = c.fetchall()
        c.execute("select @@rowcount")
        # count = c.fetchall()[0][0]
        # print(count)
        c.close()
        db.close()
        return data[0][0] # first row, first column
        #return (string.join([row[0] for row in c.fetchall()], '\n'))
    except (SystemExit, KeyboardInterrupt):
        raise
    except sybpydb.Error:
        for err in c.connection.messages:
            logger.error("Exception %s, Value %s" % (err[0], err[1]))
    except Exception:
        logger.error('Failed', exc_info=False)
    return ''


def executeSql(sql):
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = sybpydb.connect(servername=values[0], user=values[1], password=values[2])
        c = db.cursor()
        c.execute("use us")
        # print("executeSql. SQL: "+sql)
        # logger.info("executeSql. SQL: "+sql)
        c.execute(sql)
        c.execute("select @@rowcount")
        count = c.fetchall()[0][0]
        c.close()
        db.close()
        return count
    except (SystemExit, KeyboardInterrupt):
        raise
    except sybpydb.Error:
        for err in c.connection.messages:
            logger.error("Exception %s, Value %s" % (err[0], err[1]))
    except Exception:
        logger.error('Failed', exc_info=False)
    return 0


def getSiteID():
    sql = "SELECT site_id, name, type FROM sites"
    return getOneValue(sql)


def getProductKey():
    # logger.info("getProductKey")

    if testProductKey:
        return testProductKey

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
    fp.close()

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
    if sToLog:
        logger.info(sToLog)

    updated = 0
    if sToDB:
        sql = "UPDATE tm_prefs SET value ='" + sToDB + "' WHERE name = 'LCS' AND param = 'last_check'"
        updated = executeSql(sql)
        if updated < 1:
            sql = "INSERT INTO tm_prefs (name, param, value) values ('LCS', 'last_check', '" + sToDB + "')"
            updated = executeSql(sql)

    return updated


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
        db = sybpydb.connect(servername=values[0], user=values[1], password=values[2])
        c = db.cursor()
        c.execute("use us")
        c.execute("select name from tm_prefs")
        data = c.fetchall()
        # name = data[0][0]  # first row, first column
        okay = True
    except (SystemExit, KeyboardInterrupt):
        raise
    except sybpydb.Error:
        okay = False
    except Exception:
        okay = False

    if not okay:
        sql = "create table tm_prefs (name varchar(64) not null, param varchar(64) not null, value varchar(255) null, primary key (name, param) )"
        try:
            c.execute(sql)
            c.close()
            db.close()
        except (SystemExit, KeyboardInterrupt):
            raise
        except sybpydb.Error:
            for err in c.connection.messages:
                logger.error("Exception %s, Value %s" % (err[0], err[1]))
        except Exception:
            logger.error('Failed', exc_info=True)


def test_hideDisabled_isDisabled_():
    print ("=== hideDisabled & isDisabled ===")
    hideDisabled(False)
    result = isDisabled()
    hideDisabled(True)
    result2 = isDisabled()
    if not result and result2:
        print("OK")
    else:
        print("Failed. result="+str(result)+", result2="+str(result2))


def test_getSiteID_():
    print ("=== getSiteID ===")
    if 'LT1-' == getSiteID():
        print("OK")
    else:
        print("Failed")


def test_reportLicenseCheck_():
    print ("=== reportLicenseCheck ===")
    updated = reportLicenseCheck('', 'test')
    if 1 == updated:
        print("OK")
    else:
        print("Failed. updated="+str(updated))


if __name__ == '__main__':
    test_hideDisabled_isDisabled_()
    # test_getSiteID_()
