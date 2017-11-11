"""
Get information daily for all Github repositories
"""
import argparse
import csv
import os
import time


parser = argparse.ArgumentParser(prog='github_etl', description='Extract information from GitHub')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-s', action='store', dest='source', required=True, help='Input csv filename')
args = parser.parse_args()

def extract_information(e): 
    if len(e) == 5:
        call = "python github_etl.py -r -n {} -f repository/{}".format(e[3], e[4])
        print(call)
        os.system(call)
        time.sleep(3) #API restriction


with open(args.source) as file:
    STREAM = csv.reader(file, delimiter=',')
    [extract_information(e) for e in STREAM]