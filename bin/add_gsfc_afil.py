
import json
import re


'''
Parent  Child
0 	A03987 	GSFC 	NASA Goddard Space Flight Center, Maryland
A03987 	A11045 	CRESST 	Center for Research and Exploration in Space Science & Technology
A03987 	A11046 	JCET 	Joint Center for Earth Systems Technology, UMD, Baltimore
A03987 	A13048 	Plan Geo 	Goddard Space Flight Center, Planetary and Geophysics Divisions
A03987 	A13049 	Astro 	Goddard Space Flight Center, Astrophysics Division
A03987 	A13050 	GESTAR 	Goddard Earth Sciences Technology and Research
A03987 	A13059 	ESSIC 	Earth System Science Interdisciplinary Center
A00941 	A00948 	GISS 	Goddard Institute for Space Studies (@Columbia) 
0 	A00688 	NASA Wallops 	NASA Wallops Flight Facility

stretch?

A00151 	A13050 	GESTAR 	Goddard Earth Sciences Technology and Research (Morgan St U) 
A01409 	A13050 	GESTAR 	Goddard Earth Sciences Technology and Research (USRA) 
A01404 	A11075 	@NASA GSFC 	Catholic University at NASA GSFC

'''

NASA_grant_pattern = re.compile(r'NASA grant', re.IGNORECASE)

def is_gsfc_pub (doc:dict)->bool:

    # NASA afiliation list (from the ADS, see https://github.com/csgrant00/CanonicalAffiliations/blob/master/parent_child.tsv)

    NASA_Afiliations = ['A03987', 'A11045', 'A11046', 'A13048', 'A13049','A13050','A13059', 'A00948', 'A00688']

    # other afilliated GSFC funded institutions?
    '''
    '''
    
    # get the afiliation list and see if ANY of the listed afilliations matches a NASA institution
    if 'aff_id' in doc:
        for afil in doc['aff_id']:
            if afil in NASA_Afiliations:
                return True

    return False
            
def is_gsfc_grant_acknowledgement(doc:dict)->bool:
    # get the afiliation list and see if ANY of the listed afilliations matches a NASA institution
    if 'ack' in doc and NASA_grant_pattern.search(doc['ack']):
            return True

    return False


def get_paper_gsfc_status (doc:dict)->str:

    status = "NO"

    # get if nasa author
    is_NASA_pub = is_gsfc_pub(doc)
    
    if is_NASA_pub:
        status = "YES" # NASA_afiliation"
            
    return status

def contains_element(L1:list, L2:list)->bool:
    test = [i for i in L1 if i in L2]
    if len(test) > 0:
        return True
    return False

def gather_data(data_files:list, min_chars:int=99)->dict:
    
    papers = dict()
    
    # load our data
    for data_file in data_files:
        
        print (f"Doing %s" % data_file)
        with open(data_file, encoding='utf-8-sig') as f:
            data = json.load(f)
            
        #filtered_docs = [d for d in data['docs'] if contains_element(d['database'], allowed_database) and 'astronomy' in d['database'] and 'abstract' in d and len(d['abstract']) > min_chars]
        #print (f"  got %s matches for filtered list" % len(filtered_docs))

        gsfc_count = 0
        docs = []
        for doc in data['docs']:
            is_gsfc = get_paper_gsfc_status(doc)
            if is_gsfc == 'YES':
                gsfc_count += 1
            doc['gsfc-afil'] = is_gsfc
            docs.append(doc)

        # init our year of data
        year = data['year']
        papers[year] = { 'year': year, 'numFound': len(docs), 'docs': docs } 

        print (f"%s GSFC affiliations found" % gsfc_count)
        
    return papers

if __name__ == '__main__':  # use if csv of text
    import argparse

    ap = argparse.ArgumentParser(description='Script to add metadata for GSFC afiliation.')
    ap.add_argument('-d', '--debug', default = False, action = 'store_true', help='Turn on debugging messages')
    ap.add_argument('-f', '--files', nargs='+', type=str, help="Files to process", required=True)
    ap.add_argument('-p', '--pretty_print', default = False, action = 'store_true', help='Turn on pretty printed JSON output.')

    args = ap.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        LOG.setLevel(logging.DEBUG)

    papers = gather_data(args.files)
    for year in papers.keys():

        #printing JSON to file with '.new' appended
        with open(f"{year}.json.gsfc", "w") as f:
            if args.pretty_print:
                json.dump(papers[year], f, indent=2, sort_keys=True)
            else:
                json.dump(papers[year], f)
