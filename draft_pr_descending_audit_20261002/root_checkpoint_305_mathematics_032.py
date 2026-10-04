"""Publish only the PR305 mathematical checkpoint, preserving foreign Git state."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,os,stat,subprocess,fcntl
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr305_5100034';B=P/'audits/pr311_30005303'
sys.path.insert(0,str(B));sys.path.insert(0,str(P))
from root_submission_gate import current_clearance,operational_clearance,pin,sha,utc,load
from root_checkpoint_tree_guard import live_pins,staged_tree,committed_tree
NAME='checkpoint_305_mathematics_032';TOKEN='dd8a3816-588a-4873-a0c5-daf812b24b07'
def window():
    s=load(P/'SHARED_GIT_WINDOW_STATUS.json');assert not s['shared_git_writes_paused']
    assert s['descending_active_pr']==s['descending_acceptance_pr']==305
    e=s['descending_shared_write_lease'];assert e['owner_thread']=='01a0ff30-7e80-7053-abb4-4a9c45f2fd62' and e['pr']==305 and e['token']==TOKEN
    assert e['peer_readonly_release_verified'] and e['cooperative_exclusive_window']
    assert pin(P/e['release_verification_path'])==e['release_verification']
window()
fd=os.open(B/'root_integration_private/SHARED_WRITE_LEASE.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
hold=os.fdopen(fd,'r+b');fcntl.flock(hold,fcntl.LOCK_EX|fcntl.LOCK_NB);window()
current_clearance();operational_clearance()
accepted=load(A/'ROOT_MATHEMATICAL_ACCEPTANCE.json');assert accepted['status']=='PASS_CORRECTED_DISPLAYED_EQUALITY_PROVED_AND_PHASE_CONSTANCY_DISPROVED'
assert accepted['unresolved_mathematical_findings']==0 and accepted['bounded_priority_percent']==0 and not accepted['publishing_clearance']
assert pin(A/'ROOT_MATHEMATICAL_AUDIT.md')==accepted['root_report']
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=True,descending_checkpoint_scope='Publish PR305 complete mathematical audit and exact constancy correction; priority pending. Scope excludes active priority-family namespaces and all third-party full-source files.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def git(*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
parent=git('rev-parse','HEAD').decode().strip();assert parent=='f203c604c8db564423fbd3f6b5f367580745b9f2'
assert git('branch','--show-current')==b'main\n' and git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
assert not git('diff','--cached','--raw','-z')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','checkpoint_311_completed_publication_031_receipt.json',Path(__file__).name]]
files+=[B/'ROOT_SHARED_PR80_CHECKPOINT_RELEASE_VERIFICATION.json']
files+=[A/n for n in ['README.md','RESEARCH_LOG.md','snapshot_manifest.json','INDEPENDENT_FAMILIES_CRITERIA_CUSTODY.json','ROOT_PRIMARY_DEPENDENCY_INPUT_CUSTODY.json','ROOT_PRIMARY_EXTRACTION_RECEIPT.json','ROOT_IMPORTED_RECORD_AUTHENTICATION.json','ROOT_FAMILY_SEAL_AUTHENTICATION.json','ROOT_MATHEMATICAL_AUDIT.md','ROOT_MATHEMATICAL_ACCEPTANCE.json','root_run.py','freeze_original_claimed_source.py','freeze_original_claimed_source_initial_prefix_assumption_failed.py','fetch_primary_and_dependency_inputs.py','root_extract_primary_sources.py','root_authenticate_imported_record.py','root_authenticate_families.py','root_record_mathematical_acceptance.py']]
family_public={
 'meromorphic_family_20261004':['CRITERIA_FROZEN.md','criteria_freeze.json','SOURCE_TARGET_ROUTE_FROZEN.md','source_route_freeze.json','LOCAL_ANALYSIS_FROZEN.md','local_analysis_freeze.json','REPORT.md','research_log.md','CLOSURE.md','ARTIFACT_SEAL.json','SEAL_RUN.json','independent_controls_frozen.py','independent_controls_run.json','independent_exact_complex_checks.py','independent_exact_complex_checks.capture.json','independent_exact_complex_checks.stdout','independent_exact_complex_checks.stderr','independent_extended_program_freeze.json'],
 'source_fidelity_family_20261004':['INDEPENDENT_CRITERIA.md','CRITERIA_FREEZE.json','SOURCE_ONLY_FREEZE.md','SOURCE_ONLY_FREEZE.json','INDEPENDENT_DERIVATION.md','INDEPENDENT_ANALYSIS_FREEZE.json','FINAL_REPORT.md','RESEARCH_LOG.md','NO_MORE_WRITES_CLOSURE.json','ARTIFACT_SEAL.json','ENVIRONMENT.json','independent_triangle_control.py','independent_triangle_control.execution.json','independent_triangle_control.stdout.txt','independent_triangle_control.stderr.txt','independent_symbolic_control.py','independent_symbolic_control.execution.json','independent_symbolic_control.stdout.txt','independent_symbolic_control.stderr.txt'],
 'geometric_family_20261004':['CRITERIA.md','CRITERIA_FREEZE.json','SOURCE_TARGET_ROUTE.md','SOURCE_TARGET_FREEZE.json','INDEPENDENT_DERIVATIONS.md','INDEPENDENT_FREEZE.json','REPORT.md','RESEARCH_LOG.md','CLOSURE.json','MANIFEST.json','SEAL_OPERATION.run.json','SEAL_OPERATION.stdout','SEAL_OPERATION.stderr','exact_triangle.py','exact_triangle_results.json','independent_billiard.py','independent_billiard_results.json','candidate_exact_and_symbolic.py','candidate_exact_and_symbolic_results.json','canonical_vs_direct.py','canonical_vs_direct_results.json','stored_geometry_crosschecks.py','stored_geometry_crosschecks_results.json','21_runtime_provenance.run.json','21_runtime_provenance.stdout','21_runtime_provenance.stderr']}
for folder,names in family_public.items():files+=[A/folder/n for n in names]
allow=P/(NAME+'_allowlist.json');paths={str(p.relative_to(R)) for p in files}|{str(allow.relative_to(R))}
assert len(files)==len(set(files)) and all(p.is_file() and not p.is_symlink() for p in files)
assert all('/priority_' not in n and '/root_sources_private/' not in n and '/root_imported_record_private/' not in n and '/root_primary_extractions_private/' not in n and (not n.endswith(('.pdf','.png','.txt')) or n.endswith(('.stdout.txt','.stderr.txt'))) for n in paths)
def foreign():
    idx={};bodies={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,path=item.split(b'\t',1)
            if path.decode() not in paths:idx.setdefault(path,[]).append(meta)
    for b in git('diff','--name-only','-z').split(b'\0'):
        if b and b.decode() not in paths:
            p=R/b.decode();bodies[b]=(p.exists(),p.read_bytes() if p.is_file() else None,stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
    return idx,bodies
before=foreign();index=git('ls-files','--stage','-z');(D/'entire_index_before.bin').write_bytes(index)
bodypins={}
for n,(exists,b,mode) in before[1].items():
    e={'exists':exists,'mode':mode,'bytes':None,'sha256':None,'body_file':None}
    if b is not None:
        name=sha(n)+'.body';(D/name).write_bytes(b);e.update(bytes=len(b),sha256=sha(b),body_file=name)
    bodypins[n.decode()]=e
(D/'foreign_baseline.json').write_text(json.dumps({'utc':utc(),'entire_index_bytes':len(index),'entire_index_sha256':sha(index),'dirty_foreign_bodies':bodypins},indent=2)+'\n')
selected={str(p.relative_to(R)):pin(p) for p in files}
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'pins':selected,'math_percent':100,'bounded_priority_percent':0,'workflow_percent':30,'goal_complete':False,'no_third_party_full_sources_or_active_agent_artifacts':True},indent=2)+'\n')
expected=dict(selected);expected[str(allow.relative_to(R))]=pin(allow)
(D/'frozen_selected_pins.json').write_text(json.dumps(expected,indent=2)+'\n')
staged=None;commit=None
for phase in ['stage','commit','advance_main','push']:
    window();assert foreign()==before;live_pins(R,expected)
    assert git('branch','--show-current')==b'main\n' and git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
    assert git('rev-parse','HEAD').decode().strip()==(commit if phase=='push' else parent)
    if phase=='stage':
        assert not git('diff','--cached','--raw','-z');args=['/usr/bin/git','add','--',*sorted(paths)]
    if phase=='commit':
        assert staged_tree(git,parent,expected)==staged;args=['/usr/bin/git','commit-tree',staged,'-p',parent,'-m','Audit PR305 focal-pedal equality and exact phase-constancy counterexample']
    if phase=='advance_main':
        assert staged_tree(git,parent,expected)==staged;committed_tree(git,commit,parent,staged,expected)
        args=['/usr/bin/git','update-ref','refs/heads/main',commit,parent]
    if phase=='push':
        committed_tree(git,commit,parent,staged,expected);current_clearance();operational_clearance()
        args=['/usr/bin/git','push','--force-with-lease=refs/heads/main:'+parent,'origin',commit+':refs/heads/main']
    rec={'argv':args,'cwd':str(R),'started_utc':utc(),'operator_sha256':sha(Path(__file__).read_bytes())}
    (D/(phase+'_preexecution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    run=subprocess.run(args,cwd=R,capture_output=True)
    for key,b in [('stdout',run.stdout),('stderr',run.stderr)]:(D/(phase+'.'+key)).write_bytes(b)
    rec.update(ended_utc=utc(),exit_code=run.returncode,stdout_bytes=len(run.stdout),stderr_bytes=len(run.stderr),stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr))
    (D/(phase+'_execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    assert run.returncode==0 and foreign()==before;live_pins(R,expected)
    if phase=='stage':staged=staged_tree(git,parent,expected)
    if phase=='commit':
        commit=run.stdout.decode().strip();assert len(commit)==40 and all(c in '0123456789abcdef' for c in commit)
        committed_tree(git,commit,parent,staged,expected)
    if phase=='advance_main':assert git('rev-parse','HEAD').decode().strip()==commit and not git('diff','--cached','--raw','-z')
assert git('rev-parse','HEAD').decode().strip()==commit and git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
committed_tree(git,commit,parent,staged,expected);assert foreign()==before and not git('diff','--cached','--raw','-z')
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
receipt={'utc':utc(),'status':'PASS_PR305_MATHEMATICAL_CHECKPOINT_SCOPED_AND_PUSHED','parent':parent,'commit':commit,'tree':staged,'changed_paths':len(changed),'allowlist_paths':len(paths),'exact_scoped_live_staged_committed_pins_verified':True,'foreign_entire_index_entries_dirty_bytes_and_modes_preserved':True,'entire_index_empty':True,'actual_parent_verified_fast_forward_remote_lease':True,'remote_main_exact':True,'math_percent':100,'bounded_priority_percent':0,'workflow_percent':30,'goal_complete':False}
(P/(NAME+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True);(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
