#!/usr/bin/env python3
"""Optionally verify full external corpora; publish hashes and matches, never records."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('catalog');p.add_argument('problems');p.add_argument('research_results')
a=p.parse_args();root=Path(__file__).resolve().parent
expected=json.loads((root/'VERIFICATION_METADATA.json').read_text())['identity']
data=[]
for path,row in zip([a.catalog,a.problems,a.research_results],expected['datasets']):
    b=Path(path).read_bytes()
    if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:
        raise SystemExit('FAIL: corpus byte count or SHA-256: '+row['name'])
    d=json.loads(b)
    if len(d)!=row['records']:raise SystemExit('FAIL: corpus record count')
    data.append(d)
catalog,problems,research=data
cs=[v for v in catalog if str(v.get('id'))=='30005995']
ps=[v for v in problems if str(v.get('id'))=='30005995']
if len(cs)!=1 or len(ps)!=1:raise SystemExit('FAIL: nonunique identity')
c,q=cs[0],ps[0];number='OWR-14298587-010'
if q['problem_number']!=number or c['problem_number']!=number:raise SystemExit('FAIL: number')
if q['title']!=c['title'] or q['source_url']!=c['source_url']:raise SystemExit('FAIL: title/source identity')
prior=research.get(number,{})
for k,v in research.items():
    if k in ('30005995',number) or (isinstance(v,dict) and (str(v.get('id',''))=='30005995' or str(v.get('problem_id',''))=='30005995' or v.get('problem_number')==number)):
        raise SystemExit('FAIL: unexpected target research record')
sh=hashlib.sha256(q['statement'].encode()).hexdigest()
rh=hashlib.sha256(json.dumps([q,prior],sort_keys=True).encode()).hexdigest()
if sh!=c['statement_hash'] or sh!=expected['statement_sha256']:raise SystemExit('FAIL: statement hash')
if rh!=c['review_hash'] or rh!=expected['review_sha256']:raise SystemExit('FAIL: review hash')
print(json.dumps({'identity':'PASS','statement_sha256':sh,'review_sha256':rh,'full_corpora':3,'research_record_found':False},sort_keys=True))
