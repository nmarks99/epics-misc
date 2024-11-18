#!/usr/bin/env python3
import os

# Must replace the following macros:
# FILENAME, WINDOW_HEIGHT, IOC, Y
from adl_templates import adl_header, template_soft, template_vme

ioc_dir = "/net/s4dserv/xorApps/epics/synApps_6_3/ioc"
iocs = {
    f"{ioc_dir}/4ida"             : "vme",
    f"{ioc_dir}/4idaSoft"         : "soft",
    f"{ioc_dir}/4idHHLM"          : "soft",
    f"{ioc_dir}/4idVDCM"          : "soft",
    f"{ioc_dir}/4idaPostMirrBeam" : "soft",
    f"{ioc_dir}/4idaPostMonoBeam" : "soft",

    f"{ioc_dir}/4idbSoft"         : "soft",
    f"{ioc_dir}/4idbPostToroBeam" : "soft",

    f"{ioc_dir}/4idgSoft"         : "soft",

    f"{ioc_dir}/4idhSoft"         : "soft",
}

filename = "IOCManager_4ID.adl"
up_pv = "HEARTBEAT"
adl_out = adl_header
y = 5
y_offset = 35
display_path = ""

for ioc_path, ioc_type in iocs.items():
    ioc_name = ioc_path[ioc_path.rfind("/")+1:]
    display_path = f"{display_path}:{ioc_path}/{ioc_name}App/op/adl:{ioc_path}/{ioc_name}App/op/ui:{ioc_path}/{ioc_name}App/op/ui/autoconvert:"
    print(f"Adding {ioc_name}...")
    if ioc_type == "soft":
        line = template_soft.replace("$(IOC)",ioc_name)
    elif ioc_type == "vme":
        line = template_vme.replace("$(IOC)",ioc_name)
    else:
        raise RuntimeError(f"Invalid ioc type: {ioc_type}")
    line = line.replace("$(Y)", str(y))
    line = line.replace("$(UP_PV)", up_pv)
    adl_out = "".join([adl_out,line])
    y += y_offset


adl_out = adl_out.replace("$(FILENAME)", filename)
adl_out = adl_out.replace("$(WINDOW_HEIGHT)", str(y+5))
with open(filename, "w") as f:
    f.write(adl_out)
print("Done")

with open(f'{filename.replace(".adl","")}_display_path.txt', "w") as f:
    f.write(display_path)


os.system(f"/APSshare/bin/adl2ui {filename}")
