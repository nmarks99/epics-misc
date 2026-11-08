LUA_SRC = ./lua-5.4.9/src/
PVXS = /home/nick/.local/epics/pvxs
EPICS_BASE = /home/nick/.local/epics/base

CXXFLAGS = -std=c++17 -fPIC -shared \
           -I. \
           -I$(LUA_SRC) \
           -I./sol2/include \
           -I$(EPICS_BASE)/include \
           -I$(EPICS_BASE)/include/compiler/gcc \
           -I$(EPICS_BASE)/include/os/Linux \
           -I$(PVXS)/include

LDFLAGS = -L$(EPICS_BASE)/lib/linux-x86_64 \
          -L$(PVXS)/lib/linux-x86_64 \
          -L$(LUA_SRC) \
		  -Wl,-rpath,$(EPICS_BASE)/lib/linux-x86_64 \
          -Wl,-rpath,$(PVXS)/lib/linux-x86_64 \

LDLIBS = -llua -ldl -lpvxs -lCom

pvxs_lua.so: pvxs_lua.cpp
	g++ $(CXXFLAGS) $< $(LDFLAGS) $(LDLIBS) -o $@

clean:
	rm pvxs_lua.so
