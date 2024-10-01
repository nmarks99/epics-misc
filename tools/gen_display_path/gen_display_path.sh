#!/bin/bash -f

DISPLAY_MANAGER=$1

# caller (typically: start_****_xxx) MUST define:
EPICS_APP=./
EPICS_APP_ADL_DIR=./
# EPICS_APP_UI_DIR  - Location of ui file directory


#######################################
# support function to simplify repetitive task,
# used to build up displaty path of supported modules
#
# usage::
#
#    addModule ENVIRONMENT_VARIABLE DISPLAY_TYPE [SUBDIRECTORY]
#
# TMP is a temporary display path
# TMP is internal to this script, no need to export.

function addModule
{
    # $1 is a symbol defined in <synApps>/configure/RELEASE
    # module_path is the path defined for that symbol in the RELEASE file
    module='$'$1
    module_path=`eval echo $module`

	if [ "$2" != "${DISPLAY_MANAGER}" ]; then
		return 0
	fi
	
    if [ "" != "${module}" ]; then
        # module is required
        addition=${module_path}
        if [ "" != "$3" ]; then
            # optional subdirectory path
            addition+=/$3
        fi
        if [ -d "${addition}" ]; then
            # proceed ONLY if new addition path exists
            # Then, can define paths to all area detectors specific screens
            if [ "" == "${TMP}" ]; then
                # no existing path defined, start here
                TMP=.
            fi
            TMP+=:${addition}
        fi
    fi
}


#######################################
# get environment variables for support modules 

output=`perl -s $EPICS_APP/release.pl -form=bash  $EPICS_APP`
eval $output


# ========  ================     ===============          ===========================
# function  MODULE_VARIABLE      Display Manager          subdirectory with .ui files
# ========  ================     ===============          ===========================
addModule   EPICS_APP_ADL_DIR    medm                     
addModule   EPICS_APP_UI_DIR     caqtdm                   
addModule   EPICS_APP_UI_DIR     caqtdm                   /autoconvert

addModule   ALIVE                medm                     /aliveApp/op/adl
addModule   ALIVE                caqtdm                   /aliveApp/op/ui
addModule   ALIVE                caqtdm                   /aliveApp/op/ui/autoconvert

addModule   AREA_DETECTOR        medm                     /ADCore/ADApp/op/adl
addModule   AREA_DETECTOR        caqtdm                   /ADCore/ADApp/op/ui
addModule   AREA_DETECTOR        caqtdm                   /ADCore/ADApp/op/ui/autoconvert

addModule   ADSIMDETECTOR        medm                     /simDetectorApp/op/adl
addModule   ADSIMDETECTOR        caqtdm                   /simDetectorApp/op/ui
addModule   ADSIMDETECTOR        caqtdm                   /simDetectorApp/op/ui/autoconvert

addModule   ADANDOR              medm                     /andorApp/op/adl
addModule   ADANDOR              caqtdm                   /andorApp/op/ui
addModule   ADANDOR              caqtdm                   /andorApp/op/ui/autoconvert

addModule   ADANDOR3             medm                     /andor3App/op/adl
addModule   ADANDOR3             caqtdm                   /andor3App/op/ui
addModule   ADANDOR3             caqtdm                   /andor3App/op/ui/autoconvert

addModule   ADARAVIS             medm                     /aravisApp/op/adl
addModule   ADARAVIS             caqtdm                   /aravisApp/op/ui
addModule   ADARAVIS             caqtdm                   /aravisApp/op/ui/autoconvert

addModule   ADEIGER              medm                     /eigerApp/op/adl
addModule   ADEIGER              caqtdm                   /eigerApp/op/ui
addModule   ADEIGER              caqtdm                   /eigerApp/op/ui/autoconvert

addModule   ADGENICAM            medm                     /GenICamApp/op/adl
addModule   ADGENICAM            caqtdm                   /GenICamApp/op/ui
addModule   ADGENICAM            caqtdm                   /GenICamApp/op/ui/autoconvert

addModule   ADMAR345             medm                     /mar345App/op/adl
addModule   ADMAR345             caqtdm                   /mar345App/op/ui
addModule   ADMAR345             caqtdm                   /mar345App/op/ui/autoconvert

addModule   ADMARCCD             medm                     /marCCDApp/op/adl
addModule   ADMARCCD             caqtdm                   /marCCDApp/op/ui
addModule   ADMARCCD             caqtdm                   /marCCDApp/op/ui/autoconvert

addModule   ADPILATUS            medm                     /pilatusApp/op/adl
addModule   ADPILATUS            caqtdm                   /pilatusApp/op/ui
addModule   ADPILATUS            caqtdm                   /pilatusApp/op/ui/autoconvert

