"""Verify the explicit ascending release before resuming this thread's writers."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,subprocess
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';D=P/'private_shared_resume_pr66_math_20261004_recovery_2';D.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):return dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=stat.S_IMODE(p.stat().st_mode))
def run(label,args):
    j=dict(argv=args,cwd=str(R),started_utc=utc(),operator=pin(Path(__file__)))
    (D/(label+'_preexecution.json')).write_text(json.dumps(j,indent=2)+'\n');r=subprocess.run(args,cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(label+'.'+k)).write_bytes(b)
    j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr));(D/(label+'.json')).write_text(json.dumps(j,indent=2)+'\n')
    assert r.returncode==0;return r.stdout
ack=json.loads((P/'private_shared_pause_pr66_math_20261004/PAUSE_ACKNOWLEDGEMENT.json').read_bytes())
released='7b0175c879e989ea505f6133cc3e6d1f639b12a7';expectedparent='f34bdaa039398948c4c12f9ecd36ca3852885e66'
branch=run('branch',['/usr/bin/git','branch','--show-current']).decode().strip();head=run('head',['/usr/bin/git','rev-parse','HEAD']).decode().strip()
remote=run('remote',['/usr/bin/git','ls-remote','origin','refs/heads/main']).decode().split()[0]
staged=run('staged',['/usr/bin/git','diff','--cached','--raw','-z']);index=run('index',['/usr/bin/git','ls-files','--stage','-z'])
parent=run('parent',['/usr/bin/git','rev-parse',head+'^']).decode().strip()
assert branch=='main' and head==remote==released and parent==expectedparent==ack['checkpoint'] and not staged
changed=run('released_paths',['/usr/bin/git','diff-tree','--no-commit-id','--name-only','-r',head]).decode().splitlines()
assert len(changed)==236 and all(x.startswith('draft_pr_publication_program_20260930/') for x in changed)
owner='draft_pr_publication_program_20260930/';checks={};live={}
for rel,old in ack['dirty_tracked_body_mode_pins_after_status_acknowledgement'].items():
    p=R/rel;current=pin(p)
    if rel.startswith(owner):
        if current==old:checks[rel]=True
        else:
            assert rel in [owner+'CURRENT_PROGRESS.json',owner+'audits/pr65_2305051/RESEARCH_LOG.md']
            assert current['mode']==old['mode'];live[rel]=dict(before=old,current=current,committed_sha256=sha(run('committed_'+str(len(live)),['/usr/bin/git','show',head+':'+rel])))
    else:assert current==old;checks[rel]=True
allowed_live={owner+'CURRENT_PROGRESS.json',owner+'audits/pr65_2305051/RESEARCH_LOG.md'}
protected=set(ack['dirty_tracked_body_mode_pins_after_status_acknowledgement'])-allowed_live
assert len(protected)==8 and protected<=set(checks) and all(checks.values())
assert set(checks)|set(live)==set(ack['dirty_tracked_body_mode_pins_after_status_acknowledgement'])
dirty=run('current_dirty_tracked',['/usr/bin/git','status','--porcelain=v1','-z','--untracked-files=no']).decode()
for record in dirty.split('\0'):
    if record:
        rel=record[3:]
        if rel not in ack['dirty_tracked_body_mode_pins_after_status_acknowledgement']:
            assert rel.startswith(owner+'audits/pr66_10400033/')
            live[rel]=dict(current=pin(R/rel),ownership='ascending newly committed path; operational state only, no math audit')
stamp=utc();j=dict(actual_utc=stamp,status='PASS_EXPLICIT_PR66_WINDOW_RELEASE_INDEPENDENTLY_VERIFIED',parent=parent,head=head,remote_main=remote,index_empty=True,
    entire_index_sha256=sha(index),held_checks=checks,ascending_live_states=live,changed_owner_paths=len(changed),outbound_message_sent=False,
    scientific_read_scope='Mechanical commit ownership, index and body/mode preservation only; no PR66 mathematical adjudication.',mathematical_percent=100,priority_percent=60,workflow_percent=40)
(D/'RESUME_RECEIPT.json').write_text(json.dumps(j,indent=2)+'\n')
sp=P/'SHARED_GIT_WINDOW_STATUS.json';s=json.loads(sp.read_bytes());assert s['shared_git_writes_paused'] and s['paused_for']=='PR66 mathematical checkpoint 20261004'
s.update(utc=stamp,shared_git_writes_paused=False,resumed_because='Explicit ascending release and fresh independent exact main/remote/index/owner/body-mode verification.',
    native_resume_capture_directory=str(D),local_main_at_resume=head,remote_main_at_resume=remote,dirty_tracked_bodies_modes_frozen_after_acknowledgement=False,
    descending_311_priority_percent=60,descending_311_workflow_percent=40)
sp.write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — Explicit ascending PR66 mathematical checkpoint release independently verified: parent/head/remote ownership236 paths, entire index empty, all8 held tracked body/mode states unchanged, ascending live operational states separately bound. Descending writers resume; PR311 math100%, priority60%, workflow40%; no outside/other-chat message.\n')
print(json.dumps(j,indent=2))
