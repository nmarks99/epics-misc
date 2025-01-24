#!/usr/bin/env python3
from adl_templates import adl_header, adl_row_pump, adl_row_gauge, WINDOW_WIDTH
import os

PREFIX = "4idaSoft:"
labels = [
    ("IG1/CG1", "VS01"),
    ("IG2/CG2", "VS02"),
    ("IG3/CG3", "VS03"),
    ("IP1","IP01"),
    ("IP2","IP02"),
    ("IP3","IP03"),
    ("IP4","IP04"),
    ("IP5","IP05"),
    ("IP6","IP06"),
    ("IP7","IP07"),
    ("IP8","IP08"),
]

y = 5
y_offset = 20
adl_out = adl_header
filename = "vacTop4ida.adl"

for label,pg in labels:
    if "IP" in label:
        adl_out += adl_row_pump.replace("$(LABEL)", label).replace("$(Y)", str(y))
        adl_out = adl_out.replace("$(PUMP)", pg)
        y += y_offset
    elif "IG" in label:
        adl_out += adl_row_gauge.replace("$(LABEL)", label).replace("$(Y)", str(y))
        adl_out = adl_out.replace("$(GAUGE)", pg)
        y += y_offset

adl_out = adl_out.replace("$(FILENAME)", filename)
adl_out = adl_out.replace("$(WINDOW_HEIGHT)", str(y+5))
adl_out = adl_out.replace("$(WINDOW_WIDTH)", str(WINDOW_WIDTH))
adl_out = adl_out.replace("$(PREFIX)", PREFIX)

with open(filename, "w") as f:
    f.write(adl_out)

os.system(f"/APSshare/bin/adl2ui {filename}")