addModule   ADPOINTGREY          medm                     /pointGreyApp/op/adl
addModule   ADPOINTGREY          caqtdm                   /pointGreyApp/op/ui
addModule   ADPOINTGREY          caqtdm                   /pointGreyApp/op/ui/autoconvert

addModule   ADPROSILICA          medm                     /prosilicaApp/op/adl
addModule   ADPROSILICA          caqtdm                   /prosilicaApp/op/ui
addModule   ADPROSILICA          caqtdm                   /prosilicaApp/op/ui/autoconvert

addModule   ADURL                medm                     /urlApp/op/adl
addModule   ADURL                caqtdm                   /urlApp/op/ui
addModule   ADURL                caqtdm                   /urlApp/op/ui/autoconvert

addModule   ADVIMBA              medm                     /vimbaApp/op/adl
addModule   ADVIMBA              caqtdm                   /vimbaApp/op/ui
addModule   ADVIMBA              caqtdm                   /vimbaApp/op/ui/autoconvert

addModule   ASYN                 medm                     /opi/medm
addModule   ASYN                 caqtdm                   /opi/caqtdm
addModule   ASYN                 caqtdm                   /opi/caqtdm/autoconvert

addModule   AUTOSAVE             medm                     /asApp/op/adl
addModule   AUTOSAVE             caqtdm                   /asApp/op/ui
addModule   AUTOSAVE             caqtdm                   /asApp/op/ui/autoconvert

addModule   BUSY                 medm                     /busyApp/op/adl
addModule   BUSY                 caqtdm                   /busyApp/op/ui
addModule   BUSY                 caqtdm                   /busyApp/op/ui/autoconvert

addModule   CALC                 medm                     /calcApp/op/adl
addModule   CALC                 caqtdm                   /calcApp/op/ui
addModule   CALC                 caqtdm                   /calcApp/op/ui/autoconvert

addModule   CAMAC                medm                     /camacApp/op/adl
addModule   CAMAC                caqtdm                   /camacApp/op/ui
addModule   CAMAC                caqtdm                   /camacApp/op/ui/autoconvert

addModule   CAPUTRECORDER        medm                     /caputRecorderApp/op/adl
addModule   CAPUTRECORDER        caqtdm                   /caputRecorderApp/op/ui
addModule   CAPUTRECORDER        caqtdm                   /caputRecorderApp/op/ui/autoconvert

addModule   DAC128V              medm                     /dac128VApp/op/adl
addModule   DAC128V              caqtdm                   /dac128VApp/op/ui
addModule   DAC128V              caqtdm                   /dac128VApp/op/ui/autoconvert

addModule   DELAYGEN             medm                     /delaygenApp/op/adl
addModule   DELAYGEN             caqtdm                   /delaygenApp/op/ui
addModule   DELAYGEN             caqtdm                   /delaygenApp/op/ui/autoconvert

addModule   DXP                  medm                     /dxpApp/op/ui
addModule   DXP                  caqtdm                   /dxpApp/op/ui
addModule   DXP                  caqtdm                   /dxpApp/op/ui/autoconvert

addModule   DXPSITORO            medm                     /dxpSITOROApp/op/adl
addModule   DXPSITORO            caqtdm                   /dxpSITOROApp/op/ui
addModule   DXPSITORO            caqtdm                   /dxpSITOROApp/op/ui/autoconvert

addModule   DEVIOCSTATS          medm                     /op/adl
addModule   DEVIOCSTATS          caqtdm                   /op/ui
addModule   DEVIOCSTATS          caqtdm                   /op/ui/autoconvert

addModule   FLY                  medm                     /flyApp/op/adl
addModule   FLY                  caqtdm                   /flyApp/op/ui
addModule   FLY                  caqtdm                   /flyApp/op/ui/autoconvert

addModule   GALIL                medm                     /GalilSup/op/adl
addModule   GALIL                caqtdm                   /GalilSup/op/ui
addModule   GALIL                caqtdm                   /GalilSup/op/ui/autoconvert

addModule   IP                   medm                     /ipApp/op/adl
addModule   IP                   caqtdm                   /ipApp/op/ui
addModule   IP                   caqtdm                   /ipApp/op/ui/autoconvert

addModule   IP330                medm                     /ip330App/op/adl
addModule   IP330                caqtdm                   /ip330App/op/ui
addModule   IP330                caqtdm                   /ip330App/op/ui/autoconvert

addModule   IPUNIDIG             medm                     /ipUnidigApp/op/adl
addModule   IPUNIDIG             caqtdm                   /ipUnidigApp/op/ui
addModule   IPUNIDIG             caqtdm                   /ipUnidigApp/op/ui/autoconvert

# addModule   LABJACK              medm                     /LabJackApp/op/adl
# addModule   LABJACK              caqtdm                   /LabJackApp/op/ui
# addModule   LABJACK              caqtdm                   /LabJackApp/op/ui/autoconvert

