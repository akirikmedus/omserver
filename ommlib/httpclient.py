# httpclient.py

import urllib
import urllib2
import logging


logger = logging.getLogger('omserver.httpclient')


testReplyNoLicense = ""
""""msg:^License disabled|MSG_LICENSE_DISABLED
status:^LICENSE_DISABLED
dt:^20171106
<br>"""


testReplyLicenseVerified = ""
"""msg:^License verified|MSG_LICENSE_VERIFIED
status:^OK
dt:^20171106
<br>"""


testReplyLicenseIssued = """msg:^License issued|MSG_LICENSE_ISSUED
status:^LICENSE_ISSUED
licHashCode:^120e8c04b29bba99b64359adf54a5c99b738a703
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
Section1=Server Options
Section2=Study List Options
Section3=Clinical Viewer Options
Section4=First Year Support
Group1=radCloud Backup
Group2=Practice Management Interface
Group3=Advanced PACS Management
Group4=CD Burning
OPT1=1|0|-1|RSS|RadStor Server
OPT2=1|0|1|FST|Flex Storage Extension
OPT3=1|1|0|RAB|Remote Automatic Backup
OPT4=1|1|0|IOA|Instant Online Access
OPT5=1|1|0|FBC|Full Business Continuance
OPT6=1|2|1|HL7S|HL7 - Standard Interface
OPT7=1|2|0|HL7A|HL7 - Advanced Integration
OPT8=1|0|1|ORD|Ordering
OPT9=1|0|-1|MOD|Modality Interface
OPT10=1|0|-1|PUSH|DICOM Push
OPT11=1|0|0|PRR|Push for Remote Read
OPT12=1|0|0|MWLSCU|DICOM Worklist SCU
OPT13=1|0|-1|DQ&R|DICOM Query and Retrieve
OPT14=1|0|0|REM|Secure Remote Access (HTTPS)
OPT15=1|0|1|IPAD|iPad Connectivity
OPT16=1|0|0|ANDR|Android Connectivity
OPT17=1|3|1|DASH|System Dashboard
OPT18=1|3|1|ACTR|Activity Reports
OPT19=1|3|1|STOA|Storage Analysis
OPT20=1|3|1|DICU|DICOM Utilities
OPT21=2|0||BSL|RadStor Study List
OPT22=2|0|1|CFIL|Customizable Filtering
OPT23=2|0|1|DSR|Document Scanning and Rendering
OPT24=2|0|1|MMI|Multimedia Import and Rendering
OPT25=2|0|1|CDI|CD Import
OPT26=2|4|1|CDB|Standard CD Burning
OPT27=2|4|0|LSO|LightScribe Option
OPT28=2|4|0|CDPUB|CD Publishing Option
OPT29=2|0|1|VCDP|Virtual CD Publishing
OPT30=2|0|0|VCDI|Virtual CD Import
OPT31=2|0|0|OCC|On Call Caching
OPT32=3|0||RSV|RadStor Viewer
OPT33=3|0|1|REP|Reporting and Study Workflow
OPT34=3|0|1|DIPB|Dictation and Playback
OPT35=3|0|1|AMA|Advanced Measurement and Annotation
OPT36=3|0|1|WDP|Windows Print
OPT37=3|0|1|DICP|DICOM Print
OPT38=3|0|1|MMS|Multi Monitor Support
OPT39=0|0|-1|CLIENT_NO|Number of Client Computers using Study List / Viewer
OPT40=4|0|0|MAIN|Maintenance
OPT41=4|0|1|MASU|Maintenance and Support
OPT42=4|0|0|BIA|Blocked Internet Access
OPT43=3|0|1|RVENBL|radViewer Enabled
SpecialConditions=no

[PRIVILEGES]
omacm_admin=8E597305B950CEE989ACD3189E176822699CBA8F
omadmin_cc=37E1B1C6FD2E68C49FC2EC982DBF01E68AD421CC
omadmin_console=7B4813DF56C3C50826613E46580E3FBD6E284E78
omadmin_db_check=1130BD56CC2726DF32AECA00305AD53FE7C8E01F
omadmin_dict=7F7CEF4DA70B6AA4962EC93FF61C14902E2A642C
omadmin_erpr=DED61BAA5BED990526C08C65DB2B54941A4E3722
omadmin_file_audit=D3AAF37BB73F9095D0E46034332CEB39315B7E4A
omadmin_flex=BF09025526E10BCD9A3AB5686B4166B88824DFAD
omadmin_hp=39D7BDF5A111C50EA2789605B4E4170A9CBF0FC5
omadmin_kds=A14FE61BA71957C25853B36A9529215AE7DE6D6F
omadmin_push=4B8AF49F6D6DF34F2109AB8904FF5C90128D737B
omadmin_run=7074C61870748E9BC4A6B5EF56CACE419EE856D1
omadmin_utils=01DEA45923B5E8786B2E69B63DCCD4975B71496D
omsdm_power_on=6129AE9B19FE0E51D7B2686359F5353D9163C8B2
omstm_admin=D7542F6B6754DFA3C068C93608EFEAC7DB78D767
omusl_manage_patients=3A64751A66C95A4787312E96EDFC0A7EE7EB6B2B
omusl_manage_studies=A40A804EE48E626FBAC347E5BF9C1C2A72F83F59
omusl_profile=0D0C7ED4B7099356E8CA424C64E824000D10E1D8
omusl_push_monitor=FB6C260A53B158D2AA357CF299A59BA31A1078EA
omusl_run=7DC796E716CED95915F94FA317DB9626F8DC14CF
omusl_study_status=8CFAAC901C5DCDE74F71DAAE8A340D497C1CD335
omv_add_report=E34A32D124391394EF28B968478E2AA69CE7FF99
omv_edit_report=88C59FED3C19526D91901D4151B11481A484F590
omv_push=45D0C47B83D6F65DDAA36D935DC9B2F4E6222210
omv_save_anno=8740D440A0403F5A75A5DD39E05D50E08C51E4B0
omv_search=1160BDDB710F699B2562AFB54E77BFFD79FDA673
omv_show_anno=0F2176F695A02A5DA575DB0F08795D4F5DF04B74
omv_view=B76FB9B1C4BB486EE535AD6587536E0AC2BC40D1
omx_multy=49E2B29CDCE5CDF4374E2B9999E37843AAE77511
omx_run=B61D178F95FE7B83A61FD57A645032B7873C94F8
autoupdate_run=ED0401D38EBCED0DA7E93CA4800B823EB62948E3
omusl_adv_demo=B4D5F135C43C82F81CAB9C3C18A8096486BC5734
omusl_adv_filters=A2F265139B6FD41FF6E81530FC88A06776EA9744
omusl_scanner=6590A3E4F9D06AA00A54F44341EF48CA20216817
omusl_attach=E9263CB27000C499A11698D6D1E612DA4B904AA0
omusl_non_dicom=34F51A703177CFB5505DE4DDBE640CB1FBA9C5B2
omusl_cd_import=76BCB2FA80031A7EB89E742E8B1B7735A09D67BD
omusl_jpeg_export=AF8428412260C25E85D679A0D313AC32BB6E1A38
omv_adv_anno=7950BFF11E845BABB219B8B42E65F2B3C39DF4D7
pacs_wklst_scp=E2434B8A99F8932D63047118B56B380356809142
pacs_report_activity=F6DC788F4447BFCF1B83476EE194E7B18F3EFBAD
pacs_hl7=B43026E5D9F4573CAD2C2E257D7CC23EEFD5167D
pacs_ipad=68DC8BBAB4D05E349083CC8A3EE47A23FEF99142
omusl_vcd=C186B3A8249FE769FCFFB6730745F78E8B7C787F
rsvw_dictation=5B1FF11ED65DEBD8F7F405978AF9B61967346A0E
omv_print=6276FDE0DF5EA34EBBE23423B316DF59006D8274
omv_dicom_print=8C61A57DC5A39CCCBD7C682ABF5E69A5DC78B88B
omv_multi_monitor=7CDB99AA55CE765A3F1969644E77A4808F6A63DA
omusl_radviewer=1AAAB0413A817535B0D408A3BEBC6097477C967BendOfLicString
t:^20171030"""


