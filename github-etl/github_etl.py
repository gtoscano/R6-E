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
        'list_users_repositories': {'method': 'GET', 'url': '/users/{}/repos'},
        'list_orgs_repositories': {'method': 'GET', 'url': '/orgs/{}/repos'},
        'stats_contributors': {'method': 'GET', 'url': '/repos/{}/stats/contributors'},
    }

    def get_commits(github_api, full_name):
        response = github_api.operations.stats_contributors(full_name)
        total = sum([int(e['total']) for e in response.body])
        # print('{} - {}'.format(full_name, total))
        return total

parser = argparse.ArgumentParser(prog='github_etl', description='Extract information from GitHub')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-n', action='store', dest='org_usr', required=True, help='Organization name / User name')
parser.add_argument('-o', action='store_true', dest='is_org', default=False, required=False, help='Set repositories belongs to an organization')
parser.add_argument('-f', action='store', dest='csv_file', required=True, help='Export csv filename')
args = parser.parse_args()


default_params = {'access_token': 'eeac7491390f192733c4e8486d21e748eb7eee1e'}
GITHUB_API = API(api_root_url='https://api.github.com', json_encode_body=True, params=default_params)
GITHUB_API.add_resource(resource_name='operations', resource_class=OperationResource)
HEADER = ('Date', 'URL', 'Repository name', 'Commits', 'Forks', 'Watchers', 'Stars')

if args.is_org:
    RESULT = GITHUB_API.operations.list_orgs_repositories(args.org_usr)
else:
    RESULT = GITHUB_API.operations.list_users_repositories(args.org_usr)


S_TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
#Get all repositories
#/*e['full_name'],*/
[etl_utils.append_info((S_TODAY, e['url'], e['name'], 
 OperationResource.get_commits(GITHUB_API, e['full_name']), e['forks_count'], e['watchers_count'], e['stargazers_count']), args.csv_file, HEADER) 
 for e in etl_utils.sort_by(RESULT.body, 'stargazers_count')]
