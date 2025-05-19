# NOTE: paths relative to where they get installed (e.g. ./O.rhel9-x86_64)

TOP=../..

include $(TOP)/configure/CONFIG

# Define IOC library name
LIBRARY_IOC += apd

# install apdSupport.dbd into <top>/dbd
DBD += apdSupport.dbd
apdSupport_DBD += apd.dbd

# source files to be compiled and added to the library
apd_SRCS += apdDriver.cpp

# Libraries needed for apd
apd_LIBS += asyn
apd_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
