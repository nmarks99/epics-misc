# ../../bin/${EPICS_HOST_ARCH}/xxx st.cmd
< envPaths

dbLoadDatabase("../../dbd/iocxxxLinux.dbd")
iocxxxLinux_registerRecordDeviceDriver(pdbbase)

epicsEnvSet("IOCSH_PS1", "$(IOC)>")
epicsEnvSet("PREFIX", "xxx:")

AsynHttpClientConfig("client1", "asdf")

# dbLoadRecords("test.db","P=$(PREFIX)")

###############################################################################
iocInit
###############################################################################

# print the time our boot was finished
date
