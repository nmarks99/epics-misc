#!/usr/bin/env bash

export LD_LIBRARY_PATH="/home/nick/.local/epics/pvxs/lib/linux-x86_64:/home/nick/.local/epics/base/lib/linux-x86_64:${LD_LIBRARY_PATH}"

LUA_CPATH="./?.so;;" ./lua-5.4.9/src/lua example.lua
