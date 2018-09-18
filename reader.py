import requests

import pandas as pd
from bs4 import BeautifulSoup


def process_single_result_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    tables = soup.find_all('table', 'list-table')

    assert len(tables) == 6
    df = pd.read_html(str(tables[0]))
    participant_tb = df[0].to_json(orient='values')

    df = pd.read_html(str(tables[1]))
    totals_tb = df[0].to_json(orient='values')
    df = pd.read_html(str(tables[4]))
    splits_tb = df[0].to_json(orient='records')
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html?highlight=to_json#pandas.DataFrame.to_json
    print(splits_tb)


def query_berlin_marathon(first_name, last_name, year):
    base_url = 'http://results.scc-events.com/'
    year_url = base_url + str(year) + '/'
    data = {
        'search[name]': last_name,
        'search[firstname]': first_name,
        'lang': 'EN',
        'event': 'MAL',
        'search[club]': '',
        'search[nation]': '',
        'search[start_no]': '',
        'num_results': '25',
        'search_sort': 'name',
        'search_sort_order': 'ASC',
        '_form_action': 'Submit',
    }
    res = requests.post(year_url + '?pid=search', data=data)

    soup = BeautifulSoup(res.content, 'html.parser')
    tables = soup.find_all('table', 'list-table')

    rows = tables[0].findAll('tr')
    results_links = list()
    for tr in rows:
        cols = tr.findAll('td')
        if len(cols) >= 4:
            link = cols[2].find('a').get('href')
            results_links.append(link)

    for url in results_links:
        process_single_result_page(year_url + url)


query_berlin_marathon('', 'DOE', 2015)
