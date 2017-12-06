# strutils.py

import logging
import hashlib


logger = logging.getLogger('omserver.strutils')


def getHash(str):
    ''' returns hash for a string
        Ready to use
    '''
    return hashlib.sha1(str).hexdigest()


def test_getHash_():
    print ("=== getHash ===")
    if '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12' == (hashlib.sha1("The quick brown fox jumps over the lazy dog").hexdigest()):
        print("OK")
    else:
        print("Failed")


def parseLicenseReturn(data):
    '''Parse http reply from licensing server
        Ready to use
    '''

    gotit = message =  messagecode =  messagestring = status = licensecoderm = license = licenselen = messtimestamp = ""

    for l in data.split("\n"):
        # print(l)
        if(-1 != l.find('msg:^')):
            message = l[5:]
            messagestring, messagecode = message.split("|")
        elif(-1 != l.find('status:^')):
            status = l[8:]
        elif (-1 != l.find('licHashCode:^')):
            licensecoderm = l[13:]
        elif (-1 != l.find('licCount:^')):
            licenselen = l[10:]
        elif (-1 != l.find('dt:^')):
            messtimestamp = l[4:]
        elif (-1 != l.find('t:^')):
            messtimestamp = l[3:]
        elif (-1 != l.find('licString:^')):
            index = data.find('licString:^')
            if(index > 0):
                license = data[index+11:]
            index = license.find('endOfLicString')
            if(index > 0):
                license = license[:index]

    return (True, message, messagecode, messagestring, status, licensecoderm, license, licenselen, messtimestamp)


def test_parseLicenseReturn_():
    print ("=== parseLicenseReturn ===")

    testReplyNoLicense = """msg:^License disabled|MSG_LICENSE_DISABLED
status:^LICENSE_DISABLED
dt:^20171106
<br>"""

    (gotit, message, messagecode, messagestring, status, licensecoderm, license, licenselen,
     messtimestamp) = parseLicenseReturn(testReplyNoLicense)

    result = gotit == True \
             and message == 'License disabled|MSG_LICENSE_DISABLED' \
             and messagestring == 'License disabled' \
             and messagecode == 'MSG_LICENSE_DISABLED' \
             and status == 'LICENSE_DISABLED' \
             and messtimestamp == '20171106' \
             and not license \
             and not licenselen \
             and not licensecoderm

    if result:
        print("OK")
    else:
        print("Failed. message="+message+", messagestring="+messagestring+", messagecode="+messagecode+", status="+status+", messtimestamp="+messtimestamp+", licenselen="+licenselen+", licensecoderm="+licensecoderm+", license="+license)

    testReplyLicenseIssued = """msg:^License issued|MSG_LICENSE_ISSUED
status:^LICENSE_ISSUED
licHashCode:^D2036C0C1905D1591D7087C6D7DD4989A3F5B8C4
licCount:^5494
licString:^#
# !!! PLEASE DO NOT EDIT THE CONTENT OF THIS FILE !!!
#

[LICENSE]
Version=2
GenerationDate=2017-10-19
GeneratedBy=Bernard Maury
DistributorName=MedUS, LLC
ExpirationDate=*
TransactionID=226500030451
LicenseType=New License
FeatureSet=0
AutoUpdateTrigger=MEDUS
SupportType=3
MaintanenceExpirationDate=*
Connected=1
Transferable=0

[CUSTOMER]
InstitutionName=MedUS, LLC
SiteID=B0CX
SiteName=BM Laptop 1
SiteKey=16C1-036E
ProductKey=16C1-036E-19CE-03D5

[CAPACITY]
PACSMaxImageCount=-1
PACSMaxPrinters=-1
PACSMaxPushDestinations=-1
PACSMaxModalities=-1
PACSMaxQandR=-1
PACSMaxClients=-1

[OPTIONS]
POMaps=.1.19.17.1.1..33.1.2.1.33.1.1.20.1.1..8.8.1.1.1.33.33.33..1.1.1.1.1..26.26..1.1.22.12.23.24.24.27.25.1.35.14.1.18.3.5.6.7.11.15.16.28.29.30.31.34.36.37.38.4.43
SpecialConditions=no

[PRIVILEGES]
omacm_admin=8E597305B950CEE989ACD3189E176822699CBA8F
omusl_radviewer=1AAAB0413A817535B0D408A3BEBC6097477C967BendOfLicString
t:^20171030"""

    (gotit, message, messagecode, messagestring, status, licensecoderm, license, licenselen,
         messtimestamp) = parseLicenseReturn(testReplyLicenseIssued)

    result = gotit == True \
             and message == 'License issued|MSG_LICENSE_ISSUED' \
             and messagestring == 'License issued' \
             and messagecode == 'MSG_LICENSE_ISSUED' \
             and status == 'LICENSE_ISSUED' \
             and messtimestamp == '20171030' \
             and license \
             and licenselen == '5494' \
             and licensecoderm == 'D2036C0C1905D1591D7087C6D7DD4989A3F5B8C4'

    if result:
        print("OK")
    else:
        print("Failed. message="+message+", messagestring="+messagestring+", messagecode="+messagecode+", status="+status+", messtimestamp="+messtimestamp+", licenselen="+licenselen+", licensecoderm="+licensecoderm+", license="+license)


if __name__ == '__main__':
    test_getHash_()
    test_parseLicenseReturn_()

