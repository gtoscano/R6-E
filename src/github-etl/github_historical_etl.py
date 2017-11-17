"""
Github ETL
"""
import argparse
import etl_utils
import datetime
import time

from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class OperationResource(Resource):
    """Resources to use"""
    actions = {
        'list_stars': {'method': 'GET', 'url': '/repos/{}/stargazers?page={}'},
        'list_commits': {'method': 'GET', 'url': '/repos/{}/commits?page={}'},
        'list_forks': {'method': 'GET', 'url': '/repos/{}/forks?page={}'},
    }

    def get_commits(github_api, full_name):
        response = github_api.operations.stats_contributors(full_name)
        total = sum([int(e['total']) for e in response.body])
        # print('{} - {}'.format(full_name, total))
        return total

parser = argparse.ArgumentParser(prog='github_historical_etl', description='Extract historical information from GitHub')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-n', action='store', dest='org_usr', required=True, help='Owner name / Repository name')
parser.add_argument('-f', action='store', dest='csv_file', required=True, help='Export csv filename')
args = parser.parse_args()

RATE_SLEEP_LIMIT = 0.9
PARAMS = {'access_token': '17e285d62f70250db2d49eabb9b509b8f6b4f0ea'}
HEADERS = {'Accept': 'application/vnd.github.v3.star+json'}
CLIENT_API = API(api_root_url='https://api.github.com', json_encode_body=True, params=PARAMS, headers=HEADERS)
CLIENT_API.add_resource(resource_name='operations', resource_class=OperationResource)
HEADER = ('Date', 'Commits', 'Forks', 'Watchers', 'Stars', 'Size')

def get_historical_stars(api, repo):
    data = []
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
    inner_data = []
    data = []
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
        curr_data = [(e['created_at'][:10], e['forks'], e['full_name']) for e in result]
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
    data = []
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
    data_stars = get_historical_stars(api, repo)
    data_commits = get_historical_commits(api, repo)
    data_forks = get_historical_forks(api, repo)
    # print (data_forks)
    # data_stars = ['2016-08-26', '2016-09-03', '2016-09-19', '2016-12-24', '2017-01-17', '2017-02-22', '2017-03-06', '2017-03-12', '2017-05-04', '2017-05-11', '2017-06-01', '2017-06-01', '2017-06-07', '2017-06-17', '2017-06-18', '2017-06-19', '2017-06-30', '2017-07-02', '2017-07-06', '2017-07-17', '2017-07-19', '2017-07-21', '2017-07-27', '2017-07-28', '2017-08-03', '2017-08-04', '2017-08-06', '2017-08-07', '2017-08-07', '2017-08-08', '2017-08-10', '2017-08-15', '2017-08-18', '2017-08-18', '2017-08-19', '2017-08-23', '2017-08-26', '2017-08-28', '2017-08-31', '2017-08-31', '2017-09-03', '2017-09-08', '2017-09-08', '2017-09-12', '2017-09-13', '2017-09-22', '2017-09-23', '2017-09-24', '2017-09-25', '2017-09-30', '2017-11-05', '2017-11-06', '2017-11-13']
    # data_commits = ['2015-11-02', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-03', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-04', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-05', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-06', '2015-11-09', '2015-11-11', '2015-11-11', '2015-11-12', '2015-11-12', '2015-11-12', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-13', '2015-11-17', '2015-11-17', '2015-11-17', '2015-11-18', '2015-11-18', '2015-11-18', '2015-11-18', '2015-11-18', '2015-11-18', '2015-11-19', '2015-11-19', '2015-11-19', '2015-11-19', '2015-11-19', '2015-11-19', '2015-11-20', '2015-11-20', '2015-11-20', '2015-11-20', '2015-11-25', '2015-11-27', '2015-11-27', '2015-11-27', '2015-11-27', '2015-11-30', '2015-11-30', '2015-11-30', '2015-11-30', '2015-11-30', '2015-11-30', '2015-11-30', '2015-12-02', '2015-12-02', '2015-12-02', '2015-12-02', '2015-12-02', '2015-12-02', '2015-12-02', '2015-12-03', '2016-01-18', '2016-01-28', '2016-01-28', '2016-01-28', '2016-01-28', '2016-01-28', '2016-01-28', '2016-03-22', '2016-03-22', '2016-03-31', '2016-03-31', '2016-04-01', '2016-05-11', '2016-05-12', '2016-07-06', '2016-08-01', '2016-08-05', '2016-08-05', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-06', '2016-09-08', '2016-10-03', '2016-10-05', '2016-10-11', '2016-10-28', '2016-11-07', '2016-11-08', '2016-11-08', '2016-11-08', '2016-11-08', '2017-01-12', '2017-01-13', '2017-01-17', '2017-03-01', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-02', '2017-03-22', '2017-03-28', '2017-04-03', '2017-04-11', '2017-04-11', '2017-05-15', '2017-05-15', '2017-05-16', '2017-05-16', '2017-05-16', '2017-05-16', '2017-05-16', '2017-05-16', '2017-06-07', '2017-06-07', '2017-06-07', '2017-06-07', '2017-06-13', '2017-06-13', '2017-06-13', '2017-06-13', '2017-06-13', '2017-06-13', '2017-06-15', '2017-07-06', '2017-07-19', '2017-07-19', '2017-07-19', '2017-07-19', '2017-07-19', '2017-07-19', '2017-07-19', '2017-07-19', '2017-07-19', '2017-07-19', '2017-08-11', '2017-08-11', '2017-08-11', '2017-08-15', '2017-08-16']    
    # data_forks = ['2015-11-15', '2015-11-25', '2016-07-29', '2016-08-09', '2016-09-08', '2017-01-17', '2017-01-17', '2017-03-12', '2017-06-13', '2017-06-20', '2017-07-19', '2017-08-25', '2017-08-31', '2017-09-05', '2017-09-09', '2017-09-16', '2017-09-24', '2017-11-06', '2017-11-11']
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
        acc_commits = acc_commits + len([e for e in data_commits if e == curr_sdate])
        acc_forks = acc_forks + len([e for e in data_forks if e == curr_sdate])
        acc_stars = acc_stars + len([e for e in data_stars if e == curr_sdate])
        # Commits,Forks,Watchers,Stars, Size
        data.append((curr_sdate, acc_commits, acc_forks, '', acc_stars, ''))
        curr_date = curr_date + datetime.timedelta(days=1)

    etl_utils.extend_info(data, csv_file, HEADER)

get_historical(CLIENT_API, args.org_usr, args.csv_file)
