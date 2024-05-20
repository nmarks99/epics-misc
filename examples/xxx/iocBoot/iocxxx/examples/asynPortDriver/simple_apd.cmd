epicsEnvSet("LUA_SCRIPT_PATH", "$(LUA_SCRIPT_PATH):examples/asynPortDriver")

SimpleApdConfig("apd_port", "device_port_name")
dbLoadRecords("$(SIMPLE_APD)/db/apd.db", "P=$(PREFIX), PORT=apd_port, ADDR=0")

# dbLoadRecords("examples/asynPortDriver/process_chain.db", "P=$(PREFIX), PORT=apd_port, ADDR=0")
dbLoadRecords("examples/asynPortDriver/path_lua.db", "P=$(PREFIX), PORT=apd_port, ADDR=0")
