import argparse
import json
import logging
import requests

LOG = logging.getLogger('ads_api_client')
logging.basicConfig(level=logging.INFO)

def papers_by_year (api_token:str, year:int, fields:str, rows:int=10, start:int=0)->str:
    """ Call the ADS API and get all of the bibcodes for year """

    # query for all ids in a year
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_token)}

    api_url = f'https://api.adsabs.harvard.edu/v1/search/query?q=year:%s&rows=%s&start=%s&fl=%s' % (year, rows, start, fields) 
    LOG.debug(api_url)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def pull_all_papers_by_year (api_token:str, year:int, fields:str)->str:

    # get number of papers for that year 
    # ADS Call, limit to ONE paper (we just need metadata about size) 
    data = papers_by_year(api_token, year, fields, 1)
    LOG.debug(data)

    #parse out total papers for that year
    total_papers = data['response']['numFound']
    LOG.info(f"Num papers found for year:% => %s" % (year, total_papers))

    start = 0
    papers = []
    # work in batches of 2000 (the max allowed) to pull back the metadata we want
    while (start < total_papers): 
        data = papers_by_year(api_token, year, fields, 2000, start)

        # collect all data ids
        papers = papers + data['response']['docs']

        # TODO now pull all papers for these ids

        # bump start
        start = start+2000

    return papers


if __name__ == '__main__':  # use if csv of text

    ap = argparse.ArgumentParser(description='Client to pull data about ADS papers by year.')
    ap.add_argument('-d', '--debug', default = False, action = 'store_true', help='Turn on debugging messages')
    ap.add_argument('-f', '--fields', type=str, default="abstract,title,keyword,bibcode", help='ADS paper fields to pull.', required=False)
    ap.add_argument('-t', '--token', type=str, help='ADS API Token to use.', required=True)
    ap.add_argument('-y', '--year', type=int, help='Year to pull papers for.', required=True)

    args = ap.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        LOG.setLevel(logging.DEBUG)

    papers = {'year' : args.year}
    papers['docs'] = pull_all_papers_by_year(args.token, args.year, args.fields)

    #printing JSON to stdout
    print (json.dumps(papers))

