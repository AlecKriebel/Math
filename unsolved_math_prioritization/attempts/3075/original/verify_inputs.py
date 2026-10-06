#!/usr/bin/env python3
"""Check external private inputs, printing only metadata and match results."""
import hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent

def need(x,msg):
    if not x:raise ValueError(msg)

def main():
    need(len(sys.argv) in (4,5),'Usage: verify_inputs.py CATALOG PROBLEMS REPORTS [SOURCE_DIRECTORY]')
    pins=json.loads((ROOT/'IDENTITY.json').read_text());objects=[]
    for path,pin in zip(sys.argv[1:4],pins['input_snapshots']):
        b=pathlib.Path(path).read_bytes()
        need(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'Input pin mismatch: '+pin['filename'])
        objects.append(json.loads(b))
    catalog,problems,reports=objects
    records=[x for x in problems if str(x.get('id'))=='3075']
    cats=[x for x in catalog if str(x.get('id'))=='3075']
    need(len(records)==len(cats)==1,'Exact-ID count mismatch')
    record=records[0];cat=cats[0]
    need(record['problem_number']==cat['problem_number']=='OPG-605','Problem number mismatch')
    report=reports.get(record['problem_number'],{})
    need(report=={} and record['problem_number'] not in reports,'Prior report unexpectedly present')
    digest=hashlib.sha256(json.dumps([record,report],sort_keys=True).encode()).hexdigest()
    need(digest==pins['complete_record_report_pair_sha256']==cat['review_hash'],'Complete identity pair mismatch')
    checked_sources=[]
    if len(sys.argv)==5:
        for pin in json.loads((ROOT/'SOURCE_PINS.json').read_text())['sources']:
            b=(pathlib.Path(sys.argv[4])/pin['filename']).read_bytes()
            need(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'Source pin mismatch: '+pin['filename'])
            checked_sources.append(pin['filename'])
    print(json.dumps({'result':'PASS','problem_id':3075,'problem_number':'OPG-605','complete_identity_pair_sha256':digest,'sources_verified':checked_sources},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
