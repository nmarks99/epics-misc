#!/usr/bin/env python3
import argparse

def subs_row_to_list(row):
    return row.replace(" ", "").replace("}","").replace("{","").strip().split(",")

# TODO: only works for subtitutions files with a single db file
def main():
    
    parser = argparse.ArgumentParser(description='Nicely format a substitutions file')
    parser.add_argument('filename', type=str, help='Substitutions file to format')
    args = parser.parse_args()
    
    with open(args.filename, "r") as f:
        file_str = f.read()
    
    all_lines = file_str.split("\n")
    ind_header = next(i+1 for i,s in enumerate(all_lines) if "pattern" in s)
    if (ind_header == 0):
        raise RuntimeError('"pattern" not found in substitutions file')
    
    mat = []
    for row in all_lines[ind_header:]:
        row_list = subs_row_to_list(row)
        if len(row_list) > 1:
            mat.append(row_list)
    
    # get the longest string in each column
    mat = list(map(list, zip(*mat))) # transpose
    longest = [max(len(x) for x in col) for col in mat]
    mat = list(map(list, zip(*mat))) # transpose again
    
    # add the appropriate whitespace to each element of each row
    new_mat = []
    for row in mat:
        new_row = []
        for i in range(len(row)):
            spaces = " " * (longest[i] - len(row[i]))
            new_row.append(f"{spaces}{row[i]}")
        new_mat.append(new_row)
   
    # generate the fully formatted file
    out = []
    for line in all_lines[:ind_header]:
        out.append(line)
    for row in new_mat:
        row_str = "{"
        for i,v in enumerate(row):
            if i == len(row) - 1:
                row_str = f"{row_str}{v}"
            else:
                row_str = f"{row_str}{v},  "
        row_str = f"{row_str}}}"
        out.append(row_str)
    out.append("}")
    
    # Print the formatted file contents
    for row in out:
        print(row)

if __name__ == "__main__":
    main()
