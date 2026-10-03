"""Root checks actual final capture then records fresh post39 main; no imports."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat
import subprocess
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr40_2814';S=A/'acceptance_execution_preparation_family/integration_source_revision_v2';C=A/'root_final_reconciliation_actual_capture';F=A/'final_evidence_reconciliation'
def H(b):return hashlib.sha256(b).hexdigest()
def J(p):return json.loads(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def row(p):
    b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=H(b))
def member(root,z):
    p=root/z['path'];assert p.is_file() and not p.is_symlink();b=p.read_bytes();assert type(z['bytes']) is int and len(b)==z['bytes'] and H(b)==z['sha256'];return b
def write(n,o):
    with (A/n).open('x') as f:json.dump(o,f,indent=2);f.write('\n')
cap=J(C/'CAPTURE.json');assert cap['status']=='PASS' and cap['actual_execution'] is cap['completed'] is True and cap['exit_code']==0 and type(cap['pid']) is int and cap['pid']>0 and not cap['outer_errors']
assert cap['fresh_native13_before']==cap['fresh_native13_after'] and cap['fresh_native13_modes_before']==cap['fresh_native13_modes_after'] and cap['head_before']==cap['head_after'] and cap['actual_changed_native_inputs']==[]
assert {p.name for p in C.iterdir()}=={'CAPTURE.json','prelaunch_source.py','stdout.bin','stderr.bin'}
assert H((C/'prelaunch_source.py').read_bytes())==cap['source_sha256']==H((S/'seal_final_evidence.py').read_bytes())
for field in ['stdout','stderr']:member(C,cap[field])
assert not (C/'stderr.bin').read_bytes()
plan=J(A/'ROOT_REVIEWED_FINAL_PLAN.json');receipt=J(F/'ROOT_FINAL_RECONCILIATION.json');m=J(F/'FINAL_MANIFEST.json')
assert receipt['status']=='PASS' and receipt['entire_scope']==plan==J(F/'ROOT_REVIEWED_SCOPE.json') and receipt['bindings_before']==receipt['bindings_after']==plan['immutable_evidence_references']
assert receipt['actual_root_reconciliation'] is True and receipt['science_helpers_executed'] is receipt['shared_mutations'] is False
times=[dt.datetime.fromisoformat(t) for t in [cap['started_utc'],receipt['utc'],m['utc'],cap['finished_utc']]]
assert all(t.tzinfo and t.utcoffset()==dt.timedelta(0) for t in times) and times[0]<=times[1]<=times[3] and times[0]<=times[2]<=times[3]
assert len(m['files'])==m['files_count']==2 and m['self_excluded']==['FINAL_MANIFEST.json']
assert {z['path'] for z in m['files']}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'}
for z in m['files']:member(F,z)
assert {p.name for p in F.iterdir()}=={'FINAL_MANIFEST.json','ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'}
assert all(stat.S_IMODE(p.stat().st_mode)==0o444 for p in F.iterdir())
for z in plan['immutable_evidence_references']:member(R,z)
head=git('rev-parse','HEAD').decode().strip();assert head==cap['head_after']==git('rev-parse','origin/main').decode().strip() and git('branch','--show-current').strip()==b'main'
previous=A.parent/'pr39_9500008/state_mirror_bindings.json';assert H(previous.read_bytes())=='89f6c110f8fd8def0a87a6dcca5a159629d7f7853e5fb6ce85c8317b57e7789f'
prev=J(previous);assert len(prev['entries'])==29 and 39 in prev['required_completed_prs'] and 40 not in prev['required_completed_prs']
native=cap['fresh_native13_after'];assert len(native)==13
cache={'unsolved_math_prioritization/cache/'+x for x in ['problems.json','research_results.json','catalog.sqlite']}
for z in native:
    member(R,z);name=z['path'];assert stat.S_IMODE((R/name).stat().st_mode)==cap['fresh_native13_modes_after'][name]
    tree=git('ls-tree','-z',head,'--',name)
    if name in cache:assert not tree
    else:
        assert tree.startswith(b'100644 blob ') and tree.endswith(('\t'+name+'\0').encode())
        assert git('show',head+':'+name)==(R/name).read_bytes()
now=dt.datetime.now(dt.timezone.utc)
fresh=dict(approved_by_root=True,created_utc=now.isoformat(),reason_date_utc=now.date().isoformat(),reason='PR39 actual merge, full acceptance, present native mirror and post verification are complete and checkpoint f56477f54 is pushed; all current main thirteen bytes and exact cache Git absence were independently checked for PR40 acceptance.',current_head=head,files=native,whole_queue_sha256=native[0]['sha256'])
write('ROOT_FRESH_MAIN_PREIMAGES.json',fresh)
mapping={k:row(p) for k,p in [('final-plan',A/'ROOT_REVIEWED_FINAL_PLAN.json'),('final-receipt',F/'ROOT_FINAL_RECONCILIATION.json'),('final-manifest',F/'FINAL_MANIFEST.json'),('reconciliation-capture',C/'CAPTURE.json'),('previous-mirror',previous),('fresh-preimage',A/'ROOT_FRESH_MAIN_PREIMAGES.json')]}
arguments={'preparation-manifest-sha256':'e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba'}
for key,z in mapping.items():arguments[key]=z['path'];arguments[key+'-sha256']=z['sha256']
write('ROOT_REVIEWED_GATE_ARGUMENTS.json',dict(approved_by_root=True,root_full_runner_and_helper_review_completed=True,new_independent_runner_review_completed=True,explicit_arguments=arguments))
write('ROOT_ACTUAL_FINAL_GATE_INSPECTION.json',dict(status='PASS',utc=now.isoformat(),actual_pid=cap['pid'],entire_final_receipt=receipt,entire_actual_final_capture=cap,tracked_native_blobs=10,ignored_cache_git_absences=3,genuine_actual_PR39_predecessor=prev,full_problem_solved=False,new_substantive_attempts=0,audit_turns=0))
print(json.dumps(dict(status='PASS',actual_final_pid=cap['pid'],gate_arguments_sha256=H((A/'ROOT_REVIEWED_GATE_ARGUMENTS.json').read_bytes()),fresh_main_sha256=H((A/'ROOT_FRESH_MAIN_PREIMAGES.json').read_bytes()))))
