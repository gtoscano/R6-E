"""
List repository github
"""
import argparse
import etl_utils
import datetime
import csv
import time

from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class OperationResource(Resource):
    """Resources to use"""
    actions = {
        'get_repositories': {'method': 'GET', 'url': '/search/repositories?q={}&sort=stars&order=desc'},
    }

parser = argparse.ArgumentParser(prog='coinmarket_github', description='List first "main" repository project sorted by stars')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-s', action='store', dest='source', required=True, help='Source file with all cryptocoins names')
parser.add_argument('-o', action='store', dest='csv_file', required=True, help='Export csv filename with cypro, coin and repo')
args = parser.parse_args()


default_params = {'access_token': ''}
CLIENT_API = API(api_root_url='https://api.github.com', json_encode_body=True, params=default_params)
CLIENT_API.add_resource(resource_name='operations', resource_class=OperationResource)
HEADER = ('Crypto Coin', 'URL', 'Repository name')

def get_main_repository(api, name, csv_file):
    lower_name = name.lower()
    result = api.operations.get_repositories(lower_name)
    items = result.body['items']
    if not items:
        data = (name, "", "", "")
    else:
        data = next((name, e['owner']['html_url'], e['html_url'], e['full_name'], lower_name.replace(' ', '_') + ".csv") for e in items)
    etl_utils.append_tuples(data, csv_file) 
    time.sleep(3) #API restriction

with open(args.source) as file:
    STREAM = csv.reader(file, delimiter=',')
    [get_main_repository(CLIENT_API, e[0], args.csv_file) for e in STREAM]
