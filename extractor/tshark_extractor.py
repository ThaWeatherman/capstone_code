'''
flags_response == QR
a == IP (or data)
'''
import argparse
import csv

import pyshark


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='The PCAP to parse DNS data from')
    parser.add_argument('-o', type=str, required=True, help='Name of the outfile CSV')
    return parser.parse_args()


def main():
    args = get_args()
    cap = pyshark.FileCapture(args.f)
    out = open(args.o, 'w')
    fieldnames = ['qry_class', 'qry_name', 'qry_name_len', 'qry_type', 'resp_class',
                  'resp_len', 'resp_name', 'resp_ttl', 'resp_type', 'id', 'flags_opcode',
                  'flags_response', 'a', 'count_queries', 'count_auth_rr', 'count_answers']
    try:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        for pkt in cap:
            try:
                dns = pkt.dns
                d = {}
                for atr in fieldnames:
                    if hasattr(dns, atr):
                        d[atr] = getattr(dns, atr)
                writer.writerow(d)
            except Exception as e:
                print(str(e))
                continue
    finally:
        out.close()


if __name__ == '__main__':
    main()

