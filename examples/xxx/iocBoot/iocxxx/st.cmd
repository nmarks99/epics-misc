# ../../bin/${EPICS_HOST_ARCH}/xxx st.cmd
< envPaths

< settings.iocsh

dbLoadDatabase("../../dbd/iocxxxLinux.dbd")
iocxxxLinux_registerRecordDeviceDriver(pdbbase)

# Load examples
< examples/luascript/lua_example.cmd
< examples/asynPortDriver/simple_apd.cmd

###############################################################################
iocInit
###############################################################################

# print the time our boot was finished
date
