"""Commit only PR329 actual publication facts; preserve the shared index/worktree."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr329_20000450'
name='checkpoint_329_completion_017'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def git(*args):return subprocess.check_output(['git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(name+'_receipt.json')).exists() and not (P/(name+'_stage.json')).exists()
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance
current_clearance();window()
status=load(A/'CURRENT_PUBLICATION_STATUS.json')
assert status['status']=='MERGED_PUBLISHED_AND_TRACKER_VERIFIED' and status['workflow_completion_percent']==100
assert status['doi']=='10.5281/zenodo.23137834'
assert load(A/'publication/TRACKER_COMPLETE.json')['updatedRange']=="'Math Puzzles'!A21:D21"
parent=git('rev-parse','HEAD').decode().strip()
assert parent=='d72c77fdb98ba32aebef7a6e8351dcc4d6645d81'
assert git('branch','--show-current')==b'main\n'
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
assert not git('diff','--cached','--raw','-z') and not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
owned=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','checkpoint_329_acceptance_016_receipt.json',Path(__file__).name]]
owned.extend(A/n for n in ['RESEARCH_LOG.md','PREPRINT_READINESS.json','CURRENT_PUBLICATION_STATUS.json',
    'ACTUAL_MERGE_ATTEMPT.json','ACTUAL_MERGE_VERIFICATION.json','BRANCH_REFRESH_ATTEMPT.json',
    'ROOT_EXACT_LIVE_PREMERGE.json','ROOT_POST_MERGE_VERIFICATION.json','repaired_snapshot_manifest.json',
    'queue_repair_receipt.json','queue_publication_receipt.json','root_record_publication_completion.py',
    'published_pr_body.txt','published_pr_body_update_preexecution.json'])
owned.extend(q for q in (A/'publication').iterdir() if q.is_file() and q.suffix in {'.py','.json','.stdout','.stderr'})
owned.extend([R/'unsolved_math_prioritization/QUEUE.md',R/'problems/20000450_pentagonal_torsion/PREPRINT_RELEASE.md'])
owned.extend(R/'problems/20000450_pentagonal_torsion/preprint'/n for n in ['READINESS.json','PUBLICATION_RESULT.json','PUBLICATION.md'])
paths={str(q.relative_to(R)) for q in owned};allow=P/(name+'_allowlist.json');paths.add(str(allow.relative_to(R)))
for rel in paths-{str(allow.relative_to(R))}:
    q=R/rel;assert q.is_file() and not q.is_symlink()
    assert not any(t.startswith('private_') or t.endswith('_private') or t=='__pycache__' for t in q.relative_to(R).parts)
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
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),mathematical_percent=100,priority_percent=100,workflow_percent=100,
    scope='Actual exact PR329 merge, four unchanged cleared files, final clean NEW whole review, production Zenodo record23137834, all11 metadata fields and both complete public downloads exact, DOI200, ONE tracker row21 exact readback, own merged body factual publication update, own queue DOI cell12 only. Raw private/API/whole-sheet/download data and all immutable held reviewers excluded. No release or journal submission; persistent goal active.'),indent=2)+'\n')
for phase,argv in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Record PR329 verified preprint DOI and tracker publication completion','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    window();assert foreign()==before
    start=utc();(P/(name+'_'+phase+'_preexecution.json')).write_text(json.dumps(dict(utc=start,argv=argv,orchestrator_sha256=sha(Path(__file__).read_bytes())),indent=2)+'\n')
    run=subprocess.run(argv,cwd=R,capture_output=True)
    for stream,b in [('stdout',run.stdout),('stderr',run.stderr)]:(P/(name+'_'+phase+'.'+stream)).write_bytes(b)
    (P/(name+'_'+phase+'.json')).write_text(json.dumps(dict(argv=argv,started_utc=start,ended_utc=utc(),exit_code=run.returncode,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr)),indent=2)+'\n')
    assert run.returncode==0,(phase,run.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())
assert changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for rel in paths:
    q=R/rel;assert git('show',commit+':'+rel)==q.read_bytes()
    assert git('ls-tree',commit,'--',rel).decode().split()[0]==('100755' if q.stat().st_mode&0o111 else '100644')
assert not git('diff','--cached','--raw','-z') and foreign()==before
current_clearance()
receipt=dict(utc=utc(),status='PASS_PR329_COMPLETION_CHECKPOINT_PUSHED',parent=parent,commit=commit,
    changed_owned_paths=len(changed),allowlist_paths=len(paths),all_allowlisted_Git_disk_bytes_modes_equal=True,
    remote_main_exact=True,entire_index_empty=True,foreign_index_dirty_bodies_modes_preserved=True,
    mathematical_verification_percent=100,priority_percent=100,workflow_percent=100,doi=status['doi'],
    tracker_range=status['tracker_range'],actual_merge=status['actual_merge'],persistent_goal_complete=False)
(P/(name+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,
    descending_final_acceptance_preparing=False,last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR329 completion checkpoint pushed '+commit+'. All scoped Git/disk bytes/modes and remote exact, foreign index/dirty tracked bodies/modes preserved; math100%, bounded priority100%, PR329 workflow100%. DOI10.5281/zenodo.23137834, tracker A21:D21. Goal active; descending next eligible intake.\n')
print(json.dumps(receipt,indent=2))
