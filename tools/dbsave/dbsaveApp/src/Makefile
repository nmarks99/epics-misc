# NOTE: paths relative to where they get installed (e.g. ./O.rhel9-x86_64)

TOP=../..

include $(TOP)/configure/CONFIG

# C++17 is needed for things like std::optional and structured bindings
USR_CXXFLAGS += -std=c++17

# Define IOC library name
LIBRARY_IOC += dbsave

# install dbsaveSupport.dbd into <top>/dbd
DBD += dbsaveSupport.dbd
dbsaveSupport_DBD += dbsave.dbd

# source files to be compiled and added to the library
dbsave_SRCS += dbsave.cpp

# Libraries needed for dbsave
dbsave_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
