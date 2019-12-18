
#from urllib.parse import urlencode, quote_plus
#query = {"author":"martínez neutron star"}
#encoded_query = urlencode(query,quote_via=quote_plus)
#print(encoded_query)

import requests
import json

Token = 'iOTlKvECB8EqNWltL4WafhSrtLiplpdassiBuAkD' 

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

    data = papers_by_year(Token, year, 10)
    print (data)
    print (data['response']['numFound'])
    paper_ids = paper_ids + data['response']['docs']

    return paper_ids


print (pull_all_papers_by_year(Token, 1970))
