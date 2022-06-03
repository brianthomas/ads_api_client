
# search for matches of bibstems in data



import json

def chk_helio_bib(bibstem:str)->bool:
    bibstem_set = {'SpWea', 'GeoRL', 'JGR', 'JGRA', 'JGRE', 'LRSP', 'STP', 'P&SS','Ap&SS', 'SoPh','RvGSP','SSRv','AcAau','AcA','SLSci','SpReT','AdAnS','AdA&A','AASP','AdAp','AdAtS','AdGeo','AdSpR','ASPRv','AurPh','JComp','JPCom','Cmplx','LRCA','ApL','ASPRv','PLoSO','E&SS'}

    if bibstem in bibstem_set:
        return True
    return False

def count_helio_bibs(filename:str)->int:


  with open(filename, 'r') as f:
     data = json.load(f)

  match = 0

  # search docs for matching bibstems
  for doc in data['docs']:
     if 'bibstem' in doc:
         for b in doc['bibstem']:
             if chk_helio_bib(b):
                 match += 1
                 break
            
  return match, len(data['docs']) 


if __name__ == '__main__':  # use if csv of text
    import argparse

    ap = argparse.ArgumentParser(description='Count data about ADS papers which belong to helio sources.')
    ap.add_argument('-f', '--file', type=str, required=True)

    args = ap.parse_args()

    print (f"Matched %s bibs (%s docs)" % count_helio_bibs(args.file)) 

