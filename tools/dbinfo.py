#!/usr/bin/env python3
from dbutils import EPICSDatabase
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Quickly get information from an EPICS database')
    parser.add_argument('path', help='Path to the database file')
    parser.add_argument('record', nargs='?', help='Record name to find and print infomation about')
    args = parser.parse_args()

    db = EPICSDatabase(args.path)

    if args.record is not None:
        r = db.find(args.record)
        if r is not None:
            print(f"[{r.type}] {r.name}")
            for k, v in r.fields.items():
                print(f"{k} = {v}")
        else:
            print(f"Record {args.record} not found")

    else:
        # get the length of the record types so we can align the output
        record_type_max_len = 0
        for record in db:
            length = len(record.type)
            if length > record_type_max_len:
                record_type_max_len = length

        print(f"Number of records: {len(db.database)}")
        for record in db:
            space_to_add = record_type_max_len - len(record.type)
            record_type = "".join([record.type, " "*space_to_add])
            print(f"{record_type}  {record.name}")

            
