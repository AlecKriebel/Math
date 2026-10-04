"""Seal exact self-only PR47 original preparation; issue no mathematical verdict."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
A=Path(__file__).resolve().parent
ROOT_FILES=['EXPORT_PRELAUNCH_SOURCE.py','INSPECTION_PRELAUNCH_SOURCE.py','INSPECTION_V2_PRELAUNCH_SOURCE.py','INVENTORY_PRELAUNCH_SOURCE.py','ORIGINAL_CLAIM_INVENTORY.md','ORIGINAL_COMPLETE_READ_RECEIPT.json','ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json','ORIGINAL_FOREIGN_SOURCE_BINDINGS.json','ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json','ORIGINAL_SELECTION_CORRECTION.json','RESEARCH_LOG.md','capture_original_command.py','export_original.py','inspect_original.py','inspect_original_v2.py','original_diff.patch','original_native_input_bindings.json','original_pr_metadata.json','original_queue_in_head.md','snapshot_manifest.json','write_original_inventory.py','close_original_preparation.py','CLOSURE_PRELAUNCH_SOURCE.py']
CAP_DIRS=['github_changed_files_actual_capture','github_metadata_actual_capture','original_export_actual_capture','original_full_inspection_actual_capture','original_full_inspection_v2_actual_capture','original_github_base_commit_actual_capture','original_head_commit_actual_capture','original_head_fetch_actual_capture','original_head_object_actual_capture','original_inventory_authorship_actual_capture','original_native_main_head_actual_capture']
OWN_DIRS=['source_snapshot','original_native_selected','original_git_commands']+CAP_DIRS
OUTER='original_preparation_closure_actual_capture'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def write(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def capture(d,expected):
    assert {p.name for p in d.iterdir()}=={'prelaunch_operator.py','PRELAUNCH.json','stdout.bin','stderr.bin','CAPTURE.json'}
    c=json.loads((d/'CAPTURE.json').read_bytes());pre=json.loads((d/'PRELAUNCH.json').read_bytes())
    assert c['actual_execution'] is True and c['completed'] is True and c['exit_code']==expected and type(c['pid']) is int and c['pid']>0
    t0=dt.datetime.fromisoformat(c['started_utc']);t1=dt.datetime.fromisoformat(c['finished_utc']);assert t0.utcoffset()==t1.utcoffset()==dt.timedelta(0) and t0<t1
    assert pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['operator_sha256']==c['operator_sha256'] and pre['argv']==c['argv'] and pre['started_utc']==c['started_utc']
    for key in ['stdout','stderr']:
        b=(d/c[key]['path']).read_bytes();assert len(b)==c[key]['bytes'] and sha(b)==c[key]['sha256']
    assert sha((d/'prelaunch_operator.py').read_bytes())==c['operator_sha256'] and c['operator_unchanged'] is True
    return dict(path=(d/'CAPTURE.json').relative_to(A).as_posix(),pid=c['pid'],exit_code=c['exit_code'],started_utc=c['started_utc'],finished_utc=c['finished_utc'],argv=c['argv'],complete_streams_validated=True,aware_UTC_interval_validated=True)
def main():
    source=Path(__file__).read_bytes();write(A/'CLOSURE_PRELAUNCH_SOURCE.py',source)
    caps=[]
    for name in CAP_DIRS:
        expected=128 if name=='original_head_object_actual_capture' else 1 if name=='original_full_inspection_actual_capture' else 0
        caps.append(capture(A/name,expected))
    gitdirs=sorted((A/'original_git_commands').iterdir());assert len(gitdirs)==40 and all(p.is_dir() and not p.is_symlink() for p in gitdirs)
    for d in gitdirs:caps.append(capture(d,0))
    assert len(caps)==51
    m=json.loads((A/'snapshot_manifest.json').read_bytes());rr=json.loads((A/'ORIGINAL_COMPLETE_READ_RECEIPT.json').read_bytes())
    assert len(m['files'])==m['original_files']==16 and m['whole_repository_diff_files']==17
    assert rr['original_files_read_in_full']==16 and rr['all_16_added_hunks_reconstructed_byte_exact'] is True and rr['helper_execution_performed'] is False and rr['mathematical_predicates_reproduced'] is False and rr['acceptance_verdict'] is None and rr['original_substantive_turns']==1 and rr['new_substantive_turns']==0
    for r in m['files']:
        p=A/'source_snapshot'/r['relative_path'];b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'] and r['git_mode']=='100644' and stat.S_IMODE(p.stat().st_mode)==0o444
    n=json.loads((A/'ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json').read_bytes());assert n['canonical_count']==13 and n['native_writes'] is False and n['transition_performed'] is False and n['authority_for_future_main'] is False
    selected=json.loads((A/'ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json').read_bytes());assert selected['upstream_report_key_presence']=='ABSENT' and selected['complete_selected_prior_report']=={} and selected['original_prior_report_file_value'] is None
    at=now()
    with (A/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+at+' — Exact self-only original closure child PID'+str(os.getpid())+'. Verified51 completed prior actual captures, including missing-head exit128 and initial-inspection exit1; both complete streams, UTC intervals and prelaunch sources preserved. Verified16 original bodies,9 JSON receipts, full17-path diff, literal JSON1/5 ledger, canonical13 dated native bindings and absent-default prior distinction. All enumerated own files frozen at full mode0444. Outer CAP remains PENDING_CHILD_EXIT here and is excluded from this manifest; the genuine operator completes and freezes that separate5-file CAP only after this child exits. Source preparation100%; independent mathematical/source claim validation0%; full-target discovery0%; new substantive turns0. Independent review and merge remain PENDING.\n');f.flush();os.fsync(f.fileno())
    paths=[A/name for name in ROOT_FILES]
    for name in OWN_DIRS:paths.extend(p for p in (A/name).rglob('*') if p.is_file())
    assert len(paths)==len(set(paths))==301
    rows=[]
    for p in sorted(paths):
        assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in [p]+list(p.parents) if q==A or A in q.parents)
        b=p.read_bytes();assert len(b)<100*1024*1024;os.chmod(p,0o444);assert stat.S_IMODE(p.stat().st_mode)==0o444
        rows.append(dict(path=p.relative_to(A).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
    dirs=sorted({q for p in paths for q in p.parents if q!=A and A in q.parents})
    dirrows=[dict(path=p.relative_to(A).as_posix(),full_mode=stat.S_IMODE(p.stat().st_mode)) for p in dirs]
    assert {p.relative_to(A).as_posix() for p in (A/'source_snapshot').rglob('*') if p.is_file()}=={'source_snapshot/'+r['relative_path'] for r in m['files']}
    listed={r['path'] for r in rows};actual={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file() and (p.relative_to(A).parts[0] in OWN_DIRS or (len(p.relative_to(A).parts)==1 and p.name in ROOT_FILES))};assert listed==actual
    record=dict(schema='pr47-original-preparation-self-only-manifest/v1',created_utc=at,actual_pid=os.getpid(),head=m['head'],github_base=m['github_base'],merge_base=m['merge_base'],original_manifest_sha256=sha((A/'snapshot_manifest.json').read_bytes()),files_count=len(rows),files=rows,owned_directories=[r['path'] for r in dirrows],owned_directory_bindings=dirrows,authorship_root_files=ROOT_FILES,authorship_directory_roots=OWN_DIRS,authorship_root_full_mode=stat.S_IMODE(A.stat().st_mode),self_excluded=['ORIGINAL_PREPARATION_MANIFEST.json'],outer_capture_outside_authorship_scope=OUTER,outer_capture_status_at_child_closure='PENDING_CHILD_EXIT',outer_capture_completion_rule='Actual operator writes CAPTURE and complete streams only after child exits and seals five separate files0444; child manifest does not certify its future completion.',outer_capture_named_files=['prelaunch_operator.py','PRELAUNCH.json','stdout.bin','stderr.bin','CAPTURE.json'],independent_reviewer_siblings_excluded_from_preparer_authorship=True,complete_prior_actual_captures=caps,complete_prior_actual_captures_count=len(caps),all_owned_files_full_mode=0o444,all4096_permission_bits_individually_recorded=True,original_foreign_pdf_ocr_pixel_bodies_in_authorship=False,foreign_cached_raw_bodies_copied=False,foreign_source_bodies_freshly_read=False,mathematical_reproduction_performed=False,acceptance_verdict=None,independent_review='PENDING',merge='PENDING',original_ledger_kind='JSON object turns.json',original_substantive_turns=1,turn_limit=5,new_substantive_turns=0,prior_report_source_presence='UPSTREAM_ABSENT_SQLITE_EMPTY_OBJECT_ORIGINAL_NULL',original_preparation_completion_estimate_percent=100,independent_claim_validation_completion_estimate_percent=0)
    target=A/'ORIGINAL_PREPARATION_MANIFEST.json';write(target,(json.dumps(record,indent=2,sort_keys=True)+'\n').encode());os.chmod(target,0o444);assert stat.S_IMODE(target.stat().st_mode)==0o444
    assert Path(__file__).read_bytes()==source
    for row in rows:
        p=A/row['path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==row['full_mode']
    print(json.dumps(dict(status='ORIGINAL_PREPARATION_CLOSED_ONLY',created_utc=at,actual_pid=os.getpid(),manifest_bytes=target.stat().st_size,manifest_sha256=sha(target.read_bytes()),owned_files=len(rows),owned_directories=len(dirrows),prior_actual_captures=len(caps),scientific_originals=16,substantive_turns=1,helper_replays=0,acceptance_verdict=None,source_preparation_percent=100,claim_validation_percent=0),sort_keys=True))
if __name__=='__main__':main()
