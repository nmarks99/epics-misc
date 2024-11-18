#!/usr/bin/env bash

PREFIX="4idaSoft:"

export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:/APSshare/epics/synApps_6_3/support/asyn-R4-44-2/opi/caqtdm:/APSshare/epics/synApps_6_3/support/asyn-R4-44-2/opi/caqtdm/autoconvert"

/APSshare/bin/caQtDM -macro "P=${PREFIX},R=asyn_MOXA_A:1" topAsynRow.ui &
