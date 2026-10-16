"""Publish source-first PR316 intake and root checks, excluding active family work."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr316_9900002'
name='checkpoint_316_initial_018';utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda q:json.loads(q.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(name+'_receipt.json')).exists() and not (P/(name+'_stage.json')).exists()
window();parent=git('rev-parse','HEAD').decode().strip();assert parent=='c04bff19bc3ba481c4babd5cba8575aa4b4cbdb8'
assert git('branch','--show-current')==b'main\n'
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
assert not git('diff','--cached','--raw','-z') and not git('diff','--name-only','--diff-filter=U')
assert load(A/'ROOT_INITIAL_INPUT_BINDINGS.json')['status']=='PASS_CURRENT_PR316_ORIGINAL_GIT_API_MANIFEST_RAW_SOURCE_AND_TWO_REPLAY_BINDINGS'
assert load(P/'STATUS_FILTER_LEDGER.json')['next_eligible']['number']==316
stamp=utc()
scope=load(P/'CURRENT_SCOPE.json');scope.update(utc=stamp,scope='Process only submitted QUEUE.md status exactly claimed_solved; skip every other status entirely and PR8; descending current316.',current_eligible_pr=316,current_original_head='c96a3b2019ed3d6aabe0612b31491161dcb275e8',current_original_status='claimed_solved')
(P/'CURRENT_SCOPE.json').write_text(json.dumps(scope,indent=2)+'\n')
inv=load(P/'inventory.json');row=next(x for x in inv['items'] if x['number']==316)
row.update(workflow_percent=15,audit_workflow_percent=15,mathematical_verification_percent=45,
    mathematical_acceptance=False,priority_acceptance=False,publication_ready=False,
    root_original_replay_assertions=[7852,646],root_independent_geometric_checks=6124,
    fresh_mathematical_families=['renewal_probability','normalization_limits'],full_primary_binary_access_pending=True)
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=stamp,descending_active_pr=316,
    descending_316_workflow_percent=15,descending_316_mathematical_verification_percent=45,
    descending_git_checkpoint_preparing=True,descending_checkpoint_scope='PR316 source-first original19-file object/source bindings and initial root mathematical deductions/replays; two fresh families active and excluded. No mathematical/priority/preprint/merge/publication acceptance. PR329 complete DOI/tracker receipt retained.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
(A/'README.md').write_text('# Descending adversarial audit: PR316 / 9900002\n\nOriginal submitted head c96a3b2019ed3d6aabe0612b31491161dcb275e8, claimed_solved, author1/5. All19 changed objects (18 target files) match live API, Git and frozen disk bytes/modes. Imported full target and prior report match both complete pinned raw source files. Root read the complete submitted proof/verification/historical record after source-first criteria, reproduced7852/646 checks and independently derived a geometric-count concentration bound with6124 checks/three genuine false variants rejected.\n\nRoot initial mathematical verification45%, PR316 workflow15%; both fresh source-first independent families are active. Mathematical acceptance, current priority audit, paper, exact merge and publication remain pending. Full original primary PDF binary/visual access remains unavailable; current indexed institutional source hypotheses and Problem1.2 match the imported target. A historical Angus–Ding article-number typo requires correction in current publication prose, not alteration of the original18 files. No external individual contacted; goal active.\n')
log=stamp+' — PR316 initial meaningful checkpoint: full19-file original API/Git/disk and8/17/5 manifest bindings, complete pinned raw datasets/unique problem and report join/current imported payload authenticated; both original native full checker outputs exact (7852/646). Root full proof review and independent geometric-count bound with6124 exact checks/2688 toy crossing cases/three genuine false-claim controls pass. Fresh probability and normalization families source-first and first-candidate assessments independently read/bound before code release; final reports remain active. Full primary binary still inaccessible; historical source article-number typo recorded for current-prose correction. Math45%, workflow15%; no acceptance, priority, preprint, merge or publication for316; author1/5 and historical18 files preserved. PR329 complete DOI10.5281/zenodo.23137834, sheetrow21, pushed c04bff19bc3ba481c4babd5cba8575aa4b4cbdb8.\n'
for q in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with q.open('a') as f:f.write('\n'+log)
owned=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','CURRENT_SCOPE.json','STATUS_FILTER_LEDGER.json','checkpoint_329_completion_017_receipt.json',Path(__file__).name]]
owned.extend(A/n for n in ['README.md','RESEARCH_LOG.md','snapshot_manifest.json','SOURCE_FIRST_CRITERIA.md',
    'SOURCE_FIRST_BASELINE.json','ROOT_SOURCE_INTAKE.json','ROOT_RENEWAL_SOURCE_GATE.json','ROOT_NORMALIZATION_SOURCE_GATE.json',
    'ROOT_RENEWAL_CANDIDATE_GATE.json','ROOT_NORMALIZATION_CANDIDATE_GATE.json','ROOT_INITIAL_MATHEMATICAL_REVIEW.md',
    'ROOT_INITIAL_INPUT_BINDINGS.json','root_run.py','root_source_intake.py','root_authenticate_initial_inputs.py','root_geometric_crossing_checks.py'])
owned.extend(q for q in (A/'snapshot').rglob('*') if q.is_file())
# Only already-held early assessments are included. Active reports/code/native directories excluded.
for family,gate in [('renewal_probability','ROOT_RENEWAL_SOURCE_GATE.json'),('normalization_limits','ROOT_NORMALIZATION_SOURCE_GATE.json'),('renewal_probability','ROOT_RENEWAL_CANDIDATE_GATE.json'),('normalization_limits','ROOT_NORMALIZATION_CANDIDATE_GATE.json')]:
    for n,e in load(A/gate)['held_files'].items():
        q=A/family/n;assert sha(q.read_bytes())==e['sha256'] and oct(q.stat().st_mode&0o7777)==e['mode'];owned.append(q)
paths={str(q.relative_to(R)) for q in owned};allow=P/(name+'_allowlist.json');paths.add(str(allow.relative_to(R)))
for rel in paths-{str(allow.relative_to(R))}:assert (R/rel).is_file() and not (R/rel).is_symlink()
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
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),mathematical_percent=45,workflow_percent=15,
    scope='Source-first early immutable families, root initial deductions/code and original19-file frozen object/manifest/source authentication. Full primary/source import/raw API/Git/private execution data excluded. Both active final family reports and code excluded; no acceptance/priority/paper/merge/publication for316.'),indent=2)+'\n')
for phase,argv in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Audit PR316 source quantifiers and independently reproduce renewal concentration','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    window();assert foreign()==before;t=utc()
    (P/(name+'_'+phase+'_preexecution.json')).write_text(json.dumps(dict(utc=t,argv=argv,orchestrator_sha256=sha(Path(__file__).read_bytes())),indent=2)+'\n')
    q=subprocess.run(argv,cwd=R,capture_output=True)
    for stream,b in [('stdout',q.stdout),('stderr',q.stderr)]:(P/(name+'_'+phase+'.'+stream)).write_bytes(b)
    (P/(name+'_'+phase+'.json')).write_text(json.dumps(dict(argv=argv,started_utc=t,ended_utc=utc(),exit_code=q.returncode,stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr)),indent=2)+'\n')
    assert q.returncode==0,(phase,q.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())
assert changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for rel in paths:
    q=R/rel;assert git('show',commit+':'+rel)==q.read_bytes()
    assert git('ls-tree',commit,'--',rel).decode().split()[0]==('100755' if q.stat().st_mode&0o111 else '100644')
assert not git('diff','--cached','--raw','-z') and foreign()==before
j=dict(utc=utc(),status='PASS_PR316_INITIAL_SOURCE_FIRST_MATHEMATICAL_CHECKPOINT_PUSHED',parent=parent,commit=commit,
    changed_owned_paths=len(changed),allowlist_paths=len(paths),all_allowlisted_Git_disk_bytes_modes_equal=True,
    remote_main_exact=True,entire_index_empty=True,foreign_index_dirty_bodies_modes_preserved=True,
    mathematical_verification_percent=45,workflow_percent=15,active_families_excluded=True,
    mathematical_acceptance=False,priority_acceptance=False,publication_ready=False,persistent_goal_complete=False)
(P/(name+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR316 initial source-first mathematical checkpoint pushed '+commit+'. Scoped Git/disk bytes/modes and remote exact; all foreign index/dirty tracked bodies/modes preserved. Math45%, workflow15%; fresh families active and excluded, original1/5 unchanged, no acceptance or publication. Goal active.\n')
print(json.dumps(j,indent=2))