def getLicenseInfo(productkey, mc, regtype, lichashcode, ts):
    ''' Download/Verify license file
        Ready to use
    '''

    if testReplyNoLicense:
        return (True, testReplyNoLicense)

    if testReplyLicenseVerified:
        return True, testReplyLicenseVerified

    if testReplyLicenseIssued:
        return True, testReplyLicenseIssued

    url = "http://pacs-stor.com/support/licact/registrationCheck.php"

    params = {
        'productKey': productkey,  # '1234-5678',
        'mc': mc,                  # '12345678',
        'regtype': regtype,        # 'VERIFY', #'GET_LICENSE'
        'licHashCode': lichashcode,
        'ts': ts
    }

    try:
        querystring = urllib.urlencode(params)

        req = urllib2.Request(url, querystring)
        resp = urllib2.urlopen(req)
        data = resp.read()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        return False, ""

    #logger.info('HTTP response: ' + data)
    return True, data


def test_getLicenseInfo_():
    print ("=== getLicenseInfo ===")
    (gotit, data) = getLicenseInfo('1234-5678', '12345678', 'GET_LICENSE', '', '')
    if(gotit and 0 == data.find("msg:^")):
        print("OK")
    else:
        print("Failed")


if __name__ == '__main__':
    test_getLicenseInfo_()

