'''
dns.an is an answer or RR or resource record list. empty for queries
dns.qd is a Q or a query/question list
dns.ns is a name server record list
dns.qr indicates whether it is a query (0) or response (1)
dns.ar authority record list
dns.id an identifier set by the nameserver
dns.opcode RFC 2136
'''
import argparse
import csv

import dpkt


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='The PCAP to parse DNS data from')
    parser.add_argument('-o', type=str, required=True, help='Name of the outfile CSV')
    return parser.parse_args()


def main():
    args = get_args()
    pcap = dpkt.pcap.Reader(open(args.f))
    out = open(args.o, 'w')
    try:
        writer = csv.writer(out)
        writer.writerow( ('QR', 'OPCODE', 'QNAME', 'QTYPE', 'QCLS', 'RRNAME', 'RRTYPE', 'RCLS',
                          'TTL', 'RLEN', 'RDATA', 'AA', 'ID', 'QDCNT', 'ANCNT', 'NSCNT', 'ARCNT') )
        for timestamp, buf in pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)

                ip = eth.data
                if ip.p != 17:
                    continue

                udp = ip.data
                if udp.sport != 53 and udp.dport != 53:
                    continue

                dns = dpkt.dns.DNS(udp.data)

                row = [dns.qr, dns.opcode, '', '', '', '', '', '', '', '', '', dns.aa, dns.id,
                       len(dns.qd), len(dns.an), len(dns.ns), len(dns.ar)]
                if dns.qd:
                    row[2] = dns.qd[0].name
                    row[3] = dns.qd[0].type
                    row[4] = dns.qd[0].cls
                if dns.an:
                    row[5] = dns.an[0].name
                    row[6] = dns.an[0].type
                    row[7] = dns.an[0].cls
                    row[8] = dns.an[0].ttl
                    row[9] = dns.an[0].rlen
                    row[10] = dns.an[0].rdata
                writer.writerow(tuple(row))
            except Exception as e:
                print(str(e))
                continue
    finally:
        out.close()


if __name__ == '__main__':
    main()

