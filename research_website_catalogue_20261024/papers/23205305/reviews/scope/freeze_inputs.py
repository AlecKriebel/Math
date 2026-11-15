#!/usr/bin/env python3
"""Opaque one-time input custody only. No supplied code imports or science."""
from pathlib import Path
import datetime
import hashlib
import json
E=Path(__file__).resolve().parent;P=E.parents[3];S=P/'papers/23205305/sources'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def main():
 need(not (E/'PROTECTED_INPUTS.json').exists(),'one-time freeze already exists')
 fs=sorted(str(x.relative_to(S)) for x in S.rglob('*') if x.is_file());need(len(fs)==126,'whole original source namespace')
 for n,sha in [('SOURCE_READY.json','d5e1575052e0db802b6d8ff47309660b50213d91594856eb4df141943bf0db91'),('SOURCE_READY_SEAL.json','6540b1c94839ae033e0747843452bd6c33d29c3734680332c8cbc119e79fdcc8')]:need(pin(S/n)['SHA256']==sha,'exact native source terminal')
 core=sorted((P/'scripts').glob('*.py'))+[P/'verification/final-content-check.py'];need(len(core)==18,'17 original plus authorized checkpoint core')
 need(pin(P/'scripts/checkpoint_subtree.py')['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','sole authorized checkpoint helper')
 rows=[]
 for p in sorted([S/n for n in fs]+core,key=str):
  b=p.read_bytes();q=E/'inputs/blobs'/hashlib.sha256(b).hexdigest();q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists():q.write_bytes(b)
  rows.append({'path':str(p),'copy':str(q.relative_to(E)),**pin(p)})
 need(len(rows)==144,'complete distinct inputs')
 (E/'PROTECTED_INPUTS.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'source_namespace':{'path':str(S),'files':fs,'directories':sorted(str(x.relative_to(S)) for x in S.rglob('*') if x.is_dir())},'core_files':[str(p) for p in core],'core_qualification':'17 original plus separately root-authorized405b checkpoint helper','opaque_copy_not_semantic_support_code_output_or_opinion_exposure':True,'raw_inputs_ignored_before_creation':True,'other_current_scientific_review_or_root_files_copied':False,'source_or_native_programmes_executed':False},indent=2)+'\n')
 print(json.dumps({'phase':'INITIAL_OPAQUE_SOURCE_CUSTODY','source_files':126,'distinct_inputs':144,'scientific_execution':False,'support_opinions_or_results_interpreted':False}))
if __name__=='__main__':main()
