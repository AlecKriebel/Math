"""Actual-byte custody of the completed final review, not new math testing."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys

A=Path(__file__).resolve().parent
D=A/'final_partial_whole_record_adversary_20261004'
def digest(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def check(row):
 p=Path(row['path']); assert p.is_absolute() and p.is_file() and not p.is_symlink(),row['path']
 b=p.read_bytes(); assert len(b)==row['bytes'] and digest(b)==row['sha256'],row['path']
 return b
def pin(p):
 b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':digest(b)}
def main():
 assert sys.flags.ignore_environment and sys.flags.optimize==0 and sys.flags.dont_write_bytecode
 seal_pin=pin(D/'FINAL_SEAL.json')
 assert seal_pin['sha256']=='2cdf09d3c7e00f4d8ea1549efc46b55263401ab62a0261b201021a3b2ca22702'
 s=load(D/'FINAL_SEAL.json'); v=load(D/'VERDICT.json'); m=load(D/'FINAL_MANIFEST.json')
 assert s['verdict']==v['verdict']=='CLEAN' and s['essential_repairs']==v['essential_repairs']==[]
 assert s['submitted_head']==v['submitted_head']=='6f82e81631fd43abc0140a831acfb43c150f4210'
 assert v['original_effort']=='1/5' and v['new_central_proof_search_turns']==0
 assert s['full_connected_mathematics_clean'] and s['qualified_attributed_partial_record_clean'] and s['bounded_priority_audit_complete']
 assert s['historical_novelty_certified'] is False and s['intended_target_historical_resolution_certified'] is False
 assert v['current_scientific_status']=='partial' and v['operational_clearance'] is False
 seen={}
 def walk(x):
  if isinstance(x,dict):
   if {'path','bytes','sha256'}<=set(x):
    b=check(x); assert x['path'] not in seen or seen[x['path']]==digest(b)
    seen[x['path']]=digest(b)
   else:
    for value in x.values(): walk(value)
  elif isinstance(x,list):
   for value in x:walk(value)
 walk(s);walk(m)
 assert len(m['manifest'])==143 and len(m['private_cache_manifest'])==98
 assert digest(check(s['FIRST']))=='6f6bc5892f8b5450acf16bca0d610376b1c2f22cf3f1415cabd92e6a616bb5a1'
 process_paths=[Path(x['record']['path']) for x in m['process_readbacks']+s['completed_tail_processes']]
 process_paths.append(D/'seal_final.process.json')
 actual=[]
 for p in process_paths:
  r=load(p)
  assert r['child_pid']>0 and r['argv'] and r['cwd'] and r['exit_code'] in [0,1]
  assert r['prelaunch_utc']<=r['launched_utc']<=r['completed_utc']
  check(r['stdout']);check(r['stderr'])
  actual.append({'process':pin(p),'child_PID':r['child_pid'],'label':r['label'],'exit':r['exit_code'],'started':r['launched_utc'],'finished':r['completed_utc']})
 actual=list({x['process']['path']:x for x in actual}.values())
 seal_child=next(x for x in actual if x['label']=='seal_final')
 assert seal_child['child_PID']==84062 and seal_child['exit']==0
 # The seal-writing child time is not mislabeled as the later delivery readback.
 assert seal_child['finished']=='2026-10-04T19:34:51.410912+00:00'
 out=A/'ROOT_final_whole_record_closure_readback_20261004';out.mkdir(exist_ok=False)
 receipt={'status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),'actual_PID':os.getpid(),'actual_argv':sys.argv,
  'actual_cwd':os.getcwd(),'operator':pin(Path(__file__)),'final_seal':seal_pin,'finite_unique_pin_paths_actually_read':len(seen),
  'public_manifest_members':143,'private_manifest_members':98,'actual_process_receipts':actual,
  'FIRST_unchanged':True,'exact_V3_packet_verified':True,'final_connected_theorem_and_qualified_partial_record_clean':True,
  'historical_novelty_or_intended_target_resolution_certified':False,'new_math_tests':False,'native_or_PR_mutation':False,
  'final_ROOT_scientific_disposition_and_operational_authorization_still_separate':True}
 (out/'READBACK.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'status':'PASS','receipt':pin(out/'READBACK.json'),'unique_pins':len(seen),'process_receipts':len(actual)}))
if __name__=='__main__':main()
