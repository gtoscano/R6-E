"""
Github ETL
"""
import argparse
import etl_utils
import datetime

from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class OperationResource(Resource):
    """Resources to use"""
    actions = {
        'list_coins': {'method': 'GET', 'url': '/v1/ticker/?limit=120'},
    }


parser = argparse.ArgumentParser(prog='coinmarket_etl', description='Extract information from Coin Market')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-n', action='store_true', dest='get_name', default=False, required=False, help='Get coin name')
parser.add_argument('-f', action='store', dest='csv_file', required=True, help='Export csv filename')
args = parser.parse_args()


CLIENT_API = API(api_root_url='https://api.coinmarketcap.com', json_encode_body=True)
CLIENT_API.add_resource(resource_name='operations', resource_class=OperationResource)

if args.get_name:
    RESULT = CLIENT_API.operations.list_coins()
    [etl_utils.append_info([e['name']], args.csv_file) for e in RESULT.body]
