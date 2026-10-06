#!/usr/bin/env python3
"""Optional read-only replay against locally supplied public dataset snapshots."""
import argparse
import hashlib
import json
from pathlib import Path

def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--catalog',type=Path,required=True);p.add_argument('--problems',type=Path,required=True);p.add_argument('--reports',type=Path,required=True);a=p.parse_args()
    expected=json.loads((Path(__file__).resolve().parent/'PUBLIC_METADATA.json').read_text())
    datasets={}
    for name,path in [('catalog',a.catalog),('complete_problems',a.problems),('research_results',a.reports)]:
        b=path.read_bytes();need({'bytes':len(b),'sha256':sha(b)}==expected['public_dataset_fingerprints'][name],'Dataset pin mismatch '+name);datasets[name]=json.loads(b)
    cc=[x for x in datasets['catalog'] if str(x['id'])=='30001737'];pp=[x for x in datasets['complete_problems'] if x['id']==30001737]
    need(len(cc)==len(pp)==1,'Nonunique target');c=cc[0];p=pp[0];reports=datasets['research_results']
    need(p['problem_number']==c['problem_number']=='OWR-4804-005','Problem number mismatch')
    sb=p['statement'].encode();rb=json.dumps([p,reports.get(p['problem_number'],{})],sort_keys=True).encode()
    need(sha(sb)==c['statement_hash']==expected['statement_identity']['sha256'] and len(sb)==expected['statement_identity']['bytes'],'Statement mismatch')
    need(sha(rb)==c['review_hash']==expected['full_record_review']['sha256'] and len(rb)==4195,'Full record review mismatch')
    need(p['problem_number'] not in reports,'Unexpected research report')
    print(json.dumps({'status':'pass','statement_match':True,'complete_record_review_match':True,'report_present':False,'scope':'Exact public dataset fingerprints and target matching only; no theorem verification.'},sort_keys=True))
if __name__=='__main__':main()
