"""
Get information daily for all Github repositories
"""
import argparse
import csv
import os
import time


PARSER = argparse.ArgumentParser(
    prog='github_etl', description='Extract information from GitHub')
PARSER.add_argument('--version', action='version', version='%(prog)s 0.1')
PARSER.add_argument('-s', action='store', dest='source',
                    required=True, help='Input csv filename')
PARSER.add_argument('-hi', action='store_true', dest='historical',
                    required=False, help='Get historical info')
ARGS = PARSER.parse_args()

def extract_information(record):
    '''Extract daily information'''
    if len(record) == 6:
        call = "python github_etl.py {} -n {} -f repository/github/{}".format(
            record[5], record[3], record[4])
        print(call)
        os.system(call)
        time.sleep(3)  # API restriction


def extract_historical_information(record):
    '''Extract historical information'''
    if len(record) == 6:
        call = "python github_historical_etl.py -n {} -f repository/github/{}".format(
            record[3], record[4])
        print(call)
        os.system(call)
        time.sleep(3)  # API restriction


with open(ARGS.source) as file:
    STREAM = csv.reader(file, delimiter=',')
    if ARGS.historical:
        RESULT = [extract_historical_information(record) for record in STREAM]
    else:
        RESULT = [extract_information(e) for e in STREAM]
