"""Publish only the PR305 bounded-priority progress checkpoint; preserve foreign Git state."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,os,stat,subprocess,fcntl
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr305_5100034';B=P/'audits/pr311_30005303'
sys.path.insert(0,str(B));sys.path.insert(0,str(P))
from root_submission_gate import current_clearance,operational_clearance,pin,sha,utc,load
from root_checkpoint_tree_guard import live_pins,staged_tree,committed_tree
NAME='checkpoint_305_priority_routes_034';TOKEN='dd8a3816-588a-4873-a0c5-daf812b24b07'
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
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=True,descending_checkpoint_scope='Two historical families closed and authenticated; classical implications and fresh ROOT controls retained. New triangle adversary active, no integrated priority/paper/merge/publication clearance.',descending_305_bounded_priority_percent=85,descending_305_workflow_percent=40)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def git(*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
parent=git('rev-parse','HEAD').decode().strip();assert parent=='74ed422e0f5716d10c51e5b8ced380d82bfab7cd'
assert git('branch','--show-current')==b'main\n' and git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
assert not git('diff','--cached','--raw','-z')
recent=load(A/'ROOT_PRIORITY_RECENT_ROUTE_SEAL.json');assert recent['status']=='PASS_ROOT_RECENT_ROUTE_CLOSED_NO_FINAL_PRIORITY_CLEARANCE' and not recent['final_priority_clearance']
assert pin(A/'ROOT_PRIORITY_RECENT_COMPARISON.md')==recent['report']
inv=load(P/'inventory.json');before_items={x['number']:dict(x) for x in inv['items']};before_count=inv['completed_by_descending']
item=next(x for x in inv['items'] if x['number']==305);assert item['submitted_status']=='claimed_solved' and item['original_author_turn_count']=='1/5'
item.update(bounded_priority_percent=85,workflow_percent=40)
assert all(x==before_items[x['number']] for x in inv['items'] if x['number']!=305) and inv['completed_by_descending']==before_count
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n- '+utc()+' — PR305 two independent historical routes closed, fully read and authenticated; every final file/mode/native capture checked and exact controls freshly reproduced. Phase-constancy failure follows old signed-triangle/Fierobe results. ROOT restricted triangular E/M old-results implication is under a NEW targeted adversary. No full-domain prior E/M proof located in inspected sources; even E and generic complex methods are old. Six unavailable final editions and finite coverage disclosed. No integrated priority/paper/merge/publication clearance. Math100%,bounded priority85%,workflow40%; persistent goal active.\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+utc()+' — Closed historical-route checkpoint; math100%,bounded priority85%,workflow40%\n\nBoth independent priority routes were closed, fully read and authenticated by ROOT. Fresh general and focal controls pass. Exact old-results implications for negative constancy and restricted triangular E/M are recorded, the latter awaiting a NEW adversarial report. No integrated priority or paper/publication clearance. Known-held-file inventory is a dated snapshot only, not a peer writer ACK. Persistent descending goal remains active.\n')
readme=A/'README.md';body=readme.read_text();body+='\nCurrent historical-route checkpoint: two independent routes closed and ROOT-authenticated. Classical negative-constancy implication verified; restricted N3 equality/multiplier old-results implication under new targeted adversary. Mathematics100%; bounded priority85%; PR workflow40%. No integrated priority or publication clearance.\n';readme.write_text(body)
files=[P/n for n in ['RESEARCH_LOG.md', 'SHARED_GIT_WINDOW_STATUS.json', 'inventory.json', 'checkpoint_305_priority_progress_033_receipt.json', 'KNOWN_HELD_FILES_FOR_FUTURE_PEER_WINDOW_305.json', 'root_known_held_inventory_305.py', 'root_prepare_checkpoint034.py']]+[Path(__file__).resolve()]
files+=[A/n for n in ['README.md', 'RESEARCH_LOG.md', 'ROOT_CLASSICAL_NONCONSTANCY_ACQUISITION.json', 'ROOT_CLASSICAL_NONCONSTANCY_COROLLARY.md', 'ROOT_CLASSICAL_NONCONSTANCY_SEAL.json', 'ROOT_PRIORITY_GENERAL_CUSTODY.json', 'ROOT_PRIORITY_FOCAL_CUSTODY.json', 'ROOT_TRIANGULAR_OLD_IMPLICATION.md', 'root_fetch_classical_nonconstancy.py', 'root_fetch_classical_nonconstancy_v02.py', 'root_check_classical_triangle_formula.py', 'root_check_classical_triangle_formula_v02.py', 'root_seal_classical_priority.py', 'root_authenticate_priority_general.py', 'root_authenticate_priority_focal.py', 'root_triangle_priority_bridge.py', 'root_triangle_priority_bridge_v02.py']]
for family,names in {'priority_general_20261004': ['CRITERIA_FREEZE.md', 'FULL_PRIORITY_REPORT.md', 'DERIVATIONS.md', 'SOURCE_READ_LEDGER.md', 'SELF_REVIEW.md', 'STOP_WRITING.md', 'NATIVE_SOURCE_REGISTRY.json', 'SOURCE_SEAL.json', 'SOURCE_SEAL.sha256', 'check_bridges.py', 'source_custody.py', 'validate_custody.py', 'seal_audit.py', 'RESEARCH_LOG.md'], 'priority_focal_20261004': ['FROZEN_ACCEPTANCE_CRITERIA.md', 'CRITERIA_FREEZE.json', 'FOCAL_PRIORITY_COMPARISON.md', 'SEARCH_TRAIL.md', 'SOURCE_CUSTODY.json', 'CLAIM_COMPARISON.json', 'FINAL_SELF_CHECK.md', 'CLOSURE.json', 'FINAL_SEAL.json', 'classical_boundary_control.py', 'classical_boundary_control_initial.py', 'run_custody.py', 'verify_custody.py', 'seal_audit.py', 'build_metadata.py', 'RESEARCH_LOG.md']}.items(): files+=[A/family/n for n in names]
for label in ['root_classical_nonconstancy_sources_actual001', 'root_classical_nonconstancy_sources_actual002', 'root_querret_primary_page283_actual001', 'root_classical_triangle_formula_actual001', 'root_classical_triangle_formula_actual002', 'root_classical_priority_seal_actual001', 'root_priority_general_custody_actual001', 'root_priority_general_bridge_actual001', 'root_known_held_inventory_actual001', 'root_triangle_priority_algebra_actual001', 'root_triangle_priority_algebra_actual002', 'root_priority_focal_custody_actual001', 'root_priority_focal_control_actual001', 'root_priority_focal_verifier_actual001', 'root_priority_v1_table_render_actual001']:
 files+=[A/'root_runs_private'/label/n for n in ['execution_spec.json','execution.json','stdout.bin','stderr.bin']]
allow=P/(NAME+'_allowlist.json');paths={str(p.relative_to(R)) for p in files}|{str(allow.relative_to(R))}
assert len(files)==len(set(files)) and all(p.is_file() and not p.is_symlink() for p in files)
assert all('/sources_private/' not in n and '/root_sources_private/' not in n and '/root_priority_recent_private/' not in n and '/root_priority_current_private/' not in n and '/root_classical_nonconstancy_private' not in n and '/root_priority_triangular_private/' not in n and '/triangle_priority_adversary_20261005/' not in n and not n.endswith(('.pdf','.png','.txt')) for n in paths)
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
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'pins':selected,'math_percent':100,'bounded_priority_percent':85,'workflow_percent':40,'goal_complete':False,'no_third_party_full_sources_or_active_agent_artifacts':True},indent=2)+'\n')
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
        assert staged_tree(git,parent,expected)==staged;args=['/usr/bin/git','commit-tree',staged,'-p',parent,'-m','Record PR305 closed historical routes and classical implications']
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
receipt={'utc':utc(),'status':'PASS_PR305_PRIORITY_PROGRESS_CHECKPOINT_SCOPED_AND_PUSHED','parent':parent,'commit':commit,'tree':staged,'changed_paths':len(changed),'allowlist_paths':len(paths),'exact_scoped_live_staged_committed_pins_verified':True,'foreign_entire_index_entries_dirty_bytes_and_modes_preserved':True,'entire_index_empty':True,'actual_parent_verified_fast_forward_remote_lease':True,'remote_main_exact':True,'math_percent':100,'bounded_priority_percent':85,'workflow_percent':40,'goal_complete':False}
(P/(NAME+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True);(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
