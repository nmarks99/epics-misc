#!/bin/bash

export EPICS_APP="./"
export EPICS_APP_ADL_DIR="./"
source ${EPICS_APP}/setup_epics_common caqtdm

export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:$(cat ./IOCManager_7ID_display_path.txt)"
/APSshare/bin/caQtDM ./IOCManager_7ID.ui &
