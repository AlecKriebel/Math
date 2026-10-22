#!/usr/bin/env python3
"""Verify complete corpus and privately held public-source bytes without emitting them."""
import argparse,hashlib,json
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    a=argparse.ArgumentParser();a.add_argument('--catalog',required=True);a.add_argument('--problems',required=True);a.add_argument('--reports',required=True);a.add_argument('--sources',required=True);a=a.parse_args()
    m=json.loads((Path(__file__).resolve().parent/'VERIFICATION_METADATA.json').read_text())
    loaded=[]
    for p,pin in zip([a.catalog,a.problems,a.reports],m['complete_corpora']):
        b=Path(p).read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'complete corpus mismatch: '+pin['name']);loaded.append(json.loads(b))
    catalog,problems,reports=loaded
    c=[x for x in catalog if str(x.get('id'))=='3800003'];p=[x for x in problems if str(x.get('id'))=='3800003']
    need(len(c)==len(p)==1,'exact ID is not unique');record=p[0];report=reports.get(record['problem_number'],{})
    need(record['problem_number']==c[0]['problem_number']=='AMR-037-0003' and c[0]['rank']==927,'exact identity mismatch')
    pair=json.dumps([record,report],sort_keys=True).encode();pin=m['complete_record_report_pair']
    need(len(pair)==pin['bytes'] and sha(pair)==pin['sha256']==c[0]['review_hash'],'complete pair mismatch')
    need(sha(record['statement'].encode())==m['statement_sha256']==c[0]['statement_hash'],'statement mismatch')
    need(report.get('classification')=='OPEN-TRIAGE','report classification mismatch')
    checked=0
    for pin in m['public_sources']:
        if 'sha256' not in pin:continue
        b=(Path(a.sources)/pin['filename']).read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'source mismatch: '+pin['filename']);checked+=1
    print(json.dumps({'result':'PASS','complete_corpora_verified':3,'unique_exact_id':3800003,'problem_number':'AMR-037-0003','rank':927,'pair_sha256':sha(pair),'public_source_files_verified':checked,'source_contents_emitted':False,'scope':'Byte and identity verification, not theorem certification.'},sort_keys=True))
if __name__=='__main__':main()
