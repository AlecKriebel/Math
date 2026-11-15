#!/usr/bin/env python3
"""Freeze only original source/scientific-owner/core inputs into this new owner.
Standard library; no native/project/scientific execution, network or subprocess.
"""
from pathlib import Path
import datetime
import hashlib
import json
E=Path(__file__).resolve().parent;P=E.parents[3]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def names(p):return sorted(str(x.relative_to(p)) for x in p.rglob('*') if x.is_file())
def main():
 need(not (E/'PROTECTED_INPUTS.json').exists(),'source freeze already exists')
 roots=[(P/'papers/23578142/sources',77),(P/'papers/23578142/reviews/scope',77),(P/'papers/23578142/reviews/adversarial',96),(P/'papers/23578142/reviews/root',30)]
 allpaths=set();namespaces=[]
 for d,count in roots:
  ns=names(d);need(len(ns)==count,'complete immutable input namespace '+str(d));namespaces.append({'path':str(d),'files':ns,'directories':sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_dir())});allpaths.update(d/n for n in ns)
 core=sorted((P/'scripts').glob('*.py'))+[P/'verification/final-content-check.py'];need(len(core)==18,'exact existing core18')
 need(pin(P/'scripts/checkpoint_subtree.py')['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','root-authorized checkpoint helper')
 allpaths.update(core)
 for n,size,sha in [('root-clearance-23578142-20261115.json',45068,'e3a6215de7c611ef3ced99ede5d358a11e4cef76a7ad1da46c95118b51ec48dd'),('root-science-initial-23578142-20261115.json',3991,'4242d3061bec32b0ac40151ab0d6db5137be98435eab402caf912a9ccdf43059')]:
  p=P/'verification'/n;need(pin(p)=={'bytes':size,'SHA256':sha},'exact root authority');allpaths.add(p)
 rows=[]
 for p in sorted(allpaths,key=str):
  need(not p.is_relative_to(E) and not str(p).startswith('/Users/alec/Desktop/'),'no owner self or website inputs')
  b=p.read_bytes();q=E/'inputs/blobs'/hashlib.sha256(b).hexdigest();q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists():q.write_bytes(b)
  rows.append({'path':str(p),'copy':str(q.relative_to(E)),**pin(p)})
 out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'whole_original_namespaces':namespaces,'source_files':77,'scientific_owner_files':[77,96,30],'core_files':[str(p) for p in core],'core_qualification':'17 original core inputs plus separately root-authorized checkpoint_subtree helper; not18original unchanged helpers','raw_inputs_ignored_before_creation':True,'no_source_scientific_or_old_campaign_execution':True,'website_read_or_mutated':False}
 (E/'PROTECTED_INPUTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'phase':'ORIGINAL_INPUTS_FROZEN','distinct_originals':len(rows),'namespaces':[len(x['files']) for x in namespaces],'core_files':18,'scientific_execution':False}))
if __name__=='__main__':main()
