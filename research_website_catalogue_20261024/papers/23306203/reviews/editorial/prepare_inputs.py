#!/usr/bin/env python3
"""Explicit one-time source-only byte freeze. No project/science imports or replay."""
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
 need(not (E/'PROTECTED_INPUTS.json').exists(),'one-time freeze already exists')
 roots=[(P/'papers/23306203'/n,c) for n,c in [('sources',66),('reviews/scope',65),('reviews/adversarial',96),('reviews/root',29)]]
 namespaces=[];paths=set()
 for d,c in roots:
  fs=names(d);need(len(fs)==c,'complete immutable input namespace')
  namespaces.append({'path':str(d),'files':fs,'directories':sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_dir())});paths.update(d/n for n in fs)
 core=sorted((P/'scripts').glob('*.py'))+[P/'verification/final-content-check.py'];need(len(core)==18,'17 original core plus sole authorized checkpoint helper')
 need(pin(P/'scripts/checkpoint_subtree.py')['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','authorized checkpoint SHA')
 paths.update(core)
 for n,size,sha in [('root-clearance-23306203-20261115.json',41512,'bb07b481089011f96440e03e8fc657fba360d5067a9059302f9bdf6816b0c343'),('root-science-initial-23306203-20261115.json',3478,'57ad5e270050e9e4090c5b8519f75f3436fb948b04c826c31e417e920825efe6')]:
  p=P/'verification'/n;need(pin(p)=={'bytes':size,'SHA256':sha},'root exact authority');paths.add(p)
 rows=[]
 for p in sorted(paths,key=str):
  need(not p.is_relative_to(E) and not str(p).startswith('/Users/alec/Desktop/'),'no owner self or website input')
  b=p.read_bytes();q=E/'inputs/blobs'/hashlib.sha256(b).hexdigest();q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists():q.write_bytes(b)
  rows.append({'path':str(p),'copy':str(q.relative_to(E)),**pin(p)})
 need(len(rows)==276,'complete distinct original inputs')
 (E/'PROTECTED_INPUTS.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'whole_original_namespaces':namespaces,'core_files':[str(p) for p in core],'core_qualification':'17 original inputs plus separately root-authorized405b checkpoint helper','raw_inputs_ignored_before_creation':True,'source_scientific_or_old_campaigns_executed':False,'website_read_or_mutated':False},indent=2)+'\n')
 print(json.dumps({'phase':'ORIGINAL_SOURCE_INPUTS_FROZEN','distinct_originals':276,'whole_namespace_files':[66,65,96,29],'core_files':18,'scientific_execution':False}))
if __name__=='__main__':main()
