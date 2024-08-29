#!/usr/bin/env python3
from epics import caget

# TODO: make args with argparse
prefix = "4ida:"
motor_list = list(range(1,13+1))

fields = [
    "DESC",
    "SCAN",
    "DTYP",
    "ACCL",
    "ADEL",
    "ALST",
    "ATHM",
    "BACC",
    "BDST",
    "BVEL",
    "CARD",
    "CDIR",
    "CNEN",
    "DCOF",
    "DHLM",
    "DIFF",
    "DINP",
    "DIR",
    "DLLM",
    "DLY",
    "DMOV",
    "DOL",
    "DRBV",
    "DVAL",
    "EGU",
    "ERES",
    "FOF",
    "FOFF",
    "FRAC",
    "HHSV",
    "HIGH",
    "HIHI",
    "HLM",
    "HLS",
    "HLSV",
    "HOMF",
    "HOMR",
    "HOPR",
    "HSV",
    "HVEL",
    "ICOF",
    "INIT",
    "JAR",
    "JOGF",
    "JOGR",
    "JVEL",
    "LDVL",
    "LLM",
    "LLS",
    "LLSV",
    "LOCK",
    "LOLO",
    "LOPR",
    "LOW",
    "LRLV",
    "LRVL",
    "LSPG",
    "LSV",
    "LVAL",
    "LVIO",
    "MDEL",
    "MLST",
    "MIP",
    "MISS",
    "MMAP",
    "MOVN",
    "MRES",
    "MSTA",
    "NMAP",
    "NTM",
    "NTMF",
    "OFF",
    "OMSL",
    "OUT",
    "PCOF",
    "POST",
    "PP",
    "PREC",
    "PREM",
    "RBV",
    "RCNT",
    "RDBD",
    "SPDB",
    "RDBL",
    "RDIF",
    "REP",
    "RHLS",
    "RINP",
    "RLLS",
    "RLNK",
    "RLV",
    "RMOD",
    "RMP",
    "RRBV",
    "RRES",
    "RTRY",
    "RVAL",
    "RVEL",
    "SBAK",
    "SBAS",
    "SET",
    "SMAX",
    "SPMG",
    "SREV",
    "SSET",
    "STOO",
    "STOP",
    "STUP",
    "SUSE",
    "SYNC",
    "TDIR",
    "TWF",
    "TWR",
    "TWV",
    "UEIP",
    "UREV",
    "URIP",
    "VAL",
    "VBAS",
    "VELO",
    "VERS",
    "VMAX",
    "VOF",
]

def main():

    motors = []
    
    for i in motor_list:
        pv_name = f"{prefix}m{i}"
        print(f"Getting {pv_name} ...")

        _motor = dict()
        _motor["PV_NAME"] = pv_name
        for field in fields:
            val = caget(f"{pv_name}.{field}")
            _motor[field] = val
        motors.append(_motor)

    # save to text files
    with open(f"{prefix.replace(':','')}_all_motors.txt", "w") as file:
        for motor in motors:
            pv_name = motor["PV_NAME"]
            for k, v in motor.items():
                if k != "PV_NAME":
                    file.write(f"{pv_name}.{k} {v}\n")

if __name__ == "__main__":
    main()

