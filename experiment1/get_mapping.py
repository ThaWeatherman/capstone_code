'''
gets a mapping of unique domain names to integers
run this after runnning clean.py
'''
import argparse
import json
import sys

import pandas as pd


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='The input CSV')
    return parser.parse_args()


def main():
    y = input('Have you already run clean.py on the CSV? [y/n]> ')
    if y.lower() != 'y':
        print('Please first run clean.py on the data')
        sys.exit(1)
    args = get_args()
    df = pd.read_csv(args.f, encoding = "ISO-8859-1")
    name_unique = list(df['NAME'].unique())
    mapping = {name: i for name, i in zip(name_unique, range(len(name_unique)))}
    with open('mapping.json', 'w') as f:
        json.dump(mapping, f)


if __name__ == '__main__':
    main()

