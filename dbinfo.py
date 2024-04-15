#!/usr/bin/env python3

from dataclasses import dataclass
from dataclasses import field as dataclass_field
import sys

@dataclass
class Record:
    type: str = ""
    name: str = ""
    fields: dict = dataclass_field(default_factory=dict)

    def get_name_short(self):
        name_out =  self.name.replace("$(P)", "")
        name_out =  name_out.replace("$(R)", "")
        return name_out

#  class EPICSDatabase:
    #  def __init__(self, path):
        #  self.database = []
#
        #  lines = []
        #  with open(path, "r") as f:
            #  lines = f.readlines()
#
        #  for line in lines:
            #  if "record" in line:
                #  line = line.replace('"','').replace("'", "")
                #  rec_list = line[line.find("(")+1:-2].strip().split(",")
                #  rec = Record(type=rec_list[0], name=rec_list[1])
                #  self.database.append(rec)
#
    #  def show(self, hide_prefix=False):
        #  for record in self.database:
            #  if hide_prefix:
                #  print(f"{record.type}\t{record.get_name_short()}")
            #  else:
                #  print(f"{record.type}\t{record.name}")
#
#
#
#  if __name__ == "__main__":
    #  assert(len(sys.argv) == 2)
    #  path = sys.argv[1]
    #  db = EPICSDatabase(path)
    #  db.show(hide_prefix=True)


path = sys.argv[1]
with open(path, "r") as f:
    contents = f.read()


rec_list_raw = contents.split("record")
database = []
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
                tp, name = rec_split[0], rec_split[1]
                record.type=rec_split[0]
                record.name=rec_split[1]

    database.append(record)
    print("\n")

for record in database:
    print(f"{record.type}\t{record.name}")
    for field, value in record.fields.items():
        print(f"{field}:{value}")
    print("\n")

