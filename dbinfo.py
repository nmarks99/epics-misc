#!/usr/bin/env python3

'''
dbinfo.py

Easily get information about an EPICS database.
Can be used as a command line tool or imported as a library.

Example: 
Load a database and iterate through the records it defines
```
from dbinfo import EPICSDatabase
db = EPICSDatabase("my_database.db")
for record in db:
    print(record.type, record.name)
    for field, value in record.fields.items():
        print(field, value)
```

'''

# TODO:
# - handle inline comments
# - test with random databases on APSshare

from dataclasses import dataclass
from dataclasses import field as dataclass_field
import argparse

COMMENT_CHAR = "#"

@dataclass
class Record:
    type: str = ""
    name: str = ""
    fields: dict = dataclass_field(default_factory=dict)

    def show(self, prefix=True):
        if prefix:
            print(f"[{self.type}] {self.name}") 
        else:
            name_out =  self.name.replace("$(P)", "").replace("$(R)", "")
            print(f"[{self.type}] {name_out}") 
        

class EPICSDatabase:
    def __init__(self, path):
        self.database = []

        with open(path, "r") as f:
            contents = f.read()
        
        # sometimes grecord is used, replace with record for splitting
        contents = contents.replace("grecord(", "record(")

        # get rid of anything before the first record
        contents = contents[contents.find("record("):]
    
        # split by 'record(' then add back the '('
        # the outer open/close parenthesis are used to find the
        # record type and name and must not affect the prefixes
        rec_list_raw = contents.split("record(")
        rec_list_fix = []
        for rec in rec_list_raw:
            if len(rec) > 0:
                rec_list_fix.append("".join(["(",rec]))
            
        for rec_str in rec_list_fix:
            # split each record string by lines and create a Record object
            lines = rec_str.splitlines()
            record = Record()
            for ln in lines:
                # get rid of brackets and comments on each line
                line = ln.replace("{", "").replace("}","").strip()
                if line.startswith(COMMENT_CHAR):
                    continue
                if COMMENT_CHAR in line:
                    line = line[0:line.find(COMMENT_CHAR)]
                if len(line) > 0:
                    if "field" in line:
                        # fill in the fields dictionary
                        field_split = line[line.find("(")+1:line.rfind(")")].strip().split(",")
                        field_val = ",".join(field_split[1:])
                        field_val = field_val.strip()
                        field_name = field_split[0]
                        record.fields.update({str(field_name) : field_val})

                    else:
                        # record definition line (record tpye and name)
                        line = line.replace('"','').replace("'", "")
                        rec_split = line[line.find("(")+1:line.rfind(")")].strip().split(",")
                        record.type=rec_split[0].strip()
                        record.name=rec_split[1].strip()

            if len(record.name) > 0:
                self.database.append(record)
    
    def __iter__(self):
        return iter(self.database)

    def show_all(self,prefix=True, fields=False):
        for record in self.database:
            if prefix:
                record.show()
            else:
                record.show(prefix=prefix)
            if fields:
                for k,v in record.fields.items():
                    print(f"{k} = {v}")
                print("\n")

    def find(self, name: str) -> Record:
        record_out = None
        for r in self.database:
            if r.name == name or r.name.replace("$(P)","").replace("$(R)", "") == name:
                record_out = r
        return record_out


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
        db.show_all()
