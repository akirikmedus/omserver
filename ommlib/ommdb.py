# ommdb.py

import ConfigParser
import Sybase
import pkgutil
import re
import logging
import os.path

# logger = logging.getLogger(__name__)
logger = logging.getLogger('omserver.ommdb')


testProductKey = """16C1-036E-19CE-03D6"""


def getOneValue(sql):
    # logger.info("getOneValue")

    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        print("getOneValue. SQL: " + sql)
        c.execute(sql)
        data = c.fetchall()
        c.close()
        db.close()
        return data[0][0] # first row, first column
        #return (string.join([row[0] for row in c.fetchall()], '\n'))
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('getOneValue Failed', exc_info=False)
    return ''


def executeSql(sql):
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        print("executeSql. SQL: "+sql)
        c.execute(sql)
        c.execute("select @@rowcount")
        count = c.fetchall()[0][0]
        c.close()
        db.close()
        # return c.rowcount
        return count
        # return 1
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('executeSql Failed', exc_info=False)
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


def updatePrivBasedOnLicensing():

    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()

        sql = "select distinct user_privileges_lc.privilege, user_privileges_lc.description from user_privileges, user_privileges_lc where availability = 0 and user_privileges.privilege = user_privileges_lc.privilege and licensed = 0 "
        c.execute(sql)
        data = c.fetchall()

        for row in data:
            privilege = row[0]
            description = row[1]

            sql = "delete from user_privileges where privilege = '" + privilege + "' and availability = 0"
            c.execute(sql)
            sql = "insert into user_privileges (privilege, availability, group_id, user_id, description) values ('" + privilege +"', 1, '', '', '" + description + "')"
            c.execute(sql)

        bEveryoneCheck = False
        sql = "select distinct user_privileges_lc.privilege, user_privileges_lc.description from user_privileges, user_privileges_lc where availability = 1 and user_privileges.privilege = user_privileges_lc.privilege and licensed = 1 "
        " and user_privileges_lc.privilege in ('omusl_manage_patients', 'omusl_manage_studies', 'omusl_push_monitor', 'omusl_run', 'omusl_study_status',"
        " 'omv_add_report', 'omv_edit_report', 'omv_email', 'omv_push', 'omv_save_anno', 'omv_search', 'omv_show_anno', 'omv_view', 'omx_multy', 'omx_run', 'omusl_vcd',"
        " 'allpro_images', 'omusl_wklst_scu', 'omusl_scanner', 'omusl_attach', 'omusl_non_dicom', 'omusl_lightscribe', 'omusl_cd_import', 'omusl_jpeg_export',"
        " 'omv_adv_anno', 'omv_https', 'omusl_radviewer')"
        c.execute(sql)
        data = c.fetchall()

        for row in data:
            privilege = row[0]
            description = row[1]

            sql = "delete from user_privileges where privilege = '" + privilege + "' and availability = 1"
            c.execute(sql)
            sql = "insert into user_privileges (privilege, availability, group_id, user_id, description) values ('" + privilege +"', 0, 'everyone', '', '" + description + "')"
            c.execute(sql)
            bEveryoneCheck = True

        if (bEveryoneCheck):
            sql = "SELECT group_name FROM groups WHERE group_name = 'everyone'"
            c.execute(sql)
            data = c.fetchall()
            if (data[0][0] != ""):
                sql = "insert into groups (group_name) values ('everyone', '')"
                c.execute(sql)

        bAdminCheck = False
        sql = "select distinct user_privileges_lc.privilege, user_privileges_lc.description from user_privileges, user_privileges_lc where availability = 1 and user_privileges.privilege = user_privileges_lc.privilege and licensed = 1 "
        " and user_privileges_lc.privilege in ('omacm_add_priv', 'omacm_admin', 'omadmin_cc', 'omadmin_console', 'omadmin_db_check', 'omadmin_dict', 'omadmin_distr',"
        " 'omadmin_erpr', 'omadmin_file_audit', 'omadmin_flex', 'omadmin_hp', 'omadmin_kds', 'omadmin_push', 'omadmin_run', 'omadmin_utils', 'omsdm_power_on',"
        " 'omstm_run', 'omstm_admin', 'omusl_profile', 'omv_vitrea', 'pacs_hl7_adv', 'omv_push_adv', 'pacs_ipad', 'pacs_android', 'omx_publishing',"
        " 'omusl_vcd_import', 'omusl_oncall_caching', 'rsvw_dictation', 'omv_print', 'omv_dicom_print', 'omv_multi_monitor', 'autoupdate_run', 'omusl_adv_demo',"
        " 'omusl_adv_filters', 'pacs_wklst_scp', 'pacs_report_activity', 'pacs_backup', 'pacs_backup_adv', 'pacs_hl7', 'pacs_hl7_adv')"

        for row in data:
            privilege = row[0]
            description = row[1]

            sql = "delete from user_privileges where privilege = '" + privilege + "' and availability = 1"
            c.execute(sql)
            sql = "insert into user_privileges (privilege, availability, group_id, user_id, description) values ('" + privilege + "', 0, '', 'admin', '" + description + "')"
            c.execute(sql)
            bAdminCheck = True

        if (bAdminCheck):
            sql = "select user_id from users where user_id = 'admin'"
            c.execute(sql)
            data = c.fetchall()
            if (data[0][0] != ""):
                sql = "insert into users (user_id, name, last_name, first_name, password) values ('admin', 'PACSimple Admin', 'Admin', 'PACSimple', 'admin!')"
                c.execute(sql)

            sql = "select privilege from user_privileges where user_id = 'admin' and privilege = 'omadmin_run'"
            c.execute(sql)
            data = c.fetchall()
            if (data[0][0] != ""):
                c.execute("select description from user_privileges where privilege = 'omadmin_run'")
                sql = "delete from user_privileges where privilege = 'omadmin_run' and availability = 1"
                c.execute(sql)
                data = c.fetchall()
                sDescription = data[0][0]
                sql = "insert into user_privileges (privilege, availability, group_id, user_id, description) values ('omadmin_run', 0, '', 'admin', '" + sDescription + "')"
                c.execute(sql)

            sql = "select privilege from user_privileges where user_id = 'admin' and privilege = 'omacm_admin'"
            c.execute(sql)
            data = c.fetchall()
            if (data[0][0] != ""):
                c.execute("select description from user_privileges where privilege = 'omacm_admin'")
                sql = "delete from user_privileges where privilege = 'omacm_admin' and availability = 1"
                c.execute(sql)
                data = c.fetchall()
                sDescription = data[0][0]
                sql = "insert into user_privileges (privilege, availability, group_id, user_id, description) values ('omacm_admin', 0, '', 'admin', '" + sDescription + "')"
                c.execute(sql)

            sql = "select privilege from user_privileges where user_id = 'admin' and privilege = 'omacm_add_priv'"
            c.execute(sql)
            data = c.fetchall()
            if (data[0][0] != ""):
                c.execute("select description from user_privileges where privilege = 'omacm_add_priv'")
                sql = "delete from user_privileges where privilege = 'omacm_add_priv' and availability = 1"
                c.execute(sql)
                data = c.fetchall()
                sDescription = data[0][0]
                sql = "insert into user_privileges (privilege, availability, group_id, user_id, description) values ('omacm_add_priv', 0, '', 'admin', '" + sDescription + "')"
                c.execute(sql)

            c.close()
        db.close()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('updatePrivBasedOnLicensing Failed', exc_info=False)


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
    sql = "UPDATE tm_prefs SET value ='" + str(sss) + "' WHERE name = 'GLOBAL' AND param = 'pic'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pic', '" + str(sss) + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxPushDestinations")
    sql = "UPDATE tm_prefs SET value ='" + str(sss) + "' WHERE name = 'GLOBAL' AND param = 'pid'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pid', '" + str(sss) + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxModalities")
    sql = "UPDATE tm_prefs SET value ='" + str(sss) + "' WHERE name = 'GLOBAL' AND param = 'pim'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pim', '" + str(sss) + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxQandR")
    sql = "UPDATE tm_prefs SET value ='" + str(sss) + "' WHERE name = 'GLOBAL' AND param = 'piq'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'piq', '" + str(sss) + "')"
        executeSql(sql)

    sss = config.getint("CAPACITY", "PACSMaxClients")
    sql = "UPDATE tm_prefs SET value ='" + str(sss) + "' WHERE name = 'GLOBAL' AND param = 'pil'"
    if executeSql(sql) < 1:
        sql = "INSERT INTO tm_prefs (name, param, value) values ('GLOBAL', 'pil', '" + str(sss) + "')"
        executeSql(sql)


