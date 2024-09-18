#!/bin/bash

# Defines 4 IOCs
IOC1="4ida"
IOC2="4idaSoft"
IOC3="4idHHLM"
IOC4="4idVDCM"
MACROS="IOC1=${IOC1},IOC2=${IOC2},IOC3=${IOC3},IOC4=${IOC4}"

# add adl and ui directories for each IOC to CAQTDM_DISPLAY_PATH
# you will need to do this manually if not all IOCs reside in the same ioc/ dir
IOC_DIR="/net/s4dserv/xorApps/epics/synApps_6_3/ioc/"
for i in 1 2 3 4; do
    IOC_VAR="IOC${i}"
    IOC=${!IOC_VAR}
    export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:${IOC_DIR}/${IOC}/${IOC}App/op/adl"
    export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:${IOC_DIR}/${IOC}/${IOC}App/op/ui"
done

export EPICS_APP="./"
export EPICS_APP_ADL_DIR="./"
source ${EPICS_APP}/setup_epics_common caqtdm

echo $CAQTDM_DISPLAY_PATH

/APSshare/bin/caQtDM -macro $MACROS IOCManager4x.ui &
