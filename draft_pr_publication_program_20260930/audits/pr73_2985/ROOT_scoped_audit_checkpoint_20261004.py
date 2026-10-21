#!/usr/bin/env python3
"""One-shot audit-only checkpoint under an actual, tagged other-writer freeze."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys

R=Path('/Users/alec/Documents/Math')
P=R/'draft_pr_publication_program_20260930'
A=P/'audits/pr73_2985'
OUT=A/'ROOT_mathematical_audit_checkpoint_20261004'
TAG='PR73 mathematical-source checkpoint 20261004'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def pin(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha(b),mode=oct(p.lstat().st_mode))
OUT.mkdir(exist_ok=False)
counter=0
def run(argv):
 global counter
 counter+=1;begin=utc();c=subprocess.Popen(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=c.communicate();end=utc();label='%03d'%counter
 (OUT/(label+'.stdout.bin')).write_bytes(out);(OUT/(label+'.stderr.bin')).write_bytes(err)
 receipt=dict(PID=c.pid,argv=argv,cwd=str(R),started_utc=begin,finished_utc=end,exit_code=c.returncode,
  stdout=dict(path=label+'.stdout.bin',bytes=len(out),sha256=sha(out)),stderr=dict(path=label+'.stderr.bin',bytes=len(err),sha256=sha(err)))
 save(OUT/(label+'.json'),receipt)
 assert c.returncode==0,(argv,err.decode(errors='replace'))
 return out
def lines0(b):return [x.decode() for x in b.split(b'\0') if x]

plan=load(A/'ROOT_PUBLIC_SAFE_CHECKPOINT_PATHS_20261004.json')
paths=plan['paths'];assert len(paths)==len(set(paths)) and paths
for rel in paths:
 assert rel.startswith('draft_pr_publication_program_20260930/') and (R/rel).is_file()
 assert (R/rel).suffix.lower() not in {'.pdf','.png','.sqlite','.zip'}
assert all(not ('/original/' in r or '/current_sourcepair/' in r or '/commands/' in r) for r in paths)
assert sys.flags.optimize==0 and sys.flags.ignore_environment and sys.dont_write_bytecode
save(OUT/'PRELAUNCH_OPERATOR_AND_PLAN.json',dict(operator=pin(Path(__file__)),plan=pin(A/'ROOT_PUBLIC_SAFE_CHECKPOINT_PATHS_20261004.json'),PID=os.getpid(),argv=sys.argv,cwd=os.getcwd(),UTC=utc()))
(OUT/'executed_operator.py').write_bytes(Path(__file__).read_bytes())
ack_path=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
ack_bytes=ack_path.read_bytes();ack=json.loads(ack_bytes)
assert ack['shared_git_writes_paused'] is True and ack['paused_for']==TAG
assert ack['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True
assert ack['all_staged_path_count']==0
base=run(['git','rev-parse','HEAD']).decode().strip()
assert run(['git','branch','--show-current']).decode().strip()=='main'
remote=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
assert base==remote==ack['local_main_at_pause']==ack['remote_main_at_pause']
assert not run(['git','diff','--cached','--name-only','-z'])
dirty=lines0(run(['git','diff','--name-only','-z']))
foreign={rel:pin(R/rel) for rel in dirty if rel not in paths}
native={rel:pin(R/rel) for rel in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']}
owned_before={rel:pin(R/rel) for rel in paths}
save(OUT/'BEFORE.json',dict(UTC=utc(),base=base,remote=remote,actual_ack=ack,actual_ack_sha256=sha(ack_bytes),foreign_dirty_tracked=foreign,native=native,owned=owned_before))
run(['git','add','--']+paths)
staged=lines0(run(['git','diff','--cached','--name-only','-z']))
assert staged and set(staged)<=set(paths)
for rel,p in foreign.items():assert pin(R/rel)==p,rel
for rel,p in native.items():assert pin(R/rel)==p,rel
assert ack_path.read_bytes()==ack_bytes
run(['git','commit','-m','Audit PR73 mathematical counterexample and authenticate exact evidence'])
commit=run(['git','rev-parse','HEAD']).decode().strip()
assert run(['git','rev-parse','HEAD^']).decode().strip()==base
changed=lines0(run(['git','diff-tree','--no-commit-id','--name-only','-r','-z',commit]))
assert set(changed)==set(staged)
for rel,p in foreign.items():assert pin(R/rel)==p,rel
for rel,p in native.items():assert pin(R/rel)==p,rel
for rel,p in owned_before.items():assert pin(R/rel)==p,rel
assert not run(['git','diff','--cached','--name-only','-z'])
assert ack_path.read_bytes()==ack_bytes
run(['git','push','origin','main'])
after_remote=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
assert after_remote==commit==run(['git','rev-parse','HEAD']).decode().strip()
assert not run(['git','diff','--cached','--name-only','-z'])
for rel,p in foreign.items():assert pin(R/rel)==p,rel
for rel,p in native.items():assert pin(R/rel)==p,rel
assert ack_path.read_bytes()==ack_bytes
receipt=dict(status='PASS',UTC=utc(),actual_controller_PID=os.getpid(),audit_checkpoint_commit=commit,parent=base,
 committed_owned_paths=sorted(changed),committed_owned_path_count=len(changed),foreign_tracked_whole_bodies_and_modes_preserved=len(foreign),
 native_QUEUE_state_history_unchanged=True,index_empty=True,local_remote_main_equal=True,actual_ack_tag=TAG,
 primary_PDF_pixels_raw_dataset_API_streams_excluded=True,PR_merge_native_acceptance_publication_tracker_actions=False,
 manifest_membership_boundary='Referenced custody manifests inventory local evidence; this scoped Git checkpoint does not claim all their private or local members were uploaded.',
 actual_command_receipt_count=counter)
save(OUT/'RECEIPT.json',receipt)
print(json.dumps({k:receipt[k] for k in ['status','UTC','audit_checkpoint_commit','committed_owned_path_count','foreign_tracked_whole_bodies_and_modes_preserved']}))
