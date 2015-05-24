import json
import csv
import glob, os, pdb

def parse(filename):
    paths = filename.split('/')
    _id = paths[-1].split('.')[0]

    with open(filename, 'r') as fh:
        csvpath = 'data/csv/' + _id + '.csv'

        headers = ["source", "timestamp", "sound",
                       "temperature", "airquality", "airquality_raw",
                       "light", "uv", "humidity", "dust", "latitude",
                       "longitude"]

        with open('data/csv/_headers', 'w') as hh:
            f_header = csv.DictWriter(hh, headers)
            f_header.writeheader()

        with open(csvpath, 'w') as ch:
            f_csv = csv.DictWriter(ch, headers)

            for line in fh:
                json_parse = json.loads(line)

                record = {
                    "source"            : json_parse["source"],
                    "timestamp"         : json_parse["timestamp"],
                    "sound"             : json_parse["data"].get("sound", ''),
                    "temperature"       : json_parse["data"].get("temperature", ''),
                    "airquality"        : json_parse["data"].get("airquality", ''),
                    "airquality_raw"    : json_parse["data"].get("airquality_raw", ''),
                    "light"             : json_parse["data"].get("light", ''),
                    "uv"                : json_parse["data"].get("uv", ''),
                    "humidity"          : json_parse["data"].get("humidity", ''),
                    "dust"              : json_parse["data"].get("dust", ''),
                    "latitude"          : json_parse["data"]["location"][1],
                    "longitude"         : json_parse["data"]["location"][0]
                }

                f_csv.writerow(record)

if __name__ == '__main__':
    for filename in glob.glob("data/json/*.json"):
        print "Parsing " + filename
        parse(filename)
