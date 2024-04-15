#!/usr/bin/env python3

# TODO:
# - use argparse
# - handle comments
# - test with random databases on APSshare

from dataclasses import dataclass
from dataclasses import field as dataclass_field
import sys

@dataclass
class Record:
    type: str = ""
    name: str = ""
    fields: dict = dataclass_field(default_factory=dict)

    def show(self, prefix=True):
        if prefix:
            print(f"[{self.type}] {self.name}") 
        else:
            name_out =  self.name.replace("$(P)$(R)", "")
            print(f"[{self.type}] {name_out}") 
        

class EPICSDatabase:
    def __init__(self, path):
        self.database = []

        with open(path, "r") as f:
            contents = f.read()

        rec_list_raw = contents.split("record")
        for rec_txt in rec_list_raw:
            lines = rec_txt.split("\n")
            record = Record()
            for ln in lines:
                line = ln.replace("{", "").replace("}","").strip()
                if line.startswith("#"):
                    continue
                if len(line) > 0:
                    if "field" in line:
                        field_split = line[line.find("(")+1:line.rfind(")")].strip().split(",")
                        field_val = ",".join(field_split[1:])
                        field_val = field_val.strip()
                        field_name = field_split[0]
                        record.fields.update({str(field_name) : field_val})

                    else: # record definition line
                        line = line.replace('"','').replace("'", "")
                        rec_split = line[line.find("(")+1:line.rfind(")")].strip().split(",")
                        record.type=rec_split[0].strip()
                        record.name=rec_split[1].strip()

            if len(record.name) > 0:
                self.database.append(record)
    

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
            if r.name == name or r.name.replace("$(P)$(R)","") == name:
                record_out = r
        return record_out


if __name__ == "__main__":
    assert len(sys.argv) > 1 and len(sys.argv) <= 3, "invalid input"
    path = sys.argv[1]
    db = EPICSDatabase(path)
    
    if len(sys.argv) == 2:
        db.show_all()
    
    elif len(sys.argv) == 3:
        record_in = sys.argv[2]
        r = db.find(record_in)
        if r is not None:
            print(f"[{r.type}] {r.name}")
            for k, v in r.fields.items():
                print(f"{k} = {v}")
        else:
            print(f"Record {record_in} not found")
