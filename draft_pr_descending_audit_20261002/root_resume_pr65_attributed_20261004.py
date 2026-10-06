"""Authenticate an explicitly released Git window; never alter foreign files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002'
D=P/'private_shared_resume_pr65_attributed_20261004'
EXPECTED='54938331eec856ad95df7b18858eaac39d92f30b'
BASE='2a30fa40467f7c43370b13a8afd099f0bbdf9986'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b),mode=oct(stat.S_IMODE(p.stat().st_mode)))
def req(c,label):
    if not c:raise RuntimeError(label)
D.mkdir(exist_ok=False)
def run(tag,args):
    spec=dict(started_utc=utc(),argv=args,cwd=str(R),operator=pin(Path(__file__)))
    (D/(tag+'_preexecution.json')).write_text(json.dumps(spec,indent=2)+'\n')
    r=subprocess.run(args,cwd=R,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(tag+'.'+k)).write_bytes(b)
    spec.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    (D/(tag+'.json')).write_text(json.dumps(spec,indent=2)+'\n')
    req(r.returncode==0,tag+' failed');return r.stdout
req(run('branch',['/usr/bin/git','branch','--show-current'])==b'main\n','Not main')
head=run('head',['/usr/bin/git','rev-parse','HEAD']).decode().strip()
remote=run('remote',['/usr/bin/git','ls-remote','origin','refs/heads/main']).decode().split()[0]
req(head==remote==EXPECTED,'Released main/remote mismatch')
req(not run('staged',['/usr/bin/git','diff','--cached','--raw','-z']),'Index not empty')
index=run('index',['/usr/bin/git','ls-files','--stage','-z'])
ack=json.loads((P/'private_shared_pause_20261004_pr65_attributed_integration/ACKNOWLEDGEMENT.json').read_bytes())
owner={'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json','draft_pr_publication_program_20260930/audits/pr65_2305051/RESEARCH_LOG.md'}
current={rel:pin(R/rel) for rel in ack['tracked_dirty_pins']}
unchanged={rel:current[rel]==p for rel,p in ack['tracked_dirty_pins'].items() if rel not in owner}
req(len(unchanged)==11 and all(unchanged.values()),'Acknowledged foreign/descending body or mode changed')
live={}
for i,rel in enumerate(sorted(owner)):
    committed=run('owner_committed_'+str(i),['/usr/bin/git','show',head+':'+rel])
    delta=run('owner_delta_'+str(i),['/usr/bin/git','diff','--',rel])
    req(current[rel]['mode']=='0o644','Owner mode changed')
    live[rel]=dict(current=current[rel],committed=dict(bytes=len(committed),sha256=sha(committed)),postcheckpoint_delta_sha256=sha(delta))
paths=run('release_scope',['/usr/bin/git','diff','--name-only',BASE,head]).decode().splitlines()
def allowed(rel):
    return (rel.startswith('draft_pr_publication_program_20260930/audits/pr65_2305051/') or
            rel.startswith('draft_pr_publication_program_20260930/audits/pr45_9900007/root_pr65_') or
            rel=='draft_pr_publication_program_20260930/CURRENT_PROGRESS.json' or
            rel.startswith('unsolved_math_prioritization/attempts/2305051/') or
            rel in {'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/state.json'})
req(paths and all(allowed(p) for p in paths),'Released chain outside ascending scope')
req(current=={rel:pin(R/rel) for rel in current},'Tracked bodies changed during readback')
rec=dict(utc=utc(),status='PASS_EXPLICIT_PR65_ATTRIBUTED_INTEGRATION_RELEASE_VERIFIED',main=head,remote=remote,
         entire_index_empty=True,entire_index_sha256=sha(index),acknowledged_unchanged_paths=unchanged,
         ascending_live_paths=live,release_scope=paths,release_received=True,outbound_message_sent=False,
         program=pin(Path(__file__)))
(D/'RESUME_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n')
shared=json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes())
req(shared['shared_git_writes_paused'],'Window already resumed')
shared.update(utc=utc(),shared_git_writes_paused=False,dirty_tracked_bodies_modes_frozen_after_acknowledgement=False,
    resumed_because='Explicit ascending PR65 attributed-integration release; exact main/remote and empty index independently verified; all11 other acknowledged body/mode pins unchanged and two ascending live paths separately inventoried.',
    local_main_at_resume=head,remote_main_at_resume=remote,native_resume_capture_directory=str(D),
    all_staged_path_count=0,owned_staged_paths=[],descending_active_pr=311,
    descending_311_mathematical_verification_percent=60,descending_311_workflow_percent=20)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR65 attributed-integration explicit release independently verified: main=remote '+head+', entire index empty; all11 held foreign/descending body/mode pins preserved, two ascending-owned live logs separately captured and exact post-checkpoint diffs read. Shared writes resumed. PR311 both fresh source-first/prose assessments passed; author-code gate explicitly released after complete root reads; final independent consistency reviews pending. Math60%, workflow20%, priority0%, no acceptance/paper/publication clearance. Overall goal active.\n')
print(json.dumps({k:v for k,v in rec.items() if k!='release_scope'},indent=2))
