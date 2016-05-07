import argparse
import json
import math
import sys

import pandas as pd


def shannon_entropy(s):
    prob = [float(s.count(c)/len(s)) for c in s]
    entropy = -1 * sum([p*math.log(p)/math.log(2) for p in prob])
    return entropy


def ideal_shannon_entropy(length):
    prob = 1.0 / length
    return -1 * length * prob * math.log(prob) / math.log(2)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='The input CSV')
    parser.add_argument('-o', type=str, required=True, help='The output CSV')
    parser.add_argument('-m', type=str, required=True, help='Mapping file')
    return parser.parse_args()


def main():
    """
    replace urls with ints
    add column for shannon entropy
    drop rows that dont have responses
    """
    y = input('Have you already run get_mapping.py? [y/n]> ')
    if y.lower() != 'y':
        sys.exit(1)
    args = get_args()
    with open(args.m) as f:
        mapping = json.load(f)

    reader = pd.read_csv(args.f, encoding = "ISO-8859-1", chunksize=100)
    headers_written = False
    for df in reader:
        # add the entropy column
        df['ENTROPY'] = df['NAME'].map(shannon_entropy)
        # now map the urls based on the already created mapping
        # using df.replace() eats up gobs of memory for whatever reason
        # df.replace(mapping, inplace=True)
        df['NAME'] = df['NAME'].map(lambda x: mapping[x])
        # write it out
        if not headers_written:
            with open(args.o, 'w') as f:
                df.to_csv(f, index=False)
                headers_written = True
        else:
            with open(args.o, 'a') as f:
                df.to_csv(f, header=False, index=False)


if __name__ == '__main__':
    main()

