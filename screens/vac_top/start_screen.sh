#!/usr/bin/env bash

export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:/APSshare/epics/synApps_6_3/support/vac-R1-9-2/vacApp/op/ui/autoconvert"
/APSshare/bin/caQtDM -x vacTop4ida.ui &
