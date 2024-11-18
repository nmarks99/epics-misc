#!/usr/bin/env python3
import os

from adl_templates import adl_header, content
# Must replace the following macros:
# FILENAME, WINDOW_HEIGHT, M, Y

# define output adl file, ioc prefix, and motors
filename = "cnen_all.adl"

motors = [
    *[f"4idHHLM:m{i}" for i in range(1,6)],
    *[f"4idVDCM:m{i}" for i in range(1,17)],
]

adl_out = adl_header
y = 5
y_offset = 25

for m in motors:
    line = content.replace("$(M)",m).replace("$(Y)",str(y))
    y += y_offset
    adl_out = "".join([adl_out, line])

adl_out = adl_out.replace("$(FILENAME)", filename)
adl_out = adl_out.replace("$(WINDOW_HEIGHT)", str(y+5))

with open(filename, "w") as f:
    f.write(adl_out)

os.system(f"/APSshare/bin/adl2ui {filename}")

