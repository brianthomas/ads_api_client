# ADS API Client

## About
Client for Harvard Smithsonian Astrophystical Data System API. Optimized for pulling metadata about Astrophysics papers held in their system.

## Usage

```bash
usage: ads_client.py [-h] [-d] [-f FIELDS] -t TOKEN -y YEAR

Client to pull data about ADS papers by year.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Turn on debugging messages
  -f FIELDS, --fields FIELDS
                        ADS paper fields to pull.
  -t TOKEN, --token TOKEN
                        ADS API Token to use.
  -y YEAR, --year YEAR  Year to pull papers for.

```
