#!/usr/bin/env python3
from dbutils import EPICSDatabase
import argparse

def main():
    parser = argparse.ArgumentParser(description='Nicely format a substitutions file')
    parser.add_argument('infile', type=str, help='Input file name')
    parser.add_argument('outfile', type=str, help='Output file name')
    parser.add_argument('-n','--no-ask', action='store_true', help='No custom input')
    args = parser.parse_args()

    db = EPICSDatabase(args.infile)
    outfile = args.outfile

    with open(outfile, "w+") as f:
        f.write("| Record  | Type   | Description   |\n")
        f.write("|-------------- | -------------- | -------------- |\n")

        for record in db.database:
            desc = record.fields.get("DESC","").replace('"', '')
            name = record.name.replace('$(P)', '')
            print(f"{name}\t{desc}")
            if not args.no_ask:
                yn0 = input(f"Input desciption ({desc}): ")
                if len(yn0) > 0:
                    desc = yn0
            print(f"| {name}    | {record.type}     | {desc}     |\n")
            f.write(f"| {name}    | {record.type}     | {desc}     |\n")

if __name__ == "__main__":
    main()
