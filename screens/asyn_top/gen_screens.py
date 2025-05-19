#!/usr/bin/env python3
import os
import sys
from adl_templates import adl_header, adl_row8, adl_row16, WINDOW_WIDTH8, WINDOW_WIDTH16

SCREEN_TYPE = 16

# moxa4ida
#  R_list = [
    #  "asyn_MOXA_A:1",
    #  "asyn_MOXA_A:2",
    #  "asyn_MOXA_A:3",
    #  "asyn_MOXA_A:4",
    #  "asyn_MOXA_A:5",
    #  "asyn_MOXA_A:6",
    #  "asyn_MOXA_A:7",
    #  "asyn_MOXA_A:8",
    #  "asyn_MOXA_A:9",
    #  "asyn_MOXA_A:10",
    #  "asyn_MOXA_A:11",
    #  "asyn_MOXA_A:12",
    #  "asyn_MOXA_A:13",
    #  "asyn_MOXA_A:14",
    #  "asyn_MOXA_A:15",
    #  "asyn_MOXA_A:16",
#  ]

# moxa4idvac3
#  R_list = [
    #  "asyn_MOXA_VAC3:1",
    #  "asyn_MOXA_VAC3:2",
    #  "asyn_MOXA_VAC3:3",
    #  "asyn_MOXA_VAC3:4",
    #  "asyn_MOXA_VAC3:5",
    #  "asyn_MOXA_VAC3:6",
    #  "asyn_MOXA_VAC3:7",
    #  "asyn_MOXA_VAC3:8",
    #  "asyn_MOXA_VAC3:9",
    #  "asyn_MOXA_VAC3:10",
    #  "asyn_MOXA_VAC3:11",
    #  "asyn_MOXA_VAC3:12",
    #  "asyn_MOXA_VAC3:13",
    #  "asyn_MOXA_VAC3:14",
    #  "asyn_MOXA_VAC3:15",
    #  "asyn_MOXA_VAC3:16",
#  ]

#  # moxa4idb
#  R_list = [
    #  "asyn_MOXA_B:1",
    #  "asyn_MOXA_B:2",
    #  "asyn_MOXA_B:3",
    #  "asyn_MOXA_B:4",
    #  "asyn_MOXA_B:5",
    #  "asyn_MOXA_B:6",
    #  "asyn_MOXA_B:7",
    #  "asyn_MOXA_B:8",
    #  "asyn_MOXA_B:9",
    #  "asyn_MOXA_B:10",
    #  "asyn_MOXA_B:11",
    #  "asyn_MOXA_B:12",
    #  "asyn_MOXA_B:13",
    #  "asyn_MOXA_B:14",
    #  "asyn_MOXA_B:15",
    #  "asyn_MOXA_B:16",
#  ]

#  # moxa4idh
#  R_list = [
    #  "asyn_MOXA_H:1",
    #  "asyn_MOXA_H:2",
    #  "asyn_MOXA_H:3",
    #  "asyn_MOXA_H:4",
    #  "asyn_MOXA_H:5",
    #  "asyn_MOXA_H:6",
    #  "asyn_MOXA_H:7",
    #  "asyn_MOXA_H:8",
    #  "asyn_MOXA_H:9",
    #  "asyn_MOXA_H:10",
    #  "asyn_MOXA_H:11",
    #  "asyn_MOXA_H:12",
    #  "asyn_MOXA_H:13",
    #  "asyn_MOXA_H:14",
    #  "asyn_MOXA_H:15",
    #  "asyn_MOXA_H:16",
#  ]

#  # moxa7idd
#  R_list = [
    #  "asyn_MOXA_D:1",
    #  "asyn_MOXA_D:2",
    #  "asyn_MOXA_D:3",
    #  "asyn_MOXA_D:4",
    #  "asyn_MOXA_D:5",
    #  "asyn_MOXA_D:6",
    #  "asyn_MOXA_D:7",
    #  "asyn_MOXA_D:8",
    #  "asyn_MOXA_D:9",
    #  "asyn_MOXA_D:10",
    #  "asyn_MOXA_D:11",
    #  "asyn_MOXA_D:12",
    #  "asyn_MOXA_D:13",
    #  "asyn_MOXA_D:14",
    #  "asyn_MOXA_D:15",
    #  "asyn_MOXA_D:16",
#  ]
# ----------------------------------------

Y = 5
Y_OFFSET = 30
adl_out = adl_header
assert SCREEN_TYPE in [8, 16]

if SCREEN_TYPE == 8:
    filename = "topAsyn8x.adl"
    assert len(R_list) in [0, 8]
    for n in range(1,9):
        adl_out += adl_row8.replace("$(Y)", str(Y)).replace("$(N)", str(n))
        Y += Y_OFFSET
    if len(R_list):
        print("Using R list")
        for n in range(1,9):
            adl_out = adl_out.replace(f"$(R{n})", R_list[n-1])
    adl_out = adl_out.replace("$(WINDOW_WIDTH)", str(WINDOW_WIDTH8))

elif SCREEN_TYPE == 16:
    filename = "topAsyn16x.adl"
    assert len(R_list) in [0, 16]
    for n in range(1,9):
        adl_out += adl_row16.replace("$(Y)", str(Y)).replace("$(N1)", str(n)).replace("$(N2)", str(n+8))
        Y += Y_OFFSET
    if len(R_list):
        print("Using R list")
        for n in range(1,17):
            adl_out = adl_out.replace(f"$(R{n})", R_list[n-1])
    adl_out = adl_out.replace("$(WINDOW_WIDTH)", str(WINDOW_WIDTH16))

# set the window height and filename
adl_out = adl_out.replace("$(WINDOW_HEIGHT)", str(Y + 5))
adl_out = adl_out.replace("$(FILENAME)", filename)

# write contents to file
with open(filename, "w") as f:
    f.write(adl_out)

# convert to ui
os.system(f"/APSshare/bin/adl2ui {filename}")