addModule   LOVE                 medm                     /loveApp/op/adl
addModule   LOVE                 caqtdm                   /loveApp/op/ui
addModule   LOVE                 caqtdm                   /loveApp/op/ui/autoconvert

addModule   LUA                  medm                     /luaApp/op/adl
addModule   LUA                  caqtdm                   /luaApp/op/ui
addModule   LUA                  caqtdm                   /luaApp/op/ui/autoconvert

addModule   MCA                  medm                     /mcaApp/op/adl
addModule   MCA                  caqtdm                   /mcaApp/op/ui
addModule   MCA                  caqtdm                   /mcaApp/op/ui/autoconvert

addModule   MEASCOMP             medm                     /measCompApp/op/adl
addModule   MEASCOMP             caqtdm                   /measCompApp/op/ui
addModule   MEASCOMP             caqtdm                   /measCompApp/op/ui/autoconvert

addModule   MODBUS               medm                     /modbusApp/op/adl
addModule   MODBUS               caqtdm                   /modbusApp/op/ui
addModule   MODBUS               caqtdm                   /modbusApp/op/ui/autoconvert

addModule   MOTOR                medm                     /motorApp/op/adl
addModule   MOTOR                caqtdm                   /motorApp/op/ui
addModule   MOTOR                caqtdm                   /motorApp/op/ui/autoconvert

addModule   OPTICS               medm                     /opticsApp/op/adl
addModule   OPTICS               caqtdm                   /opticsApp/op/ui
addModule   OPTICS               caqtdm                   /opticsApp/op/ui/autoconvert

addModule   QUADEM               medm                     /quadEMApp/op/adl
addModule   QUADEM               caqtdm                   /quadEMApp/op/ui
addModule   QUADEM               caqtdm                   /quadEMApp/op/ui/autoconvert

addModule   SCALER               medm                     /scalerApp/op/adl
addModule   SCALER               caqtdm                   /scalerApp/op/ui
addModule   SCALER               caqtdm                   /scalerApp/op/ui/autoconvert

addModule   SOFTGLUE             medm                     /softGlueApp/op/adl
addModule   SOFTGLUE             caqtdm                   /softGlueApp/op/ui
addModule   SOFTGLUE             caqtdm                   /softGlueApp/op/ui/autoconvert

addModule   SOFTGLUEZYNQ         medm                     /softGlueApp/op/adl
addModule   SOFTGLUEZYNQ         caqtdm                   /softGlueApp/op/ui
addModule   SOFTGLUEZYNQ         caqtdm                   /softGlueApp/op/ui/autoconvert

addModule   SSCAN                medm                     /sscanApp/op/adl
addModule   SSCAN                caqtdm                   /sscanApp/op/ui
addModule   SSCAN                caqtdm                   /sscanApp/op/ui/autoconvert

addModule   STD                  medm                     /stdApp/op/adl
addModule   STD                  caqtdm                   /stdApp/op/ui
addModule   STD                  caqtdm                   /stdApp/op/ui/autoconvert

addModule   TDS3000              medm                     /medm

addModule   VAC                  medm                     /vacApp/op/adl
addModule   VAC                  caqtdm                   /vacApp/op/ui
addModule   VAC                  caqtdm                   /vacApp/op/ui/autoconvert

addModule   VME                  medm                     /vmeApp/op/adl
addModule   VME                  caqtdm                   /vmeApp/op/ui
addModule   VME                  caqtdm                   /vmeApp/op/ui/autoconvert

addModule   XPRESS3              medm                     /xpress3App/opi/adl
addModule   XPRESS3              caqtdm                   /xpress3App/opi/ui
addModule   XPRESS3              caqtdm                   /xpress3App/opi/ui/autoconvert

addModule   YOKOGAWA_DAS         medm                     /mw100App/op/adl
addModule   YOKOGAWA_DAS         caqtdm                   /mw100App/op/ui
addModule   YOKOGAWA_DAS         caqtdm                   /mw100App/op/ui/autoconvert

# ========  ================  ===========================

if [ "$DISPLAY_MANAGER" == "medm" ]; then
	if [ -z "$EPICS_DISPLAY_PATH" ]; then
		export EPICS_DISPLAY_PATH=${TMP}
	else
		export EPICS_DISPLAY_PATH=${TMP}:${EPICS_DISPLAY_PATH}
	fi
        echo "$EPICS_DISPLAY_PATH" > medm_display_path_all.txt
fi

if [ "$DISPLAY_MANAGER" == "caqtdm" ]; then
	if [ -z "$CAQTDM_DISPLAY_PATH" ]; then
		export CAQTDM_DISPLAY_PATH=${TMP}
	else
		export CAQTDM_DISPLAY_PATH=${TMP}:${CAQTDM_DISPLAY_PATH}
	fi
        echo "$CAQTDM_DISPLAY_PATH" > caqtdm_display_path_all.txt
fi

