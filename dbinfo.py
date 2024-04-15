#!/usr/bin/env python3

from dataclasses import dataclass
import sys

@dataclass
class Record:
    type: str = None
    name: str = None
    fields: dict = None

    def get_name_short(self):
        name_out =  self.name.replace("$(P)", "")
        name_out =  name_out.replace("$(R)", "")
        return name_out

class EPICSDatabase:
    def __init__(self, path):
        self.database = []

        lines = []
        with open(path, "r") as f:
            lines = f.readlines()

        for line in lines:
            if "record" in line:
                #  indl = line.find("(")
                line = line.replace('"','').replace("'", "")
                rec_list = line[line.find("(")+1:-2].strip().split(",")
                rec = Record(type=rec_list[0], name=rec_list[1])
                self.database.append(rec)

    def show(self, hide_prefix=False):
        for record in self.database:
            if hide_prefix:
                print(f"{record.type}\t{record.get_name_short()}")
            else:
                print(f"{record.type}\t{record.name}")



if __name__ == "__main__":
    assert(len(sys.argv) == 2)
    path = sys.argv[1]
    db = EPICSDatabase(path)
    db.show(hide_prefix=True)

