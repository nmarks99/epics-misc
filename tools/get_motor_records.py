#!/usr/bin/env python3
from epics import caget
import argparse

# TODO: make args with argparse
#  prefix = "4ida:"
#  motor_list = list(range(1,13+1))


basic_fields = [
    "DESC",
    "EGU",
    "HLM",
    "LLM",
    "RBV",
    "VAL",
    "DHLM",
    "DLLM",
    "DRBV",
    "DVAL",
    "RVAL",
    "RRBV",
    "OFF",
    "FOFF",
    "DIR",
    "VMAX",
    "VELO",
    "VBAS",
    "ACCL",
    "MRES",
    "ERES",
    "RDBD",
    "RTRY",
    "UEIP",
    "URIP",
    "PREC"
]

all_fields = [
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

    parser = argparse.ArgumentParser(description='Get fields of motor records')
    parser.add_argument('prefix', type=str, help='IOC name')
    parser.add_argument('motors', type=str, nargs='+', help='Motor numbers to get')
    parser.add_argument('--basic', action='store_true', help='Optional flag to enable basic mode')
    parser.add_argument('--outfile', type=str, help='Path to an output file')
    args = parser.parse_args()
    
    prefix = args.prefix
    if ":" not in prefix:
        prefix = f"{prefix}:"
   
    motor_list = []
    if len(args.motors) == 1:
        assert "-" in args.motors[0]
        motors_split = args.motors[0].split("-")
        m_start = motors_split[0].strip()
        m_end = motors_split[1].strip()
        motor_list = list(range(int(m_start),int(m_end)+1))
    else:
        motor_list = [int(m) for m in args.motors]

    motors = []
    fields = all_fields
    if args.basic:
        fields = basic_fields
    
    outfile = f"{prefix.replace(':','')}_all_motors.txt"
    outfile = args.outfile if args.outfile else outfile
    
    for i in motor_list:
        pv_name = f"{prefix}m{i}"
        print(f"Getting {pv_name} ...")

        _motor = dict()
        _motor["PV_NAME"] = pv_name
        for field in fields:
            print(f"{field}")
            val = caget(f"{pv_name}.{field}")
            _motor[field] = val
        motors.append(_motor)

    # save to text files
    with open(outfile, "w") as file:
        for motor in motors:
            pv_name = motor["PV_NAME"]
            for k, v in motor.items():
                if k != "PV_NAME":
                    file.write(f"{pv_name}.{k} {v}\n")
            file.write("\n")

    print(f"Motor record fields saved to {outfile}")
if __name__ == "__main__":
    main()

