import json
import os

import pandas as pd
from tqdm import tqdm


report_dir = 'data/reports/'
reports = [os.path.join(report_dir, f) for f in os.listdir(report_dir)]
all_reps = []
print('Reading reports...')
for report in tqdm(reports):
    with open(report) as f:
        r = json.loads(f.read())
    all_reps.append({'positives': r['positives'], 'url': r['url']})
df = pd.DataFrame(all_reps)
df.sort_values('positives', ascending=False).head(n=20).to_csv('../anchor.csv', index=False)
