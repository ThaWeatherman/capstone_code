'''
python generate_anchor.py dataset.csv
'''
import json
import sys

import pandas as pd


if len(sys.argv) != 2:
    print('usage: generate_anchor.py dataset.csv')
    sys.exit(1)

with open('mapping.json') as f:
    mapping = json.load(f)
df = pd.read_csv('anchor_start.csv')
df2 = pd.read_csv(sys.argv[1], encoding = "ISO-8859-1")
df['NAME'] = df['url'].map(lambda x: mapping[x])
names = list(df['NAME'])
dfs = [df2[df2['NAME'] == name] for name in names]

anchor = dfs[0]
for d in dfs[1:]:
    anchor = anchor.append(d, ignore_index=True)
final_anchor = anchor.groupby('NAME').first().reset_index()
final_anchor.to_csv('anchor.csv', index=False)
