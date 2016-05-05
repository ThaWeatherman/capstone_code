import argparse
import pickle

import pandas as pd


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='The input CSV')
    return parser.parse_args()


def main():
    args = get_args()
    df = pd.read_csv(args.f, encoding = "ISO-8859-1")
    qname_unique = df['QNAME'].dropna().unique()
    rrname_unique = df['RRNAME'].dropna().unique()
    all_names = set(qname_unique) | set(rrname_unique)
    mapping = {name: i for name, i in zip(all_names, range(len(all_names)))}
    with open('mapping.pickle', 'wb') as f:
        pickle.dump(mapping, f)


if __name__ == '__main__':
    main()

