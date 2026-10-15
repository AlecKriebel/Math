"""Publish qualified PR329 proof package and bounded priority, preserving foreign state."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr329_20000450'
PREFIX='checkpoint_329_preprint_010'
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(PREFIX+'_receipt.json')).exists() and not (P/(PREFIX+'_stage.json')).exists()
assert load(A/'ROOT_LOCAL_GIT_VERIFICATION.json')['status']=='PASS_COMPLETE_PR329_LOCAL_GIT_DIFF_BLOBS_MODES_MATCH_FROZEN_API'
paths=set()
def add(p):
    assert p.is_file() and not p.is_symlink() and (p.resolve().is_relative_to(P) or p.resolve().is_relative_to(R/'problems/20000450_pentagonal_torsion/preprint'))
    assert not any(part.startswith('private_') or part.endswith('_private') or part in {'__pycache__','.runtime'} for part in p.relative_to(R).parts)
    paths.add(str(p.relative_to(R)))
for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','STATUS_FILTER_LEDGER.json',
          'checkpoint_329_math_008_receipt.json','checkpoint_329_preprint_009_receipt.json','root_provisional_math_329.py','root_record_math_gate_329.py','root_record_preprint_progress_329.py',Path(__file__).name]:add(P/n)
for p in A.iterdir():
    if p.is_file() and not p.name.startswith('.'):add(p)
for family,names in {
    'geometry':['geometry_report.md','validate_candidate_geometry.py','independent_source_geometry.py','independent_quotient_geometry.py'],
    'division_polynomial':['REPORT.md','independent_chord.py','independent_model.py','independent_finite.py','independent_quintic_factors.py','verify_review.py','OWNED_NAMESPACE_MANIFEST.json','FINAL_PINS.json'],
    'arithmetic':['REPORT.md','check_arithmetic.py','verify_readonly.py','replay_controls.py','capture.py','build_manifest.py','prepare_bindings.py','MANIFEST.json']
}.items():
    for name in names:add(A/family/name)
for p in sorted((A/'preprint').rglob('*')):
    if p.is_file():add(p)
for p in sorted((R/'problems/20000450_pentagonal_torsion/preprint').iterdir()):
    if p.is_file():add(p)
assert load(A/'ROOT_CURRENT_MATHEMATICAL_GATE.json')['status']=='PASS_ROOT_CURRENT_COMPLETE_MATHEMATICAL_GATE_PR329'
assert load(A/'ROOT_PRIORITY_CLOSURE.json')['status']=='PASS_ROOT_EXTERNALLY_CLOSED_PRIORITY_AUDIT_PR329'
Q=A/'preprint/qualification_v02';qualification=load(Q/'QUALIFICATION.json')
assert qualification['status']=='NATIVELY_QUALIFIED_FOR_FRESH_ADVERSARIAL_REVIEW' and qualification['input_count']==8
assert not qualification['preprint_ready'] and not qualification['publication_ready']
for name,record in qualification['inputs'].items():
    b=(Q/'inputs'/name).read_bytes();assert len(b)==record['bytes'] and sha(b)==record['sha256'] and (R/record['original_path']).read_bytes()==b
for name in ['independent_derivation_frozen.md','primitivity_report.md','verify_primitivity.py','namespace_inventory.json','requirements.txt']:add(A/'geometry_primitivity'/name)
S=A/'priority_audit/stage3_current_priority'
for row in load(S/'PUBLIC_MANIFEST.json')['payloads']:add(S/row['path'])
for name in ['PUBLIC_MANIFEST.json','WHOLE_NAMESPACE_MANIFEST.json','verify_whole_namespace.py','capture_operation.py','retrieve_primary.py','read_scoped.py','render_pages.py','build_ledgers.py','build_final_manifests.py','inspect_final_chronology.py','compare_imported_versions.py']:add(S/name)
for name in ['SOURCE_ONLY_FREEZE.json','verify_source_only.py','stage2_candidate_exposure/FIRST_CANDIDATE_FREEZE.json']:add(A/'priority_audit'/name)
now=utc()
ready=dict(utc=now,status='NATIVELY_QUALIFIED_FOR_FRESH_ADVERSARIAL_REVIEW',mathematical_verification_percent=100,priority_percent=100,workflow_percent=60,priority_complete=True,preprint_ready=False,merged=False,published=False,
    qualification_sha256=sha((Q/'QUALIFICATION.json').read_bytes()),verification_archive_sha256=qualification['inputs']['verification.zip']['sha256'],
    exact_remaining_gates=['Successive fresh independent full-preprint adversarial reviews and global repairs','Exact merge','Production Zenodo publication and DOI tracker append'])
(R/'problems/20000450_pentagonal_torsion/preprint/READINESS.json').write_text(json.dumps(ready,indent=2)+'\n')
p=P/'inventory.json';j=load(p);row=next(x for x in j['items'] if x['number']==329);row.update(workflow_percent=60,audit_workflow_percent=60,preprint_current_qualification='v02',preprint_review_01_started=True,preprint_review_01_agent='/root/pr329_preprint_01');p.write_text(json.dumps(j,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write('\n'+now+' — PR329 current v02 archive qualification PASS:8frozen inputs,50public payloads,11positive programs/4mathematical mutants,9additional integrity/optimization controls and separate public priority verifier; source-bound7pagePDF. New PR329 preprint01 child begins source-only independent baseline before candidate release. Mathematics100%, priority100%, workflow60%; successive full-preprint reviews and publication pending.\n')
window();s=load(P/'SHARED_GIT_WINDOW_STATUS.json')
s.update(utc=utc(),descending_git_checkpoint_preparing=True,
    descending_checkpoint_scope='PR329 externally closed bounded priority, uniform primitivity proof and native-qualified v02 preprint archive; math100%, priority100%, workflow60%; active preprint01/private sources excluded; no final acceptance/publication clearance.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'math_percent':100,'workflow_percent':60,
    'scope':'Qualified source-bound current note, exact metadata and v02 portable archive; complete bounded priority and uniform primitivity addendum externally closed. Math100%, priority100%, workflow60%; successive full-preprint reviews/merge/publication pending. Active preprint01 and private/raw source/runtime excluded.'},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--name-only','--diff-filter=U') and not git('diff','--cached','--raw','-z')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
def foreign():
    entries={};bodies={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,name=item.split(b'\t',1)
            if name.decode() not in paths:entries.setdefault(name,[]).append(meta)
    for name in git('diff','--name-only','-z').split(b'\0'):
        if name and name.decode() not in paths:
            f=R/name.decode();bodies[name]={'exists':f.exists(),'bytes':f.read_bytes() if f.is_file() else None,'mode':f.stat().st_mode&0o7777 if f.exists() else None}
    return entries,bodies
window();before=foreign();parent=git('rev-parse','HEAD').decode().strip()
assert parent=='25aaa7146e257ef5276e80aae60429cf3f4765f9'
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
for label,argv in [('stage',['git','add','-f','--',*sorted(paths)]),
   ('commit',['git','commit','--only','-m','Checkpoint qualified PR329 preprint package and externally verified bounded priority','--',*sorted(paths)]),
   ('push',['git','push','origin','main'])]:
    window();started=utc();(P/(PREFIX+'_'+label+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':argv,'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
    r=subprocess.run(argv,cwd=R,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (P/(PREFIX+'_'+label+'.'+k)).write_bytes(b)
    (P/(PREFIX+'_'+label+'.json')).write_text(json.dumps({'argv':argv,'started_utc':started,'ended_utc':utc(),'exit_code':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)},indent=2)+'\n')
    assert r.returncode==0,(label,r.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for p in paths:
    f=R/p;assert git('show',commit+':'+p)==f.read_bytes()
    mode=git('ls-tree',commit,'--',p).decode().split()[0];assert mode==('100755' if f.stat().st_mode&0o111 else '100644')
assert not git('diff','--cached','--raw','-z')
j={'utc':utc(),'status':'PASS_PR329_QUALIFIED_PREPRINT_CHECKPOINT_PUSHED','parent':parent,'commit':commit,
    'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_Git_disk_bytes_modes_equal':True,
    'remote_main_exact':True,'entire_index_empty':True,'foreign_index_dirty_bodies_modes_preserved':True,
    'mathematical_verification_percent':100,'workflow_percent':60,'priority_complete':True,'preprint_or_publication_clearance':False,'persistent_goal_complete':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True,descending_git_checkpoint_preparing=False,descending_329_workflow_percent=60,descending_329_preprint_review_01_started=True,descending_329_preprint_review_01_agent='/root/pr329_preprint_01')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR329 qualified preprint checkpoint pushed '+commit+'. Foreign index/dirty tracked bodies/modes preserved; remote/main and all scoped bytes/modes exact. Math100%, priority100%, workflow60%; full-preprint reviews/merge/publication remain pending, original1/5 unchanged.\n')
print(json.dumps(j,indent=2))
