#!/usr/bin/env python3
"""Custody only: standard library, no scientific or project imports, writes,
subprocesses, network, replay, rendering, or mathematical computation."""
from pathlib import Path
import hashlib
import json
A=Path(__file__).resolve().parent
checks=0
def need(ok,why):
 global checks
 checks+=1
 if not ok:raise ValueError(why)
def read(p):return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(p):
 b=read(p);return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def bound(p,r):need(pin(p)=={'bytes':r['bytes'],'SHA256':r['SHA256']},str(p))
def names(p):return sorted(str(x.relative_to(p)) for x in p.rglob('*') if x.is_file())
need(pin(A/'INITIAL_SEAL.json')['SHA256']=='1f5d79148e117f81c8a9cc53746984dfbf11e85199b2ccf7de535f26274ac9e7','initial seal')
bound(A/'INITIAL_MANIFEST.json',obj(A/'INITIAL_SEAL.json')['manifest'])
for n,r in obj(A/'INITIAL_MANIFEST.json')['payloads'].items():bound(A/n,r)
for r in obj(A/'INITIAL_INPUTS.json')['files']:
 bound(Path(r['original']),r);need(read(Path(r['original']))==read(A/r['copy']),'whole original controlling input')
r=obj(A/'EDITORIAL_REVIEW_BINDINGS.json');E=Path(r['editorial_directory'])
need(names(E)==sorted(r['files']),'complete reviewed editorial file namespace')
for n,b in r['files'].items():bound(E/n,b)
for row in r['native_asset_copies']:
 bound(Path(row['original']),row);bound(E/row['copy'],row)
 need(read(Path(row['original']))==read(E/row['copy']),'whole unchanged native download')
for row in r.get('whole_json_equalities',[]):
 def get(value,path):
  for key in path:value=value[key]
  return value
 def equal(x,y):
  if type(x) is not type(y):return False
  if isinstance(x,dict):return list(x)==list(y) and all(equal(x[k],y[k]) for k in x)
  if isinstance(x,list):return len(x)==len(y) and all(equal(a,b) for a,b in zip(x,y))
  return x==y
 need(equal(get(obj(Path(row['original'])),row['original_pointer']),get(obj(E/row['copy']),row['copy_pointer'])),'whole typed custody '+row['label'])
v=obj(A/'CUSTOM_VERDICT.json')
need(v['publication_authority'] is False and v['canonical_url'] is None and v['AA'] is None and v['follow_up'] is None,'private authority')
if (A/'FINAL_SEAL.json').exists():
 f=obj(A/'FINAL_SEAL.json');bound(A/'OWNED_MANIFEST.json',f['manifest']);m=obj(A/'OWNED_MANIFEST.json')
 need(names(A)==sorted(list(m['payloads'])+['OWNED_MANIFEST.json','FINAL_SEAL.json']),'strict own final namespace')
 for n,b in m['payloads'].items():bound(A/n,b)
print(json.dumps({'status':'PASS_READ_ONLY_INFORMED_EDITORIAL_CUSTODY','checks':checks,'selected_controlling_inputs':len(obj(A/'INITIAL_INPUTS.json')['files']),'reviewed_editorial_files':len(r['files']),'native_asset_copies':len(r['native_asset_copies']),'project_imports_science_network_subprocess_or_writes':False,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None},indent=2))
