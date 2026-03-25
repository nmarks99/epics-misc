# ../../bin/${EPICS_HOST_ARCH}/testIOC st.cmd
< envPaths

dbLoadDatabase("../../dbd/ioctestIOCLinux.dbd")
ioctestIOCLinux_registerRecordDeviceDriver(pdbbase)

epicsEnvSet("IOCSH_PS1", "$(IOC)>")
epicsEnvSet("PREFIX", "testIOC:")

DriverAConfig("DRVA")
dbLoadRecords("$(TEST_DRIVER)/db/drv.db", "P=$(PREFIX),R=A,PORT=DRVA")

DriverBConfig("DRVB")
dbLoadRecords("$(TEST_DRIVER)/db/drv.db", "P=$(PREFIX),R=B,PORT=DRVB")

DriverCConfig("DRVC", "DRVA", "DRVB")
dbLoadRecords("$(TEST_DRIVER)/db/drv.db", "P=$(PREFIX),R=C,PORT=DRVC")

###############################################################################
iocInit
###############################################################################

# print the time our boot was finished
date
