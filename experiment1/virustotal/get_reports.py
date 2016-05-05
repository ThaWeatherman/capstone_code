import argparse
import json
import os
import time

import requests
import pandas as pd
from tqdm import tqdm


REPORT_URL = 'http://www.virustotal.com/vtapi/v2/url/report'
REPORT_DATA = {'apikey': '', 'scan': '1', 'resource': ''}
REPORT_OUT_DIR = 'data/reports/'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='Input CSV')
    parser.add_argument('-a', type=str, required=True, help='VT API key')
    return parser.parse_args()


def _chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def sanitize_url(url):
    u = url
    if u.startswith('http://'):
        u = u[7:]
    if u.endswith('/'):
        u = u[:-1]
    return u


def main():
    args = get_args()
    REPORT_DATA['apikey'] = args.a
    df = pd.read_csv(args.f, encoding = "ISO-8859-1")  # assuming py3
    ids = list(df['scanid'])
    chunked = [chunk for chunk in _chunk(ids, 4)]
    failed = []
    for chunk in tqdm(chunked):
        REPORT_DATA['resource'] = '\n'.join(chunk)
        r = requests.post(REPORT_URL, data=REPORT_DATA)
        if r.status_code == 200:
            j = r.json()
            if isinstance(j, list):
                # more than one entry
                for d in j:
                    u = sanitize_url(d['url'])
                    with open(os.path.join(REPORT_OUT_DIR, u+'.json'), 'w') as f:
                        json.dump(d, f)
            else:
                u = sanitize_url(j['url'])
                with open(os.path.join(REPORT_OUT_DIR, u+'.json'), 'w') as f:
                    json.dump(j, f)
        else:
            for sid in chunk:
                failed.append(sid)
        time.sleep(16)
    print('---------')
    print('Complete!')
    print('---------')
    if failed:
        print('Had {} failures...'.format(len(failed)))
        with open('data/failed_retrieval.txt', 'w') as f:
            f.write('\n'.join(failed))


if __name__ == '__main__':
    main()

