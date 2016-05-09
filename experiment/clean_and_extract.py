'''
clean_and_extract.py input.csv output.csv <number of lines in input.csv>

Specify the number of lines to have a pretty progress bar. Note that it might not be
exactly accurate: pandas knows how to read in the RDATA column properly, but in the CSV that column
sometimes has \n in it. That throws off the line count from `wc -l`.
'''
import json
import math
import sys

import pandas as pd
from tqdm import tqdm


def shannon_entropy(s):
    if isinstance(s, float):
        return 0.0
    """computes the shannon entropy of a given string `s`.returns a float"""
    prob = [float(s.count(c)/len(s)) for c in s]
    entropy = -1 * sum([p*math.log(p)/math.log(2) for p in prob])
    return round(entropy, 2)


if not len(sys.argv) >= 3:
    print('usage: clean_and_extract.py input.csv output.csv <number of lines in input.csv>')
    sys.exit(1)
n = 0
chunksize = 100
if len(sys.argv) >= 4:
    n = int(sys.argv[3])
reader = pd.read_csv(sys.argv[1], encoding = "ISO-8859-1", chunksize=chunksize)
if n:
    # if we know the number of rows, we can make a nice progress bar
    reader = tqdm(reader, total=math.ceil(n/chunksize))
mapping = {}
count = 1
headers_written = False
for df in reader:
    df.fillna(value=0.0, inplace=True)
    del df['RRNAME']
    # add to the global mapping of domain names to integers
    # names = set(df['QNAME'].unique()) | set(df['RRNAME'].unique())
    df['QNAME'] = df['QNAME'].map(lambda x: x.lower() if isinstance(x, str) else x)
    names = df['QNAME'].unique()
    for name in names:
        if name not in mapping:
            mapping[name] = count
            count += 1
    # now make a shannon entropy column
    df['NAME_ENTROPY'] = df['QNAME'].map(shannon_entropy)
    df['DATA_ENTROPY'] = df['RDATA'].map(shannon_entropy)
    del df['RDATA']
    # now map names to ints
    df['QNAME'] = df['QNAME'].map(lambda x: mapping[x])
    # write out the chunk
    if not headers_written:
        with open(sys.argv[2], 'w') as f:
            df.to_csv(f, index=False)
            headers_written = True
    else:
        with open(sys.argv[2], 'a') as f:
            df.to_csv(f, header=False, index=False)
# finally, write out the mapping so we have it for later
with open('mapping.json', 'w') as f:
    json.dump(mapping, f)

