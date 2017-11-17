"""
Github ETL
"""
import argparse
import etl_utils
import datetime
import time

from simple_rest_client.api import API
from simple_rest_client.resource import Resource

RATE_SLEEP_LIMIT = 0.9

class OperationResource(Resource):
    """Resources to use"""
    actions = {
        'list_repositories': {'method': 'GET', 'url': '/search/repositories?q=+repo:{}&sort=stars&order=desc'},
        'list_users_repositories': {'method': 'GET', 'url': '/users/{}/repos'},
        'list_orgs_repositories': {'method': 'GET', 'url': '/orgs/{}/repos'},
        'stats_contributors': {'method': 'GET', 'url': '/repos/{}/stats/contributors'},
        'list_commits': {'method': 'GET', 'url': '/repos/{}/commits?page={}'},
        'list_watchers': {'method': 'GET', 'url': '/repos/{}/subscribers?page={}'},
    }

    def get_commits(api, repo):
        page = 1
        skip = 100
        last_result = 0
        while True:
            tries = 0
            print("Commits page {}".format(page))
            while tries < 10:
                try:
                    result = api.operations.list_commits(repo, page).body
                    time.sleep(RATE_SLEEP_LIMIT)
                    break
                except:
                    print("Commits tries {}".format(tries))
                    time.sleep(10)
                    tries = tries + 1
            if not result:
                if skip == 1:
                    page = page - 2
                    break
                page = page - skip
                skip = int(skip / 10)
            else:
                last_result = len(result)
                page = page + skip
        commits = page*30 + last_result
        return commits

    def get_watchers(api, repo):
        page = 1
        skip = 100
        last_result = 0
        while True:
            tries = 0
            print("Watchers page {}".format(page))
            while tries < 10:
                try:
                    result = api.operations.list_watchers(repo, page).body
                    time.sleep(RATE_SLEEP_LIMIT)
                    break
                except:
                    print("Commits tries {}".format(tries))
                    time.sleep(10)
                    tries = tries + 1
                    
            if not result:
                if skip == 1:
                    page = page - 2
                    break
                page = page - skip
                skip = int(skip / 10)
            else:
                last_result = len(result)    
                page = page + skip
        
        watchers = page*30 + last_result
        return watchers

    

    # def sum_commits(weeks):
    #     total = sum([int(e['c']) for e in weeks])
    #     print(total)
    #     return total

    # def get_commits(api, full_name):
    #     print('Hola')
    #     response = api.operations.stats_contributors(full_name)
    #     total = sum([OperationResource.sum_commits(e['weeks']) for e in response.body])
    #     print('{} - {}'.format(full_name, total))
    #     return total

parser = argparse.ArgumentParser(prog='github_etl', description='Extract information from GitHub')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-r', action='store_true', dest='is_single_repo', required=False, help='Is single repository info?')
parser.add_argument('-n', action='store', dest='org_usr', required=True, help='Organization name / User name / Repository name')
parser.add_argument('-o', action='store_true', dest='is_org', default=False, required=False, help='Set repositories belongs to an organization')
parser.add_argument('-f', action='store', dest='csv_file', required=True, help='Export csv filename')
args = parser.parse_args()


default_params = {'access_token': '17e285d62f70250db2d49eabb9b509b8f6b4f0ea'}
CLIENT_API = API(api_root_url='https://api.github.com', json_encode_body=True, params=default_params)
CLIENT_API.add_resource(resource_name='operations', resource_class=OperationResource)
HEADER = ('Date', 'Commits', 'Forks', 'Watchers', 'Stars', 'Size')

if args.is_org:
    RESULT = CLIENT_API.operations.list_orgs_repositories(args.org_usr)
    items = RESULT.body
if args.is_single_repo:
    RESULT = CLIENT_API.operations.list_repositories(args.org_usr)
    items = RESULT.body['items']
else:
    RESULT = CLIENT_API.operations.list_users_repositories(args.org_usr)
    items = RESULT.body


S_TODAY = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
#Get all repositories
#/*e['full_name'],*/
[etl_utils.append_info((S_TODAY, OperationResource.get_commits(CLIENT_API, e['full_name']), 
    e['forks_count'], OperationResource.get_watchers(CLIENT_API, e['full_name']), e['stargazers_count'], e['size']), args.csv_file, HEADER) 
 for e in etl_utils.sort_by(items, 'stargazers_count')]
