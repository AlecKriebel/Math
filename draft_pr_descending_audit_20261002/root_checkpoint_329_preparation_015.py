"""Checkpoint fresh second-review family closure, preserving all foreign state."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr329_20000450'
name='checkpoint_329_preparation_015'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def git(*args):return subprocess.check_output(['git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(name+'_receipt.json')).exists()
window();assert git('branch','--show-current')==b'main\n'
assert not git('diff','--cached','--raw','-z') and not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
parent=git('rev-parse','HEAD').decode().strip();assert parent=='66f240bd4d9d5d40fffd850ac60496ef47e7461c'
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
owned=[P/'RESEARCH_LOG.md',P/'SHARED_GIT_WINDOW_STATUS.json',P/'inventory.json',P/'checkpoint_329_preparation_014_receipt.json',Path(__file__),A/'RESEARCH_LOG.md',A/'PREPRINT_READINESS.json',R/'problems/20000450_pentagonal_torsion/preprint/READINESS.json']
owned.extend(A/n for n in ['ROOT_PREPRINT02_PHASE2_TRANSFER_CHECK.json','ROOT_PREPRINT02_FAMILIES_GATE.json','root_bind_preprint02_families.py','publication/TRACKER_READ_ONLY_PREFLIGHT.json','publication/preflight_tracker_read.py'])
paths={str(p.relative_to(R)) for p in owned};allow=P/(name+'_allowlist.json');paths.add(str(allow.relative_to(R)))
for p in paths-{str(allow.relative_to(R))}:assert (R/p).is_file() and not (R/p).is_symlink()
def foreign():
    entries={};bodies={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,p=item.split(b'\t',1)
            if p.decode() not in paths:entries.setdefault(p,[]).append(meta)
    for p in git('diff','--name-only','-z').split(b'\0'):
        if p and p.decode() not in paths:
            q=R/p.decode();bodies[p]=(q.exists(),q.read_bytes() if q.is_file() else None,q.stat().st_mode&0o7777 if q.exists() else None)
    return entries,bodies
before=foreign()
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=True,descending_329_workflow_percent=73,descending_checkpoint_scope='PR329 fresh review02 geometry/kernel held and eight root independent full-output replays bound; whole successor adversary active, no publication clearance.',descending_329_review02_geometry_kernel_externally_closed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
j=load(P/'inventory.json');row=next(x for x in j['items'] if x['number']==329);row.update(workflow_percent=73,audit_workflow_percent=73,preprint_review_02_geometry_kernel_complete=True,preprint_review_02_geometry_kernel_externally_closed=True,preprint_review_02_full_packet_active=True,preprint_ready=False,publication_ready=False)
(P/'inventory.json').write_text(json.dumps(j,indent=2)+'\n')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),mathematical_percent=100,priority_percent=100,workflow_percent=73,scope='Externally bound fresh geometry/kernel families and eight root scientific replays; later historical stdout transfer binding and safe read-only tracker preflight. Active parent reviewer namespace/private raw evidence excluded. No approval/merge/publication/tracker mutation.'),indent=2)+'\n')
for phase,argv in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Checkpoint PR329 fresh geometry and torsion review with root reproductions','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    window();start=utc();(P/(name+'_'+phase+'_preexecution.json')).write_text(json.dumps(dict(utc=start,argv=argv,orchestrator_sha256=sha(Path(__file__).read_bytes())),indent=2)+'\n')
    run=subprocess.run(argv,cwd=R,capture_output=True)
    for stream,b in [('stdout',run.stdout),('stderr',run.stderr)]:(P/(name+'_'+phase+'.'+stream)).write_bytes(b)
    (P/(name+'_'+phase+'.json')).write_text(json.dumps(dict(argv=argv,started_utc=start,ended_utc=utc(),exit_code=run.returncode,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr)),indent=2)+'\n')
    assert run.returncode==0,(phase,run.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())
assert changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for p in paths:
    q=R/p;assert git('show',commit+':'+p)==q.read_bytes()
    assert git('ls-tree',commit,'--',p).decode().split()[0]==('100755' if q.stat().st_mode&0o111 else '100644')
assert not git('diff','--cached','--raw','-z') and foreign()==before
receipt=dict(utc=utc(),status='PASS_PR329_FRESH_SECOND_REVIEW_FAMILY_CHECKPOINT_PUSHED',parent=parent,commit=commit,changed_owned_paths=len(changed),allowlist_paths=len(paths),all_allowlisted_Git_disk_bytes_modes_equal=True,remote_main_exact=True,entire_index_empty=True,foreign_index_dirty_bodies_modes_preserved=True,mathematical_verification_percent=100,priority_percent=100,workflow_percent=73,review01_complete=True,review02_complete=False,publication_clearance=False,persistent_goal_complete=False)
(P/(name+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True);(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR329 fresh second-review family checkpoint pushed '+commit+'. Exact scoped Git/disk bytes/modes and remote main; foreign index/dirty tracked state preserved. Math100%, bounded priority100%, workflow73%; full successor adversary active, publication pending.\n')
print(json.dumps(receipt,indent=2))
