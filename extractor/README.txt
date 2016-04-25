Installation
------------

pip install -r requirements.txt

dpkt won't install in Py3 unfortunately, or I couldn't get it to anyways.
So Python 2 is a requirement.

Run
---

python <extractor.py> -f in.pcap -o out.csv

Example
-------

See included caps and csvs for example inputs and outputs.
Run tcpdump_extractor.py on captures done through tcpdump.
Run tshark_extractor.py on captures done through tshark.
