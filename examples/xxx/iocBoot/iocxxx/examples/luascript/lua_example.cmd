# Append luascript directory to lua script search path
epicsEnvSet("LUA_SCRIPT_PATH", "$(LUA_SCRIPT_PATH):examples/luascript")

# load database
dbLoadRecords("examples/luascript/lua_example.db", "P=$(PREFIX)")
