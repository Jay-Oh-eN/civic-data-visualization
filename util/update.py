import requests
import csv
import json
import dateutil.parser
import pytz
import datetime
import time
import pdb
import os.path
from sh import tail

base = 'http://sensor-api.localdata.com/api/v1/sources/'

sensors = {
    'Urban Launchpad' : 'ci4yfbbdb000d03zzoq8kjdl0',
    'GlenParklifeLogger': 'ci4yhy9yy000f03zznho5nm7c',
    'ClimateNinja9000': 'ci4yyrdqi000j03zz8ylornqd',
    'Exploratorium': 'ci4vy1tfy000m02s7v29jkkx4',
    'Datavore': 'ci4lnqzte000002xpokc9d25v',
    'Grand Theater': 'ci4usvy81000302s7whpk8qlp',
    'mapsense' : 'ci4usvryz000202s7llxjafaf',
    'GehlData' : 'ci4xcxxgc000n02tci92gpvi6',
    'a-streetcar-named-data-sensor' : 'ci4usss1t000102s7hkg0rpqg',
    'AlleyCat' : 'ci4tmxpz8000002w7au38un50',
    'DataDonut' : 'ci4yf50s5000c03zzt4h2tnsq',
    'grapealope' : 'ci4ut5zu5000402s7g6nihdn0'
}

def init_scrape(_id, end):
    #pdb.set_trace()
    print "Init scrape"
    initial = base + _id + '/entries?count=1'
    response = requests.get(initial)
    json_parse = response.json()
    date = json_parse['data'][0]['timestamp']
    
    with open('data/json/' + _id + '.json', 'w') as fh:
        #pdb.set_trace()
        write_data(fh, date, end)

def write_data(fh, date, end):
    next = base + _id + '/entries?count=1000&after=' + date
    counter = 0

    while dateutil.parser.parse(date) < end:
        if (counter % 10) == 0:
            print "downloading %s" % date

        response = requests.get(next)
        json_parse = response.json()

        if 'next' not in json_parse['links']:
            break

        next = json_parse['links']['next']
        date = json_parse['data'][-1]['timestamp']

        for d in json_parse['data']:
            fh.write(json.dumps(d))
            fh.write('\n')

        counter += 1
        time.sleep(1)

def append_file(path, end):
    last_row = tail('-n', '1', path)

    date = [ json.loads(d)['timestamp'] for d in last_row ]

    print "Appending"
    with open(path, 'a') as fh:
        write_data(fh, date[0], end)

if __name__ == '__main__':
    end = datetime.datetime.now(pytz.utc)

    for name, _id in sensors.items():
        print "Downloading {0}".format(name)
        filepath = 'data/json/' + _id + '.json'
    
        if os.path.isfile(filepath):
            append_file(filepath, end)
        else:
            init_scrape(_id, end)
