"""Check the explicitly released integration chain and protected state before resume."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,subprocess
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';D=P/'private_shared_resume_pr66_integration_20261004';D.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):return dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=stat.S_IMODE(p.stat().st_mode))
def run(label,args):
 j=dict(argv=args,cwd=str(R),started_utc=utc(),operator=pin(Path(__file__)))
 (D/(label+'_spec.json')).write_text(json.dumps(j,indent=2)+'\n');r=subprocess.run(args,cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),capture_output=True)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(label+'.'+k)).write_bytes(b)
 j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr));(D/(label+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n')
 assert r.returncode==0;return r.stdout
ack=json.loads((P/'private_shared_pause_pr66_integration_20261004/PAUSE_ACKNOWLEDGEMENT.json').read_bytes())
released='48c4ff4d14a5bf8dece2bfe0a8cc70b865eba68a';accept='31d789fa7088e7916f489ad297ef75f74bd38ec8';merge='4068f9594e1687305908621ffd2043b7989218f3'
branch=run('branch',['/usr/bin/git','branch','--show-current']).decode().strip();head=run('head',['/usr/bin/git','rev-parse','HEAD']).decode().strip()
remote=run('remote',['/usr/bin/git','ls-remote','origin','refs/heads/main']).decode().split()[0]
staged=run('staged',['/usr/bin/git','diff','--cached','--raw','-z']);index=run('index',['/usr/bin/git','ls-files','--stage','-z'])
assert branch=='main' and head==remote==released and not staged
parents=run('chain',['/usr/bin/git','log','-3','--format=%H %P',head]).decode().splitlines()
assert parents==[released+' '+accept,accept+' '+merge,merge+' '+ack['checkpoint']+' 78f4a7fadac0fd24e147a617956cb409eb6a579e']
changed=run('checkpoint_paths',['/usr/bin/git','diff-tree','--no-commit-id','--name-only','-r',head]).decode().splitlines()
owner='draft_pr_publication_program_20260930/'
assert changed and all(x.startswith(owner) for x in changed)
all_changed=run('integration_paths',['/usr/bin/git','diff','--name-only',ack['checkpoint'],head]).decode().splitlines()
native='unsolved_math_prioritization/';allowed_native={native+x for x in ['QUEUE.md','state.json','history.jsonl']}
assert all(x.startswith(owner) or x.startswith(native+'attempts/10400033/') or x in allowed_native for x in all_changed)
q=native+'QUEUE.md';before_queue=run('queue_before',['/usr/bin/git','show',ack['checkpoint']+':'+q]);after_queue=run('queue_after',['/usr/bin/git','show',head+':'+q])
without_target=lambda b:b'\n'.join(x for x in b.split(b'\n') if b'10400033' not in x)
assert without_target(before_queue)==without_target(after_queue)
checks={};live={};allowed_live={owner+'CURRENT_PROGRESS.json',owner+'audits/pr66_10400033/RESEARCH_LOG.md'}
for rel,old in ack['dirty_tracked_body_mode_pins_after_status_acknowledgement'].items():
 current=pin(R/rel)
 if rel in allowed_live and current!=old:
  assert current['mode']==old['mode'];live[rel]=dict(before=old,current=current)
 else:assert current==old;checks[rel]=True
protected=set(ack['dirty_tracked_body_mode_pins_after_status_acknowledgement'])-allowed_live
assert len(protected)==8 and protected<=set(checks)
assert set(checks)|set(live)==set(ack['dirty_tracked_body_mode_pins_after_status_acknowledgement'])
dirty=run('current_dirty_tracked',['/usr/bin/git','status','--porcelain=v1','-z','--untracked-files=no']).decode()
for record in dirty.split('\0'):
 if record:
  rel=record[3:]
  if rel not in ack['dirty_tracked_body_mode_pins_after_status_acknowledgement']:
   assert rel.startswith(owner);live[rel]=dict(current=pin(R/rel),ownership='ascending live state')
stamp=utc();j=dict(actual_utc=stamp,status='PASS_EXPLICIT_PR66_INTEGRATION_RELEASE_INDEPENDENTLY_VERIFIED',
 base=ack['checkpoint'],merge=merge,acceptance=accept,checkpoint=head,remote_main=remote,entire_index_empty=True,index_sha256=sha(index),
 commit_chain_exact=True,checkpoint_only_ascending_owned_paths=len(changed),integration_changed_paths=len(all_changed),
 queue_all_non10400033_bytes_equal=True,held_whole_body_mode_checks=checks,ascending_live_states=live,
 scientific_scope='Operational chain/path ownership and foreign-state preservation only; no PR66 mathematical adjudication.',
 math_percent=100,bounded_priority_percent=100,workflow_percent=55,outbound_message_sent=False)
(D/'RESUME_RECEIPT.json').write_text(json.dumps(j,indent=2)+'\n')
sp=P/'SHARED_GIT_WINDOW_STATUS.json';s=json.loads(sp.read_bytes());assert s['shared_git_writes_paused'] and s['paused_for']=='PR66 attributed prior-result integration 20261004'
s.update(utc=stamp,shared_git_writes_paused=False,resumed_because='Explicit integration release independently verified for exact merge/acceptance/checkpoint chain, remote/index and all eight protected whole bodies/modes.',
 native_resume_capture_directory=str(D),local_main_at_resume=head,remote_main_at_resume=remote,dirty_tracked_bodies_modes_frozen_after_acknowledgement=False)
sp.write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — Explicit ascending PR66 integration release independently verified: exact merge4068f959/acceptance31d789fa/checkpoint48c4ff4d chain,main=remote,indexempty,only ascending/native10400033-owned paths and only that QUEUE row changed; all8protected tracked whole bodies/modes unchanged. Descending sharedwriters resume. Math100%,boundedpriority100%,workflow55%. No PR66 math audit or outboundmessage.\n')
print(json.dumps(j,indent=2))
