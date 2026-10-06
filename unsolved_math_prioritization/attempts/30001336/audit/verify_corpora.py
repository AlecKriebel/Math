#!/usr/bin/env python3
"""Verify supplied full corpora; print only public hashes/counts/match results."""
import hashlib,json,pathlib,sys

def require(condition,label):
    if not condition: raise RuntimeError(label)

if len(sys.argv)!=4: raise SystemExit('Usage: verify_corpora.py catalog.json problems.json research_results.json')
names=('catalog.json','problems.json','research_results.json')
pins=('891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566','04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf','8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')
data={};rows=[]
for name,path,pin in zip(names,sys.argv[1:],pins):
    raw=pathlib.Path(path).read_bytes();digest=hashlib.sha256(raw).hexdigest();require(digest==pin,'full corpus hash '+name)
    data[name]=json.loads(raw);rows.append({'filename':name,'bytes':len(raw),'sha256':digest,'top_level_records':len(data[name])})
records=[x for x in data['problems.json'] if str(x['id'])=='30001336']
catalog=[x for x in data['catalog.json'] if str(x['id'])=='30001336']
require(len(records)==len(catalog)==1,'unique target')
r=records[0];position=data['catalog.json'].index(catalog[0])+1
require(position==825 and catalog[0]['rank']==825,'rank')
statement=hashlib.sha256(r['statement'].encode()).hexdigest()
review=hashlib.sha256(json.dumps([r,data['research_results.json'].get(r['problem_number'],{})],sort_keys=True).encode()).hexdigest()
require(statement=='17a1be49413d42ae3f434a21865940cdfa5f1a164571e8a6571d421236783f27','statement hash')
require(review=='2a87ecb68d9fd292d3b6baec29d17439aa52c62e672da02267811f0e2ddfda69','review hash')
print(json.dumps({'id':30001336,'rank':825,'corpora':rows,'target_unique':True,'catalog_rank_1_based':position,'statement_sha256':statement,'record_and_report_sha256':review,'target_match':True},indent=2))
