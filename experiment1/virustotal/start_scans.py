import argparse
import time

import requests
from tqdm import tqdm


SCAN_URL = 'https://www.virustotal.com/vtapi/v2/url/scan'
SCAN_DATA = {'apikey': '', 'url': ''}


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='Input text file of URLs')
    parser.add_argument('-o', type=str, required=True, help='Output CSV')
    parser.add_argument('-a', type=str, required=True, help='VT API key')
    return parser.parse_args()


def _chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def main():
    args = get_args()
    SCAN_DATA['apikey'] = args.a
    with open(args.f) as f:
        urls = [url.strip() for url in f.readlines()]
    chunked = [chunk for chunk in _chunk(urls, 4)]
    failed = []
    with open(args.o, 'w') as f:
        f.write('url,scanid\n')
        for chunk in tqdm(chunked):
            SCAN_DATA['url'] = '\n'.join(chunk)
            r = requests.post(SCAN_URL, data=SCAN_DATA)
            if r.status_code == 200:
                j = r.json()
                if isinstance(j, list):
                    for d in j:
                        if d['response_code'] == 1:
                            f.write(d['url']+','+d['scan_id']+'\n')
                else:
                    d = j
                    if d['response_code'] == 1:
                        f.write(d['url']+','+d['scan_id']+'\n')
            else:
                for u in chunk:
                    failed.append(u)
            time.sleep(16)
    print('---------')
    print('Complete!')
    print('---------')
    if failed:
        print('Had {} failures...'.format(len(failed)))
        with open('data/failed_submissions.txt', 'w') as f:
            f.write('\n'.join(failed))


if __name__ == '__main__':
    main()