def GetLicenseCheckResponse():
    sql = "select value from tm_prefs where name = 'LCS' and param = 'response'"
    return getOneValue(sql)


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


def checkDBtables(tmPrefsOnly):
    okay = False
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        c.execute("select name from tm_prefs")
        data = c.fetchall()
        okay = True
        logger.info("tm_prefs exists")
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.info("tm_prefs is missing")
        okay = False

    if not okay:
        sql = "create table tm_prefs (name varchar(64) not null, param varchar(64) not null, value varchar(255) null, primary key (name, param) )"
        try:
            c.execute(sql)
            okay = True
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logger.error('Failed', exc_info=True)

    if tmPrefsOnly:
        c.close()
        db.close()
        return okay

    okay2 = False
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        c.execute("SELECT user_id FROM user_privileges")
        data = c.fetchall()
        okay2 = True
        logger.info("user_privileges exists")
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        okay2 = False

    if not okay2:
        sql = "create table user_privileges (privilege varchar(30) not null, availability int not null, group_id varchar(30) null, user_id varchar(30) null, description varchar(128) null )"
        try:
            c.execute(sql)
            okay2 = True
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logger.error('Failed', exc_info=True)

    okay3 = False
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        c.execute("SELECT indx FROM user_privileges_lc")
        data = c.fetchall()
        okay3 = True
        logger.info("user_privileges_lc exists")
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        okay3 = False

    if not okay3:
        sql = "create table user_privileges_lc (indx int not null, privilege varchar(30) not null, description varchar(128) null, licensed int not null )"
        try:
            c.execute(sql)
            okay3 = True
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logger.error('Failed', exc_info=True)

    okay4 = False
    data = pkgutil.get_data(__package__, 'database.dat')
    values = re.split("\W+", data)
    try:
        db = Sybase.connect(values[0], values[1], values[2], values[3])
        c = db.cursor()
        c.execute("SELECT * FROM groups")
        data = c.fetchall()
        okay4 = True
        logger.info("groups exists")
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        okay4 = False

    if not okay4:
        sql = "create table groups (group_name varchar(30) not null, user_id varchar(30) null )"
        try:
            c.execute(sql)
            okay4 = True
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logger.error('Failed', exc_info=True)
        sql = "insert into groups (group_name, user_id) values ('everyone', '')"
        try:
            c.execute(sql)
            okay4 = True
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            logger.error('Failed', exc_info=True)

    c.close()
    db.close()

    return okay and okay2 and okay3 and okay4


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

