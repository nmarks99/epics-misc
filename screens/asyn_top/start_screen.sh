#!/usr/bin/env bash

export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:/APSshare/epics/synApps_6_3/support/asyn-R4-44-2/opi/caqtdm:/APSshare/epics/synApps_6_3/support/asyn-R4-44-2/opi/caqtdm/autoconvert"
PREFIX="4idhSoft:"
# /APSshare/bin/caQtDM -macro "P=${PREFIX}" topAsyn8x.ui &
/APSshare/bin/caQtDM -macro "P=${PREFIX}" topAsyn16x.ui &
