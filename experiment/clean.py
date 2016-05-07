'''
Cleans an input csv to look how it needs to for analysis, except for feature extraction
usage: clean.py input.csv output.csv
'''
import sys

import pandas as pd


if not len(sys.argv) == 3:
    print('usage: clean.py input.csv output.csv')
    sys.exit(1)
reader = pd.read_csv(sys.argv[1], encoding = "ISO-8859-1", chunksize=100)
headers_written = False
for df in reader:
    df.dropna(inplace=True)
    del df['QNAME']
    del df['RDATA']
    del df['QR']
    df.rename(columns={'RRNAME': 'NAME'}, inplace=True)
    if not headers_written:
        with open(sys.argv[2], 'w') as f:
            df.to_csv(f, index=False)
            headers_written = True
    else:
        with open(sys.argv[2], 'a') as f:
            df.to_csv(f, header=False, index=False)

