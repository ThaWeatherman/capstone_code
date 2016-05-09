import json
import os


reports = 'virustotal/data/reports/'
malicious = open('malicious.txt', 'w')


with open('anom.txt') as f:
    for line in f:
        line = line.strip()
        filename = os.path.join(reports, line) + '.json'
        try:
            with open(filename) as g:
                r = json.load(g)
                score = r['positives']
                if score > 0:
                    malicious.write(line + '\n')
        except:
            pass

malicious.close()

