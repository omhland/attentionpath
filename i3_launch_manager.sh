#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Find name of current directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ) 

python3 $SCRIPT_DIR/python_src/config_reader.py
sleep 0.5

input=$SCRIPT_DIR/python_src/bash_output/output_text.txt

while IFS= read -r line
do
	eval "$line"
done < "$input"
