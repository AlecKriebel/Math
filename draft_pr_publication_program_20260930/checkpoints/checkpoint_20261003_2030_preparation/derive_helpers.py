"""Exact documented derivation from ROOT-read1915 source; no production execution."""
from pathlib import Path
import datetime,difflib,hashlib,json,os
N=Path(__file__).absolute().parent;O=N.parent/'checkpoint_20261003_1915_preparation'
PINS={'common.py':'6aea8e653c9c20e6b746b9c64d05c040cc33713f80bf1f2dbcb05cd7dc58a8d1',
 'stage_checkpoint.py':'63c3d84e13f98f03ca64a048ec330ca5fbb637f389f6ff601c9baf1c2a9191d8',
 'commit_checkpoint.py':'7ce43551cb6da51e3ba0fef968abc56065e13bec97ef1db14849df8b503bd344',
 'capture_source.py':'045ce2206b6cf7e5b45124f4040cbb0bc4b6b8b098cdc8c9b682db3095624905',
 'verify_source.py':'833f7a766c7fc49ac6a0fe42119a014b3f1720c8da0889ddaf9a774d2c3cba78',
 'freeze_source.py':'645085ba730809797ddca1a65dc6d16c762a90a89b7bf9a0106c49a2972daf8f',
 'read_source.py':'4d9e598e290a5716480b1e43f20b105ba1950ed543b3ea6eb6dfda3a2367700c',
 'capture_finalization.py':'7b15421a2df4e03887c9526e3a7416ee40143a77a05f7bda15a1826361dd2bd8'}
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def rep(s,a,b):
 assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
def main():
 rows=[];diffs=[]
 for name,pin in PINS.items():
  f=O/name;b=f.read_bytes();assert hashlib.sha256(b).hexdigest()==pin;s=b.decode()
  if name=='common.py':s=rep(s,'checkpoint_20261003_1915_preparation','checkpoint_20261003_2030_preparation')
  if name=='stage_checkpoint.py':s=rep(s,'Checkpoint 20261003_1915 SOURCE reviewed by ROOT at ','Checkpoint 20261003_2030 SOURCE reviewed by ROOT at ')
  if name=='commit_checkpoint.py':
   s=rep(s,'Checkpoint completed PR48 V6 and PR60-61 research evidence','Checkpoint completed PR48 rollback and PR61-62 research evidence')
   s=rep(s,'Partial inventory38 is not completed acceptance; failed PR48 finalization is retained.','Selected PR48 rollback is complete; failed finalization remains retained. Native acceptance is still pending. Checkpoint1915 compression metadata is preserved.')
  if name=='verify_source.py':s=rep(s,'checkpoint1915-preparer-readonly-verification/v1','checkpoint2030-preparer-readonly-verification/v1')
  if name in ['freeze_source.py','read_source.py']:
   a="""        if j['exit_code']!=0:
            need(q.name=='source_initial_collection_actual_capture' and j['pid']==14273 and j['exit_code']==1
                 and digest((q/'CAPTURE.json').read_bytes())=='e345a8eb14d1caddc77bfbd70a24c15705bbc40a0305d184ed740180705806a3',
"""
   end="                 'Only the explicitly retained failed initial collector is qualified; no later failure is promoted')\n" if name=='freeze_source.py' else "                 'Retained qualified failure; no PASS promotion')\n"
   s=rep(s,a+end,"        need(j['exit_code']==0,'Current completed SOURCE captures must succeed; retained historical failure is selected separately')\n")
  if name=='freeze_source.py':
   s=rep(s,'actual_failed_inner_capture_files=11,storage_readback_packet_files=12,','completed_rollback_quarantine_files=13,storage_readback_packet_files=13,')
   s=rep(s,'partial_inventory38_is_not_completed_acceptance=True,','selected_rollback_does_not_complete_native_acceptance=True,')
   s=rep(s,'old1745_source_and_actual_receipts_unchanged=True,historical_FAILED80414_and80480_preserved=True,','old1915_source_and_actual_receipts_unchanged=True,historical_FAILED80414_and80480_unchanged_already_checkpointed=True,')
   s=rep(s,"      own_initial_collector14273_failed_and_qualified_not_PASS=True,\n",'')
  out=s.encode();put(N/name,out)
  rows.append(dict(name=name,base_path=str(f),base_bytes=len(b),base_sha256=pin,current_bytes=len(out),current_sha256=hashlib.sha256(out).hexdigest()))
  diffs+=list(difflib.unified_diff(b.decode().splitlines(True),s.splitlines(True),fromfile='ROOT-read1915/'+name,tofile='2030/'+name))
 put(N/'DERIVATION.diff',''.join(diffs).encode())
 r=dict(schema='checkpoint2030-explicit-source-derivation/v1',actual_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),rows=rows,
  production_changes='Literal folder/ROOT marker and commit prose only. Private staging, full foreign protection, index lock, exact-parent CAS and failure custody are unchanged.',
  administrative_changes='Dated verification naming/current-scope counters and strict success for this new SOURCE; prior failed source history is selected separately, not promoted.',
  production_helpers_executed=False,ROOT_approval=False)
 put(N/'DERIVATION.json',(json.dumps(r,indent=2,sort_keys=True)+'\n').encode());print(json.dumps(dict(status='SOURCE_ONLY_DERIVED',actual_pid=os.getpid(),files=len(rows))))
if __name__=='__main__':main()
