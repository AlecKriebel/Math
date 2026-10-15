"""Normalize only four historical native observations; retain all other fixed bindings."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,stat,os
F=Path(__file__).resolve().parent;R=F.parents[3];A=F.parent;C=A/'reviewed_candidate';H=F/'historical_v1'
NATIVE4={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/state.json'}
def ref(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
    b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=stat.S_IMODE(s.st_mode))
def body(p,v,mode=True):
    q=ref(p)
    for k in ['bytes','sha256']+(['full_mode'] if mode else []):assert type(v[k]) is type(q[k]) and v[k]==q[k],(str(p),k)
    return q
def load(p):return json.loads(p.read_bytes())
archive=load(H/'ARCHIVE_MANIFEST.json')
for v in archive['files']:body(H/v['path'],v)
assert len(archive['files'])==21 and archive['before_any_replacement'] is True
assert (F/'CURRENT_READ_LEDGER.json').read_bytes()==(H/'CURRENT_READ_LEDGER.json').read_bytes()
old=load(H/'CURRENT_READ_LEDGER.json');assert len(old['full_body_mode_rows'])==3087
original_by_path={v['path']:v for v in old['full_body_mode_rows']};assert len(original_by_path)==3087
assert NATIVE4<=set(original_by_path)
fixed=[v for v in old['full_body_mode_rows'] if v['path'] not in NATIVE4]
assert len(fixed)==3083
for v in fixed:body(R/v['path'],v)
deps=load(C/'CURRENT_DEPENDENCIES.json'); inputs={v['path']:v for v in deps['current_native13']}
frozen_root_inputs=load(C/'root_approval/ROOT_CURRENT_INPUT_PREIMAGES.json')
assert frozen_root_inputs['current_head']=='ae20170da67ad1d891f9852ca3ed6df74a869513'
for n in NATIVE4:assert original_by_path[n]==inputs[n]==next(v for v in frozen_root_inputs['files'] if v['path']==n)
initial=load(F/'CURRENT_READ_V4_ACTUAL_CAPTURE/CAPTURE.json')
assert initial['pid']==62254 and initial['exit_code']==0 and initial['completed'] is True
dated=[]
for n in sorted(NATIVE4):
    observed=original_by_path[n];snap=C/'native4_proposal/preimage'/n.replace('/','__')
    s=body(snap,dict(observed,full_mode=0o444))
    assert s['path'] in {v['path'] for v in fixed}
    dated.append(dict(original_observed_row=observed,whole_historical_snapshot=s,observation_started_utc=initial['started_utc'],observation_finished_utc=old['created_utc'],freeze_input_authority=ref(C/'root_approval/ROOT_CURRENT_INPUT_PREIMAGES.json'),dated_main_head=frozen_root_inputs['current_head'],live_unchanged_required_by_review_closure=False,future_fresh13_ROOT_required=True))
faildir=A.parent/'pr45_9900007/root_pr49_current_whole_closure_actual_capture';fail=load(faildir/'CAPTURE.json')
assert fail['pid']==82903 and fail['exit_code']==1 and fail['completed'] is True and fail['actual_execution'] is True and fail['status']=='FAIL'
assert fail['argv'][2]==str(F/'close_review_ROOT_only.py') and fail['argv'][-1]=='a9e5f23c968956b68bc339575e0d71cad0b6149dc44748cd9b6699b94f31bad2'
members=[ref(faildir/n) for n in ['CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin']]
for k in ['stdout','stderr']:body(faildir/fail[k]['path'],dict(fail[k],full_mode=0o644))
assert ref(faildir/'prelaunch_operator.py')['sha256']==fail['operator_sha256']
assert (faildir/'stdout.bin').read_bytes()==b'' and 'inventory.json' in (faildir/'stderr.bin').read_text()
prelaunch=A/'ROOT_WHOLE_CLOSURE_PRELAUNCH_SOURCE.py'
assert prelaunch.read_bytes()==(H/'close_review_ROOT_only.py').read_bytes()
members.append(ref(prelaunch))
q=dict(schema='pr49-whole-review-narrow-dated-native4-normalization/v2',status='PASS_REQUIRED_CUSTODY_CORRECTION_PREPARED',actual_pid=os.getpid(),created_utc=datetime.now(timezone.utc).isoformat(),original_3087_ledger=ref(H/'CURRENT_READ_LEDGER.json'),original_3087_ledger_preserved_in_place=True,fixed_complete_body_mode_rows=fixed,fixed_complete_count=3083,dated_native4=dated,dated_native4_count=4,frozen_snapshot_proves_entire_original_body=True,retained_ROOT_failed_closure=fail,retained_ROOT_failed_closure_fixed_members=members,ROOT_execution_attributed=True,own_ROOT_closer_executed=False,archive=ref(H/'ARCHIVE_MANIFEST.json'),no_other_path_exemption=True,stable9_remain_live_fixed=True,current_live_native4_or_main_authority=False,future_fresh13_ROOT_required=True,no_mathematical_correction=True,no_production_import_compile_execution=True,no_native_index_ref_remote_write=True)
(F/'NORMALIZED_CURRENT_BINDINGS_V2.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps(dict(status=q['status'],actual_pid=os.getpid(),fixed_rows=len(fixed),dated_native4=len(dated),ROOT_failed_child=82903,self_manifest_exists=(F/'SELF_MANIFEST.json').exists())))
