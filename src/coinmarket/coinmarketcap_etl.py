"""
Coin Market Cap ETL
"""
import argparse
import datetime
import requests
import etl_utils
from lxml import html
# import lxml.html

PARSER = argparse.ArgumentParser(prog='coinmarketcap_etl',
                                 description='Extract information from Coin Market Cap')
PARSER.add_argument('--version', action='version', version='%(prog)s 0.1')
PARSER.add_argument('-t', type=int, action='store', dest='top_number',
                    required=True, help='Get coin name')
PARSER.add_argument('-p', action='store', dest='path',
                    required=True, help='Path to save')
ARGS = PARSER.parse_args()

HTML_PAGE_CMC = 'https://coinmarketcap.com'

def extract_info(coin_market_page, today, filename):
    """Extract volumen 24h info"""
    page = requests.get(HTML_PAGE_CMC + coin_market_page)
    html_info = html.fromstring(page.content)

    table = etl_utils.read_csv(filename)
    header = []

    if not table:
        table = []
        header.insert(0, 'Date')
    else:
        header = table.pop(0)

    # print (table)
    # print (header)

    data = [None] * len(header)
    data[0] = today

    for market_root in html_info.xpath("//table[@id='markets-table']/tbody/tr"):
        market = market_root.getchildren()[1].xpath("a/text()")[0]
        market = market + "|" + market_root.getchildren()[2].xpath("a/text()")[0]
        notes = market_root.getchildren()[3].xpath("text()")[0].replace("\n", "").strip()
        volume = notes + (market_root.getchildren()[3].xpath("span/text()")[0]
                          .replace("\n", "").replace("\"", "").strip())
        if market in header:
            index = header.index(market)
            data[index] = volume
        else:
            header.append(market)
            data.append(volume)
            for row in table:
                row.append(None)

    table.append(data)
    table.insert(0, header)

    etl_utils.replace_csv_file(table, filename)


S_TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
NEXT_PAGE = ""
COIN_COUNT = 1
CURR_PAGE = 1
while True:
    CURRENT_PAGE = HTML_PAGE_CMC + NEXT_PAGE
    PAGE = requests.get(CURRENT_PAGE)
    HTML_INFO = html.fromstring(PAGE.content)
    for coin_root in HTML_INFO.xpath("//tr[starts-with(@id,'id-')]"):
        coin_filename = coin_root.xpath("@id")[0].replace("id-", "") + ".csv"
        coin_market = coin_root.xpath("td[4]//a/@href")[0]
        extract_info(coin_market, S_TODAY, ARGS.path + coin_filename)
        print(COIN_COUNT)
        COIN_COUNT = COIN_COUNT + 1
        if COIN_COUNT > ARGS.top_number:
            break

    if COIN_COUNT > ARGS.top_number:
        break

    CURR_PAGE = CURR_PAGE + 1
    NEXT_PAGE = "/" + str(CURR_PAGE)
