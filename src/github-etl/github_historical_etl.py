"""
Github ETL
"""
import datetime
import time
import argparse
import etl_utils

from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class OperationResource(Resource):
    """Resources to use"""
    actions = {
        'list_stars': {'method': 'GET', 'url': '/repos/{}/stargazers?page={}'},
        'list_commits': {'method': 'GET', 'url': '/repos/{}/commits?page={}'},
        'list_forks': {'method': 'GET', 'url': '/repos/{}/forks?page={}'},
    }

    @staticmethod
    def get_commits(github_api, full_name):
        """Get commits from history"""
        response = github_api.operations.stats_contributors(full_name)
        total = sum([int(e['total']) for e in response.body])
        # print('{} - {}'.format(full_name, total))
        return total


PARSER = argparse.ArgumentParser(
    prog='github_historical_etl', description='Extract historical information from GitHub')
PARSER.add_argument('--version', action='version', version='%(prog)s 0.1')
PARSER.add_argument('-n', action='store', dest='org_usr',
                    required=True, help='Owner name / Repository name')
PARSER.add_argument('-f', action='store', dest='csv_file',
                    required=True, help='Export csv filename')
ARGS = PARSER.parse_args()

RATE_SLEEP_LIMIT = 0.9
PARAMS = {'access_token': '9280cc85a7a72a8f166339f22d7de2c194e064f3'}
HEADERS = {'Accept': 'application/vnd.github.v3.star+json'}
CLIENT_API = API(api_root_url='https://api.github.com',
                 json_encode_body=True, params=PARAMS, headers=HEADERS)
CLIENT_API.add_resource(resource_name='operations',
                        resource_class=OperationResource)
HEADER = ('Date', 'Commits', 'Forks', 'Watchers', 'Stars', 'Size')


def get_historical_stars(api, repo):
    """Get historical information about stars"""
    data = []
    result = []
    page = 1
    while True:
        tries = 0
        print("Stars page {}".format(page))
        while tries < 10:
            try:
                result = api.operations.list_stars(repo, page).body
                time.sleep(RATE_SLEEP_LIMIT)
                break
            except:
                print("Stars tries {}".format(tries))
                time.sleep(10)
                tries = tries + 1

        page = page + 1
        if not result:
            break
        data.extend([(e['starred_at'][:10]) for e in result])
    data.sort()
    return data


def get_historical_forks(api, repo):
    """Get historical information about forks"""
    inner_data = []
    data = []
    result = []
    page = 1
    while True:
        tries = 0
        print("Forks page {}".format(page))
        while tries < 5:
            try:
                result = api.operations.list_forks(repo, page).body
                time.sleep(RATE_SLEEP_LIMIT)
                break
            except:
                print("Forks tries {} repo: {} page: {}".format(tries, repo, page))
                time.sleep(10)
                tries = tries + 1

        if tries == 5:
            break

        page = page + 1
        if not result:
            break
        curr_data = [(e['created_at'][:10], e['forks'], e['full_name'])
                     for e in result]
        inner_data.extend(curr_data)
        inner_forks = [e for e in curr_data if e[1] > 0]

        if inner_forks:
            # print(inner_forks)
            for fork in inner_forks:
                # print(fork)
                data.extend(get_historical_forks(api, fork[2]))

    data.extend([e[0] for e in inner_data])
    data.sort()
    return data


def get_historical_commits(api, repo):
    """Get historical information about commits"""
    data = []
    result = []
    page = 1
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

        page = page + 1
        if not result:
            break
        data.extend([(e['commit']['committer']['date'][:10]) for e in result])
    data.sort()
    return data

def get_historical(api, repo, csv_file):
    """Get historical information from all columns"""
    data_stars = get_historical_stars(api, repo)
    data_commits = get_historical_commits(api, repo)
    data_forks = get_historical_forks(api, repo)
    lmin = []
    if data_stars:
        lmin.append(data_stars[0])
    if data_commits:
        lmin.append(data_commits[0])
    if data_forks:
        lmin.append(data_forks[0])

    if not lmin:
        return

    min_date = min(lmin)

    curr_date = datetime.datetime.strptime(min_date, '%Y-%m-%d')
    today = datetime.datetime.today()
    data = []
    acc_commits = 0
    acc_forks = 0
    acc_stars = 0
    while True:
        if today < curr_date:
            break
        curr_sdate = curr_date.strftime('%Y-%m-%d')
        acc_commits = acc_commits + \
            len([e for e in data_commits if e == curr_sdate])
        acc_forks = acc_forks + len([e for e in data_forks if e == curr_sdate])
        acc_stars = acc_stars + len([e for e in data_stars if e == curr_sdate])
        # Commits,Forks,Watchers,Stars, Size
        data.append((curr_sdate, acc_commits, acc_forks, '', acc_stars, ''))
        curr_date = curr_date + datetime.timedelta(days=1)

    etl_utils.extend_info(data, csv_file, HEADER)


get_historical(CLIENT_API, ARGS.org_usr, ARGS.csv_file)
