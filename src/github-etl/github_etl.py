"""
Github ETL
"""
import datetime
import time
import argparse
import etl_utils

from simple_rest_client.api import API
from simple_rest_client.resource import Resource

RATE_SLEEP_LIMIT = 0.9


class OperationResource(Resource):
    """Resources to use"""
    actions = {
        'list_repositories': {'method': 'GET',
                              'url': '/search/repositories?q=+repo:{}&sort=stars&order=desc'},
        'list_users_repositories': {'method': 'GET', 'url': '/users/{}/repos'},
        'list_orgs_repositories': {'method': 'GET', 'url': '/orgs/{}/repos'},
        'stats_contributors': {'method': 'GET', 'url': '/repos/{}/stats/contributors'},
        'list_commits': {'method': 'GET', 'url': '/repos/{}/commits?page={}'},
        'list_watchers': {'method': 'GET', 'url': '/repos/{}/subscribers?page={}'},
    }

    @staticmethod
    def get_commits(api, repo):
        """Get commits from history"""
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
        commits = page * 30 + last_result
        return commits

    @staticmethod
    def get_watchers(api, repo):
        """Get watchers from history"""
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

        watchers = page * 30 + last_result
        return watchers


PARSER = argparse.ArgumentParser(
    prog='github_etl', description='Extract information from GitHub')
PARSER.add_argument('--version', action='version', version='%(prog)s 0.1')
PARSER.add_argument('-r', action='store_true', dest='is_single_repo',
                    required=False, help='Is single repository info?')
PARSER.add_argument('-n', action='store', dest='org_usr', required=True,
                    help='Organization name / User name / Repository name')
PARSER.add_argument('-o', action='store_true', dest='is_org', default=False, required=False,
                    help='Set repositories belongs to an organization')
PARSER.add_argument('-u', action='store_true', dest='is_user', default=False, required=False,
                    help='Set repositories belongs to an user')
PARSER.add_argument('-f', action='store', dest='csv_file',
                    required=True, help='Export csv filename')
ARGS = PARSER.parse_args()

DEFAULT_PARAMS = {'access_token': ''}
CLIENT_API = API(api_root_url='https://api.github.com',
                 json_encode_body=True, params=DEFAULT_PARAMS)
CLIENT_API.add_resource(resource_name='operations',
                        resource_class=OperationResource)
HEADER = ('Date', 'Commits', 'Forks', 'Watchers', 'Stars', 'Size')

ITEMS = []
if ARGS.is_org:
    RESULT = CLIENT_API.operations.list_orgs_repositories(ARGS.org_usr)
    ITEMS = RESULT.body
if ARGS.is_single_repo:
    RESULT = CLIENT_API.operations.list_repositories(ARGS.org_usr)
    ITEMS = RESULT.body['items']
if ARGS.is_user:
    RESULT = CLIENT_API.operations.list_users_repositories(
        ARGS.org_usr.split('/')[0])
    ITEMS = [e for e in RESULT.body if e['full_name'] == ARGS.org_usr]

S_TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
# S_TODAY = (datetime.datetime.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')


RESULT = [etl_utils.append_info((S_TODAY,
                                 OperationResource.get_commits(
                                     CLIENT_API, e['full_name']),
                                 e['forks_count'], OperationResource.get_watchers(
                                     CLIENT_API, e['full_name']),
                                 e['stargazers_count'], e['size']), ARGS.csv_file, HEADER)
          for e in etl_utils.sort_by(ITEMS, 'stargazers_count')]
