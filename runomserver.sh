#!/bin/bash
#

#source /home/ati/.profile
source /home/ati/.bash_profile
source /opt/sap/SYBASE.sh

cd /home/ati/omserver
#python /home/ati/omserver/omserver.py >/dev/null 2>&1
python /home/ati/omserver/omserver.py >/home/ati/omserver/omserver-1.log 2>/home/ati/omserver/omserver-2.log


