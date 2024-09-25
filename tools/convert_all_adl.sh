#!/usr/bin/env bash

export CAQTDM_DISPLAY_PATH=$CAQTDM_DISPLAY_PATH:/home/beams/NMARKS/Public/caqtdm

ADL2UI="/APSshare/bin/adl2ui"
output_dir=""

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -o)
      output_dir="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$output_dir" ]]; then
  echo "Error: Please specifiy output directory"
  echo "Usage: $0 -o <output_dir>"
  exit 1
fi

# convert all adl files (not the _BAK.adl files)
for file in *.adl; do
  if [[ -f "$file" && ! "$file" == *_BAK.adl ]]; then
    $ADL2UI "$file"
  fi
done

# move all converted ui files to output_dir
for file in *.ui; do
  if [ -f "$file" ]; then
    mv "$file" "${output_dir}"
  fi
done

# copy all .gif files to output_dir too
for file in *.gif; do
  if [ -f "$file" ]; then
    cp "$file" "${output_dir}"
  fi
done

printf "Converted .ui files can be found in ${output_dir}"
