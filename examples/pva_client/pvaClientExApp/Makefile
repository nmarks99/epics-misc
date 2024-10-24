TOP=..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================
PROD_LIBS += pvAccessCA ca pvAccess pvData Com

PROD_HOST += miniget
miniget_SRCS += miniget.cpp
miniget_LIBS += $(EPICS_BASE_HOST_LIBS)

PROD_HOST += miniput
miniput_SRCS += miniput.cpp
miniput_LIBS += $(EPICS_BASE_HOST_LIBS)

PROD_HOST += main
main_SRCS += main.cpp
main_LIBS += $(EPICS_BASE_HOST_LIBS)
main_SYS_LIBS += ncurses

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

