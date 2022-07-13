#!/bin/bash
set -euo pipefail
IFS=$'\n\t'


# FIXME Make a good home variable that makes the script invariant of placement


# Find name of current directory
HOME_DIR=pwd 

python3 python_src/config_reader.py
sleep 0.5

input=python_src/bash_output/output_text.txt

while IFS= read -r line
do
	eval "$line"
done < "$input"
