"""Checkpoint staged review independence and root replays, preserving foreign state."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess
P=Path(__file__).resolve().parent; R=P.parent; A=P/'audits/pr329_20000450'
name='checkpoint_329_review_011'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def git(*args):
    return subprocess.check_output(['git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():
    assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(name+'_receipt.json')).exists()
window()
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--cached','--raw','-z')
assert not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
parent=git('rev-parse','HEAD').decode().strip()
assert parent=='03c3cc4ee2502f6937185fb55d17e1143fe5b6ea'
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
paths={str(x.relative_to(R)) for x in [P/'RESEARCH_LOG.md',P/'SHARED_GIT_WINDOW_STATUS.json',P/'inventory.json',P/'checkpoint_329_preprint_010_receipt.json',Path(__file__),A/'RESEARCH_LOG.md',A/'ROOT_PREPRINT01_SOURCE_GATE.json',A/'ROOT_PREPRINT01_FIRST_CANDIDATE_GATE.json',A/'ROOT_PREPRINT01_INTERIM_REPLAY.json']}
allow=P/(name+'_allowlist.json'); paths.add(str(allow.relative_to(R)))
for p in paths-{str(allow.relative_to(R))}:
    assert (R/p).is_file() and not (R/p).is_symlink()
def foreign():
    entries={}; bodies={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,p=item.split(b'\t',1)
            if p.decode() not in paths:entries.setdefault(p,[]).append(meta)
    for p in git('diff','--name-only','-z').split(b'\0'):
        if p and p.decode() not in paths:
            q=R/p.decode();bodies[p]=(q.exists(),q.read_bytes() if q.is_file() else None,q.stat().st_mode&0o7777 if q.exists() else None)
    return entries,bodies
before=foreign()
s=load(P/'SHARED_GIT_WINDOW_STATUS.json')
s.update(utc=utc(),descending_git_checkpoint_preparing=True,descending_329_workflow_percent=62,descending_checkpoint_scope='PR329 review01 independently frozen source/candidate stages and six successful root-native replays; complete review still active, minor source attribution correction pending; no merge/publication clearance.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
j=load(P/'inventory.json');row=next(x for x in j['items'] if x['number']==329)
row.update(workflow_percent=62,audit_workflow_percent=62,preprint_review_01_root_independent_replays=6,preprint_review_01_complete=False)
(P/'inventory.json').write_text(json.dumps(j,indent=2)+'\n')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),mathematical_percent=100,priority_percent=100,workflow_percent=62,scope='Staged independent whole-review gates and root-native mathematical replay checkpoint; active reviewer namespace/private evidence excluded; global wording repair and successor review remain.'),indent=2)+'\n')
for phase,argv in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Checkpoint PR329 fresh review independence and root mathematical replays','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    window();start=utc()
    (P/(name+'_'+phase+'_preexecution.json')).write_text(json.dumps(dict(utc=start,argv=argv,orchestrator_sha256=sha(Path(__file__).read_bytes())),indent=2)+'\n')
    run=subprocess.run(argv,cwd=R,capture_output=True)
    for stream,b in [('stdout',run.stdout),('stderr',run.stderr)]: (P/(name+'_'+phase+'.'+stream)).write_bytes(b)
    (P/(name+'_'+phase+'.json')).write_text(json.dumps(dict(argv=argv,started_utc=start,ended_utc=utc(),exit_code=run.returncode,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr)),indent=2)+'\n')
    assert run.returncode==0,(phase,run.stderr.decode(errors='replace'))
    assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())
assert changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for p in paths:
    q=R/p;assert git('show',commit+':'+p)==q.read_bytes()
    assert git('ls-tree',commit,'--',p).decode().split()[0]==('100755' if q.stat().st_mode&0o111 else '100644')
assert not git('diff','--cached','--raw','-z') and foreign()==before
receipt=dict(utc=utc(),status='PASS_PR329_FRESH_REVIEW_PROGRESS_CHECKPOINT_PUSHED',parent=parent,commit=commit,changed_owned_paths=len(changed),allowlist_paths=len(paths),all_allowlisted_Git_disk_bytes_modes_equal=True,remote_main_exact=True,entire_index_empty=True,foreign_index_dirty_bodies_modes_preserved=True,mathematical_verification_percent=100,priority_percent=100,workflow_percent=62,full_preprint_review_complete=False,publication_clearance=False,persistent_goal_complete=False)
(P/(name+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR329 fresh-review progress checkpoint pushed '+commit+'. Scoped Git/disk bytes/modes and remote main exact; foreign index/dirty tracked bodies/modes preserved. Math100%, bounded priority100%, workflow62%; whole review/repair/successor review and merge/publication pending.\n')
print(json.dumps(receipt,indent=2))
