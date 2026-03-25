# NOTE: paths relative to where they get installed (e.g. ./O.rhel9-x86_64)

TOP=../..

include $(TOP)/configure/CONFIG

# Define IOC library name
LIBRARY_IOC += testDriver

# install testDriverSupport.dbd into <top>/dbd
DBD += testDriverSupport.dbd
testDriverSupport_DBD += testDriver.dbd

# source files to be compiled and added to the library
testDriver_SRCS += drvA.cpp drvB.cpp drvC.cpp

# Libraries needed for testDriver
testDriver_LIBS += asyn
testDriver_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
