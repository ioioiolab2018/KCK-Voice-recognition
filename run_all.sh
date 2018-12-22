#!/usr/bin/env bash
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
exec python3 HPS.py 012_K.wav
echo "$filename"