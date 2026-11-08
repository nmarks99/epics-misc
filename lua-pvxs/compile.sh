#!/usr/bin/env bash

LUA_SRC="./lua-5.4.9/src/"
PVXS="/home/nick/.local/epics/pvxs"
EPICS_BASE="/home/nick/.local/epics/base"

g++ -std=c++17 -fPIC -shared \
    -I. \
    -I${LUA_SRC} \
    -I${EPICS_BASE}/include \
    -I${EPICS_BASE}/include/compiler/gcc \
    -I${EPICS_BASE}/include/os/Linux \
    -I${PVXS}/include \
    -L${EPICS_BASE}/lib/linux-x86_64 \
    -L${PVXS}/lib/linux-x86_64 \
    -L${PVXS}/lib/linux-x86_64 \
    -L${LUA_SRC} \
    ./pvxs_lua.cpp \
    -llua -ldl -lpvxs -lCom \
    -o pvxs_lua.so
