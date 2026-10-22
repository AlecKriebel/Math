#!/usr/bin/env python3
"""Verify this pinned audit package's integrity and acceptance invariants."""
import hashlib
import json
from pathlib import Path
import re
import sys

FILES={'ACCEPTANCE.json','ACCEPTANCE.md','ARTIFACT_VERIFICATION.json','AUDITOR_SELF_TESTS.json','CORPUS_VERIFICATION.json','MATHEMATICAL_AUDIT.md','ORIGINAL_PRESERVATION.json','PDF_VERIFICATION.json','README.md','REPLAY_RESULTS.json','SOURCE_INSPECTIONS.json','SOURCE_REVIEW.md','replay_independent.py','verify_audit.py'}
def require(ok,msg):
 if not ok: raise ValueError(msg)
def unique(pairs):
 d={}
 for k,v in pairs:
  require(k not in d,'Duplicate JSON key');d[k]=v
 return d
def read(p):
 def bad(v): raise ValueError('Nonfinite JSON')
 return json.loads(p.read_text(),object_pairs_hook=unique,parse_constant=bad)
def main():
 require(len(sys.argv)<=2,'Usage: verify_audit.py [package_directory]')
 root=Path(sys.argv[1]) if len(sys.argv)==2 else Path(__file__).resolve().parent
 require(root.is_dir() and not root.is_symlink(),'Invalid package root')
 children=list(root.iterdir());require({x.name for x in children}==FILES|{'MANIFEST.json'},'Unexpected or missing member')
 require(all(x.is_file() and not x.is_symlink() for x in children),'Nonregular or symlink member')
 m=read(root/'MANIFEST.json');require(m['schema_version']==1,'Wrong manifest schema');entries=m['members']
 require(len(entries)==len(FILES) and {e['name'] for e in entries}==FILES,'Manifest coverage mismatch')
 for e in entries:
  require(type(e['bytes']) is int and e['bytes']>0 and re.fullmatch('[0-9a-f]{64}',e['sha256']),'Malformed entry')
  b=(root/e['name']).read_bytes();require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'Member pin mismatch: '+e['name'])
 a=read(root/'ACCEPTANCE.json');require(a['problem_id']==2733 and a['problem_number']=='KP-1.74' and a['rank']==907,'Wrong problem')
 require(a['verdict']=='ACCEPT_EXACT_AUTHOR_FREEZE_AS_PARTIAL_FORMULATION_AUDIT','Wrong verdict')
 require(a['accepted_archive']['bytes']==16395 and a['accepted_archive']['sha256']=='f05d1acd29f9366fa08facff81b97e561bcadd60072584dce6037a001e273953','Wrong accepted archive')
 require(a['accepted_external_manifest']['bytes']==3750 and a['accepted_external_manifest']['sha256']=='c715974ed45a383eb56086518b506887b340671025d532f3a33cf36f62cdeb44','Wrong author manifest')
 require(a['intended_nontrivial_part_a']==a['part_b']=='unresolved' and a['full_resolution'] is False and a['novelty_claim'] is False,'Mathematical overclaim')
 require(a['approaches_used']==2 and a['approach_limit']==5 and a['correction_required'] is False and a['derivative_created'] is False,'Wrong approach or patch status')
 r=read(root/'REPLAY_RESULTS.json');require(len(r['baseline_runs'])==6 and all(x['exit_code']==0 for x in r['baseline_runs']),'Invalid baselines')
 require(r['mutation_case_count']==14 and r['mutation_run_count']==len(r['mutation_runs'])==42 and all(x['exit_code']!=0 and x['failed_closed'] is True for x in r['mutation_runs']),'Invalid negative tests')
 c=read(root/'CORPUS_VERIFICATION.json');require(c['complete_problem_report_pair_sha256']=='3728d6f7692daadc11b003a16e89a90a49832dd78bdeb4fe0719072b0d1e81e0' and c['report_empty'] is True,'Wrong corpus gate')
 p=read(root/'PDF_VERIFICATION.json');require(len(p['pdfs'])==5 and all(x['match'] is True and x['redistributed'] is False for x in p['pdfs']),'Invalid source pins')
 print(json.dumps({'result':'PASS','problem_id':2733,'checked_payload_files':len(FILES),'intended_part_a':'unresolved','part_b':'unresolved','scope':'Audit integrity and stored acceptance invariants; not a geometry proof'},sort_keys=True))
if __name__=='__main__':
 try: main()
 except Exception as e:
  print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
