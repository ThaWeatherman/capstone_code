create directories:
    data/
    data/reports/

run the scripts with -h to see expected input, the scripts being `get_reports.py` and `start_scans.py`.

remember, VT has daily API limits.
you'll want a couple of accounts to get this done faster.
also, this will take a good 7 hours.
only 4 resources can be submitted at a time, and you can only make 4 calls per minute to an endpoint.

# Anchor extraction

once you have done all of that, run `python get_top_bad_domains.py` to generate an anchor CSV file.
it will be placed one directory up, which is the main experiment directory
