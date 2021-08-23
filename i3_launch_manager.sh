#!/bin/bash

input=$HOME"/config_files/i3_manager/bash_commands.txt"

while IFS= read -r line
do
	eval "$line"
done < "$input"


