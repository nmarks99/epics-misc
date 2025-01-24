#!/usr/bin/env bash
export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:/APSshare/epics/synApps_6_3/support/motor-R7-3-1/motorApp/op/ui"
export CAQTDM_DISPLAY_PATH="${CAQTDM_DISPLAY_PATH}:/APSshare/epics/synApps_6_3/support/motor-R7-3-1/motorApp/op/ui/autoconvert"

/APSshare/bin/caQtDM ACSMotionMenu.ui
