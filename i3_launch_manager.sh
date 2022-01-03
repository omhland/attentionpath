#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

python3 ~/attentionPath/config_reader.py
sleep 0.5

input=$HOME"/attentionPath/test.txt"

while IFS= read -r line
do
	eval "$line"
done < "$input"
