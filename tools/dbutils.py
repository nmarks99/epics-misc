#!/usr/bin/env python3

# TODO:
# - sort by record type

from dataclasses import dataclass
from dataclasses import field as dataclass_field
import re

COMMENT_CHAR = "#"

def hide_macros(text):
    return re.sub(r"\$\(.*\)", "", text)

@dataclass
class Record:
    type: str = ""
    name: str = ""
    fields: dict = dataclass_field(default_factory=dict)

    def __str__(self):
       return f"[{self.type}] {self.name}" 


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

    def find(self, name: str) -> Record:
        record_out = None
        for r in self.database:
            if r.name == name or hide_macros(r.name) == name:
                record_out = r
        return record_out
