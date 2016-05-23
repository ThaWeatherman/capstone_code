import collections
import itertools
import json
import os
import pprint
import sys

import numpy as np
import pandas as pd
from sklearn.cluster import MeanShift, estimate_bandwidth, AffinityPropagation, KMeans


if len(sys.argv) != 3:
    print('usage: learn.py <control> <input.csv>')
    sys.exit(1)


dataset = sys.argv[2]  # dns_final.csv
anchor_file = 'anchor.csv'
map_file = 'mapping.json'
reports = 'virustotal/data/reports/'
anomalies = open('anomalies.txt', 'w')
base_chunk_size = 48
base_seed_size = 2
control = int(sys.argv[1])
chunk_size = base_chunk_size * control
seeds = base_seed_size * control


def generate_random_sample():
    anchor_sample = np.random.choice(anchor.index.values, seeds)
    anchor_sample_df = anchor.ix[anchor_sample]
    return anchor_sample_df


def get_report(name):
    n = os.path.join(reports, name) + '.json'
    try:
        with open(n) as f:
            r = json.load(f)
        return r['positives']
    except:
        return -1


def get_clustered(labels, seed, df):
    indexes = np.where((labels[:-1*seeds] == seed))
    bad = df.iloc[indexes]
    # pos = len(df[df['SCORE'] > 0])
    anomalies.write('\n'.join(bad['DNAME'].unique()))


reader = pd.read_csv(dataset, chunksize=chunk_size)
anchor = pd.read_csv(anchor_file)
with open(map_file) as f:
    mapping = json.load(f)
    rev_mapping = {y: x for x, y in mapping.items()}


num_clusts = collections.defaultdict(int)


for df in reader:
    ar = np.array(df)
    anch = generate_random_sample()
    ar = np.concatenate((ar, np.array(anch)), axis=0)

    bandwidth = estimate_bandwidth(ar, quantile=0.5)
    alg = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    # alg = AffinityPropagation()
    # alg = KMeans(n_clusters=2)
    alg.fit(ar)
    # matches with row numbers in the nparray
    labels = alg.labels_
    # each nparray matches up with the df columns
    # cluster_centers = alg.cluster_centers_
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    num_clusts[n_clusters_] += 1
    df['DNAME'] = df['QNAME'].map(lambda x: rev_mapping[x])
    # df['SCORE'] = df['DNAME'].map(get_report)
    seen = set()
    for seed in labels[-1*seeds:]:
        if seed in seen:
            continue
        get_clustered(labels, seed, df)
        seen.add(seed)

anomalies.close()
print('---------------------')
pprint.pprint(num_clusts)
print('---------------------')
