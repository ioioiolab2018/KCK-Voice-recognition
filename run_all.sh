#!/usr/bin/env bash
folder="train"
if [[ $# -gt 1 ]]; then
    filename=$1
    folder=$2
elif [[ $# -gt 0 ]]; then
    filename=$1
else
    printf "Script require:\n\t* filename or parameter 'all'\n"
    exit
fi

echo "Script is started"
if [[ -f result.txt ]]; then
    exec rm -r result.txt &
fi

if [[ ${filename} == "all" ]]; then
    for file in ${folder}/*; do
        exec python3 HPS.py ${file} | printf "%s %s%s\n" "$file -> " "$(cat -)" "/${file:10:1}" >> result.txt &
    done
else
    exec python3 HPS.py ${folder}/${filename} | printf "%s %s%s\n" "$filename -> " "$(cat -)" "/${filename:4:1}" >> result.txt &
fi

echo "$filename"