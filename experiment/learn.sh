#!/bin/bash

echo Running learning algorithm
python learn.py $1
awk '!x[$0]++' anomalies.txt > anom.txt
echo Checking anomalies for malicious domains
python check_anomalies.py
echo ---------------------------
TOTAL=`wc -l anom.txt | cut -f1 -d' '`
MAL=`wc -l malicious.txt | cut -f1 -d' '`
echo $MAL/$TOTAL
