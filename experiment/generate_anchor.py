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
df['QNAME'] = df['url'].map(lambda x: mapping[x])
names = list(df['QNAME'])
dfs = [df2[df2['QNAME'] == name] for name in names]

anchor = dfs[0]
for d in dfs[1:]:
    anchor = anchor.append(d, ignore_index=True)
final_anchor = anchor.groupby('QNAME').first().reset_index()
final_anchor = final_anchor[df2.columns]
final_anchor.to_csv('anchor.csv', index=False)
