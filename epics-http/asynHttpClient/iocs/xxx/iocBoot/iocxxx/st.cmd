# ../../bin/${EPICS_HOST_ARCH}/xxx st.cmd
< envPaths

dbLoadDatabase("../../dbd/iocxxxLinux.dbd")
iocxxxLinux_registerRecordDeviceDriver(pdbbase)

epicsEnvSet("IOCSH_PS1", "$(IOC)>")
epicsEnvSet("PREFIX", "xxx:")

AsynHttpClientConfig("client1", "asdf")
dbLoadRecords("test.db","P=$(PREFIX),PORT=client1")

###############################################################################
iocInit
###############################################################################

dbpf "xxx:BaseURL.VAL" "http://localhost:3030"
dbpf "xxx:Endpoint.VAL" "/action?action_name=getj&args=%7B%7D"

# print the time our boot was finished
date
