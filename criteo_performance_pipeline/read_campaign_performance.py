import csv
import io
import json
import sys

stream = io.open(sys.stdin.fileno(), encoding='utf-8')

writer = csv.writer(sys.stdout, delimiter=';', quoting=csv.QUOTE_MINIMAL)
for row in json.loads(stream.read()):
    writer.writerow([
        row['campaignID'],
        row['dateTime'],
        row.get('click'),
        row.get('impressions'),
        row.get('CTR'),
        row.get('revcpc'),
        row.get('ecpm'),
        row.get('cost'),
        row.get('sales'),
        row.get('convRate'),
        row.get('orderValue'),
        row.get('salesPostView'),
        row.get('convRatePostView'),
        row.get('orderValuePostView'),
        row.get('costOfSale'),
        row.get('overallCompetitionWin'),
        row.get('costPerOrder'),
    ])
