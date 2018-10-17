import io
import json
import sys
import csv

stream = io.open(sys.stdin.fileno(), encoding='utf-8')

writer = csv.writer(sys.stdout, delimiter='\t')
for campaign in json.loads(stream.read()):
    writer.writerow([
        str(campaign['campaignID']),
        campaign['campaignName'],
        campaign['platform'],
        campaign['channel'],
        campaign['partner'],
        campaign['advertiserName'],
        campaign['currency']
    ])
