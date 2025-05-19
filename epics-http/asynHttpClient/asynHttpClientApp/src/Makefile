# NOTE: paths relative to where they get installed (e.g. ./O.rhel9-x86_64)

TOP=../..

include $(TOP)/configure/CONFIG

# Define IOC library name
LIBRARY_IOC += asynHttpClient

# NOTE: cpr must be compiled with CMAKE_POSITION_INDEPENDENT_CODE ON
# TODO: no absolute paths here
USR_INCLUDES += -I/home/nick/.local/include
LIB_INSTALLS += /home/nick/.local/lib/libcpr.a
BIN_INSTALLS += /home/nick/.local/lib/libcpr.so
BIN_INSTALLS += /home/nick/.local/lib/libcpr.so.1
BIN_INSTALLS += /home/nick/.local/lib/libcpr.so.1.11.2

# install asynHttpClientSupport.dbd into <top>/dbd
DBD += asynHttpClientSupport.dbd
asynHttpClientSupport_DBD += asynHttpClient.dbd

# source files to be compiled and added to the library
asynHttpClient_SRCS += asynHttpClient.cpp

# Libraries needed for asynHttpClient
asynHttpClient_LIBS += asyn cpr
asynHttpClient_SYS_LIBS += curl
asynHttpClient_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
