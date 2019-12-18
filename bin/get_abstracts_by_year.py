import argparse
import json
import logging
import requests

LOG = logging.getLogger('ads_api_client')
logging.basicConfig(level=logging.INFO)


def papers_by_year (api_token:str, year:int, rows:int=10, start:int=0)->str:
    """ Call the ADS API and get all of the bibcodes for year """

    # query for all ids in a year
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_token)}

    api_url = f'https://api.adsabs.harvard.edu/v1/search/query?q=year:%s&rows=%s&start=%s' % (year, rows, start) 
    print (api_url)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def pull_all_papers_by_year (api_token:str, year:int)->str:

    paper_ids = []

    data = papers_by_year(api_token, year, 10)
    print (data)
    print (data['response']['numFound'])
    paper_ids = paper_ids + data['response']['docs']

    return paper_ids



if __name__ == '__main__':  # use if csv of text

    ap = argparse.ArgumentParser(description='pii detection from text held in a file.')
    ap.add_argument('-d', '--debug', default = False, action = 'store_true', help='Turn on debugging messages')
    ap.add_argument('-t', '--token', type=str, help='ADS API Token to use.', required=True)
    ap.add_argument('-y', '--year', type=int, help='Year to pull papers for.', required=True)

    args = ap.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        LOG.setLevel(logging.DEBUG)

    print (pull_all_papers_by_year(args.token, args.year))

