#!/bin/bash

echo Clean and extract the data
python clean_and_extract.py dns.csv dns_final.csv
echo Generate the anchor file
python generate_anchor.py dns_final.csv
./learn.sh
