#!/usr/bin/env python3

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
            name_out =  self.name.replace("$(P)", "")
            name_out =  name_out.replace("$(R)", "")
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
                line = ln.strip()
                if len(line) > 1:
                    if "field" in line:
                        field_split = line[line.find("(")+1:line.rfind(")")].strip().split(",")
                        field_val = ",".join(field_split[1:])
                        field_val = field_val.strip()
                        field_name = field_split[0]
                        record.fields.update({str(field_name) : field_val})

                    else: # record definition line
                        line = line.replace('"','').replace("'", "")
                        rec_split = line[line.find("(")+1:line.rfind(")")].strip().split(",")
                        record.type=rec_split[0]
                        record.name=rec_split[1]

            if len(record.name) > 0:
                self.database.append(record)
    

    def show_all(self,prefix=False, fields=False):
        for record in self.database:
            if prefix:
                record.show()
            else:
                record.show(prefix=prefix)
            if fields:
                for k,v in record.fields.items():
                    print(f"{k} = {v}")
                print("\n")


if __name__ == "__main__":
    assert len(sys.argv) > 1
    path = sys.argv[1]
    db = EPICSDatabase(path)
    db.show_all()




