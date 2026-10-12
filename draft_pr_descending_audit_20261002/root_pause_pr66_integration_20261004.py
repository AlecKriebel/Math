"""Acknowledge the exact requested ascending integration window with fresh pins."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,subprocess
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';D=P/'private_shared_pause_pr66_integration_20261004'
D.mkdir(exist_ok=False);utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):return dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=stat.S_IMODE(p.stat().st_mode))
def run(label,args):
 j=dict(argv=args,cwd=str(R),started_utc=utc(),operator=pin(Path(__file__)))
 (D/(label+'_spec.json')).write_text(json.dumps(j,indent=2)+'\n')
 r=subprocess.run(args,cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),capture_output=True)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(label+'.'+k)).write_bytes(b)
 j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
 (D/(label+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n');assert r.returncode==0;return r.stdout
cp=json.loads((P/'checkpoint_311_preprint_026_receipt.json').read_bytes());assert cp['status']=='PASS_PR311_PREPARED_PREPRINT_CHECKPOINT_PUSHED'
gate=R/'draft_pr_publication_program_20260930/audits/pr66_10400033/ROOT_FINAL_PRIOR_DISPOSITION_20261004.json'
assert sha(gate.read_bytes())=='c426a1e28fff9825e22e417a1b46ddbb6dc52f97b777dae2097b8175d8c4b9a7'
branch=run('branch',['/usr/bin/git','branch','--show-current']).decode().strip()
head=run('head',['/usr/bin/git','rev-parse','HEAD']).decode().strip()
remote=run('remote',['/usr/bin/git','ls-remote','origin','refs/heads/main']).decode().split()[0]
staged=run('staged',['/usr/bin/git','diff','--cached','--raw','-z']);index=run('index',['/usr/bin/git','ls-files','--stage','-z'])
assert branch=='main' and head==remote==cp['commit'] and not staged
sp=P/'SHARED_GIT_WINDOW_STATUS.json';s=json.loads(sp.read_bytes());stamp=utc();assert stamp>'2026-10-04T17:29:10.078022+00:00'
assert not s['shared_git_writes_paused']
s.update(utc=stamp,shared_git_writes_paused=True,paused_for='PR66 attributed prior-result integration 20261004',
 reason='Incoming ascending request for exclusive attributed-prior PR66 integration; own CP026 pushed and native main/remote/index freshly checked.',
 resume_on='Explicit ascending release, followed by independent native head/remote/index and protected whole-body/mode verification',
 local_main_at_pause=head,remote_main_at_pause=remote,all_staged_path_count=0,owned_staged_paths=[],entire_index_sha256_at_pause=sha(index),
 native_pause_capture_directory=str(D),outbound_message_sent=False,descending_git_checkpoint_preparing=False,
 descending_mathematical_readonly_review_continues=True,dirty_tracked_bodies_modes_frozen_after_acknowledgement=True,
 descending_311_mathematical_verification_percent=100,descending_311_priority_percent=100,descending_311_workflow_percent=55)
sp.write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — Exclusive PR66 attributed-prior integration window acknowledged in shared status only, after incoming sealed final gate17:29:10UTC. Own CP026 pushed; native main=remote '+head+',indexempty. All dirty tracked whole bodies/modes held after acknowledgement; no Git/index/QUEUE/history writes until explicit release independently verified. PR311 first full preprint review may continue in a wholly untracked namespace. Math100%,boundedpriority100%,workflow55%; goalactive,no outboundother-chatmessage.\n')
dirty=run('dirty_tracked_after_ack',['/usr/bin/git','status','--porcelain=v1','-z','--untracked-files=no']);pins={}
for record in dirty.decode().split('\0'):
 if record:
  rel=record[3:];p=R/rel;assert p.is_file() and not p.is_symlink();pins[rel]=pin(p)
j=dict(actual_utc=utc(),acknowledgement_utc=stamp,status='SHARED_PR66_ATTRIBUTED_PRIOR_INTEGRATION_WINDOW_PAUSED',paused_for=s['paused_for'],
 local_main=head,remote_main=remote,index_empty=True,entire_index_sha256=sha(index),
 dirty_tracked_body_mode_pins_after_status_acknowledgement=pins,checkpoint=cp['commit'],operator=pin(Path(__file__)),outbound_message_sent=False,
 mathematical_percent=100,bounded_priority_percent=100,workflow_percent=55,goal_complete=False)
(D/'PAUSE_ACKNOWLEDGEMENT.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
