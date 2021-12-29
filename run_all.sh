#!/bin/bash
for file in src/Python/day*.py
do
    echo ${file}
    time python3 ./${file}
    printf "\n"
done