"""Seal exact self-only PR48 original preparation; no mathematical verdict."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
A=Path(__file__).resolve().parent
ROOT_FILES=['ORIGINAL_COMPLETE_READ_RECEIPT.json','original_queue_in_head.md','original_native_input_bindings.json','EXPORT_PRELAUNCH_SOURCE.py','write_original_inventory.py','capture_original_command.py','ORIGINAL_SELECTION_CORRECTION.json','export_original_v2.py','RESEARCH_LOG.md','ORIGINAL_FOREIGN_SOURCE_BINDINGS.json','ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json','inspect_original.py','ORIGINAL_CLAIM_INVENTORY.md','export_original.py','INVENTORY_PRELAUNCH_SOURCE.py','snapshot_manifest.json','ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json','EXPORT_V2_PRELAUNCH_SOURCE.py','original_diff.patch','INSPECTION_PRELAUNCH_SOURCE.py','original_full_tree.json','original_pr_metadata.json','close_original_preparation.py','CLOSURE_PRELAUNCH_SOURCE.py']
CAP_DIRS=['github_metadata_actual_capture','github_changed_files_actual_capture','original_head_object_actual_capture','original_native_main_head_actual_capture','original_head_fetch_actual_capture','original_head_commit_actual_capture','original_github_base_commit_actual_capture','original_export_actual_capture','original_export_v2_actual_capture','original_full_inspection_actual_capture','original_inventory_authorship_actual_capture']
OWN_DIRS=['original_git_commands','original_git_commands_v2','original_native_selected','original_native_selected_v2','source_snapshot']+CAP_DIRS
OUTER='original_preparation_closure_actual_capture'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def write(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def capture(d,expected):
    c=json.loads((d/'CAPTURE.json').read_bytes());pre=json.loads((d/'PRELAUNCH.json').read_bytes())
    names={'prelaunch_operator.py','PRELAUNCH.json','stdout.bin','stderr.bin','CAPTURE.json'}
    if 'target_source' in c:names.add('prelaunch_target.py')
    assert {p.name for p in d.iterdir()}==names
    assert c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==expected and type(c['pid']) is int and c['pid']>0
    t0=dt.datetime.fromisoformat(c['started_utc']);t1=dt.datetime.fromisoformat(c['finished_utc']);assert t0.utcoffset()==t1.utcoffset()==dt.timedelta(0) and t0<t1
    assert pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['exit_code'] is None and pre['operator_sha256']==c['operator_sha256'] and pre['argv']==c['argv'] and pre['cwd']==c['cwd'] and pre['started_utc']==c['started_utc']
    for key in ('stdout','stderr'):
        b=(d/c[key]['path']).read_bytes();assert len(b)==c[key]['bytes'] and sha(b)==c[key]['sha256']
    assert sha((d/'prelaunch_operator.py').read_bytes())==c['operator_sha256'] and c['operator_unchanged'] is True
    if 'target_source' in c:
        target=(d/'prelaunch_target.py').read_bytes();assert sha(target)==c['target_source']['sha256'] and len(target)==c['target_source']['bytes'] and pre['target_source']==c['target_source'] and c['target_unchanged'] is True
    return dict(path=(d/'CAPTURE.json').relative_to(A).as_posix(),pid=c['pid'],exit_code=c['exit_code'],started_utc=c['started_utc'],finished_utc=c['finished_utc'],argv=c['argv'],cwd=c['cwd'],complete_streams_validated=True,aware_UTC_interval_validated=True,prelaunch_sources_validated=True)
def main():
    source=Path(__file__).read_bytes();write(A/'CLOSURE_PRELAUNCH_SOURCE.py',source);assert not (A/'ORIGINAL_PREPARATION_MANIFEST.json').exists()
    caps=[]
    for name in CAP_DIRS:caps.append(capture(A/name,128 if name=='original_head_object_actual_capture' else 1 if name=='original_export_actual_capture' else 0))
    for name in ('original_git_commands','original_git_commands_v2'):
        dirs=sorted((A/name).iterdir());assert len(dirs)==46 and all(p.is_dir() and not p.is_symlink() for p in dirs)
        for d in dirs:caps.append(capture(d,0))
    assert len(caps)==103
    m=json.loads((A/'snapshot_manifest.json').read_bytes());rr=json.loads((A/'ORIGINAL_COMPLETE_READ_RECEIPT.json').read_bytes());native=json.loads((A/'ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json').read_bytes());selected=json.loads((A/'ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json').read_bytes());correction=json.loads((A/'ORIGINAL_SELECTION_CORRECTION.json').read_bytes());tree=json.loads((A/'original_full_tree.json').read_bytes())
    assert m['original_files']==len(m['files'])==17 and m['whole_repository_diff_files']==18 and len(m['scientific_tree_entries'])==22 and len(tree['whole_repository_entries'])==36538
    assert rr['original_files_read_in_full']==17 and len(rr['complete_original_JSON_values'])==8 and len(rr['complete_original_JSONL_values']['turns.jsonl'])==2 and rr['all_17_added_hunks_reconstructed_byte_exact'] is True and rr['helper_execution_performed'] is False and rr['mathematical_predicates_reproduced'] is False and rr['acceptance_verdict'] is None and rr['original_substantive_turns']==2 and rr['new_substantive_turns']==0 and rr['turn_limit']==5
    assert sum(v['equals_claimed_original'] for v in rr['original_sentence_reversal_candidates'])==1
    for row in m['files']:
        p=A/'source_snapshot'/row['relative_path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and row['git_mode']=='100644' and stat.S_IMODE(p.stat().st_mode)==0o444
    assert native['canonical_count']==len(native['current_canonical13_bindings'])==13 and all(r['body_read_in_full'] for r in native['current_canonical13_bindings']) and native['native_writes'] is False and native['transition_performed'] is False and native['authority_for_future_main'] is False
    assert selected['selected_rows_count']==2 and selected['raw_problem_IDs_unique'] is True and selected['foreign_full_raw_bodies_copied'] is False and selected['source_claims_not_validated'] is True
    assert {v['key'] for v in selected['selected']}=={'2961','30004403'}
    for v in selected['selected']:assert v['upstream_report_key_present'] is False and v['upstream_report_presence']=='ABSENT' and v['complete_upstream_report'] is None and v['complete_selected_prior_SQLite']=={} and v['sqlite_report_literal']=='{}' and v['original_prior_report_file_exists'] is False and v['source_record_semantics']=='plain selected problem; no queue.py show wrapper'
    assert len(correction['corrections'])==7 and correction['initial_receipts_retained'] is True and correction['corrected_receipts_separate'] is True
    for row in correction['corrections']:assert sha((A/row['original_path']).read_bytes())==row['original_sha256'] and sha((A/row['corrected_path']).read_bytes())==row['corrected_sha256']
    at=now()
    with (A/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+at+' — Exact original preparation closure child PID '+str(os.getpid())+'. Verified103 prior completed actual captures, including missing-head exit128 and export_v1 exit1 with full streams/prelaunch sources; corrected export_v2 and typed inspection exit0. All17 originals,8 JSON values,2-line JSONL ledger, full18-path diff and full head-tree manifests verified. Native13 actual full-body bindings and both exact raw/plain/wrapper/absent-report/SQLite{} distinctions retained; initial string-ID selection error preserved and separate correction verified. Exact enumerated own files frozen at full mode0444. Outer capture remains PENDING_CHILD_EXIT and is excluded from this authored manifest; actual ROOT operator must finish/seal its separate capture only after child exit. Source preparation100%; independent mathematical/source claim validation0%; new substantive turns0; ROOT acceptance/independent review/native transition/merge PENDING.\n');f.flush();os.fsync(f.fileno())
    paths=[A/name for name in ROOT_FILES]
    for name in OWN_DIRS:paths.extend(p for p in (A/name).rglob('*') if p.is_file())
    assert len(paths)==len(set(paths))==574
    rows=[]
    for p in sorted(paths):
        assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in [p]+list(p.parents) if q==A or A in q.parents)
        b=p.read_bytes();os.chmod(p,0o444);assert stat.S_IMODE(p.stat().st_mode)==0o444
        rows.append(dict(path=p.relative_to(A).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
    dirs=sorted({q for p in paths for q in p.parents if q!=A and A in q.parents});assert len(dirs)==110
    directory_rows=[dict(path=p.relative_to(A).as_posix(),full_mode=stat.S_IMODE(p.stat().st_mode)) for p in dirs]
    actual_dirs={p.relative_to(A).as_posix() for name in OWN_DIRS for p in [A/name]+list((A/name).rglob('*')) if p.is_dir()};assert actual_dirs=={r['path'] for r in directory_rows}
    actual_files={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file() and (p.relative_to(A).parts[0] in OWN_DIRS or (len(p.relative_to(A).parts)==1 and p.name in ROOT_FILES))};assert actual_files=={r['path'] for r in rows}
    assert {p.relative_to(A).as_posix() for p in (A/'source_snapshot').rglob('*') if p.is_file()}=={'source_snapshot/'+r['relative_path'] for r in m['files']}
    record=dict(schema='pr48-original-preparation-self-only-manifest/v1',created_utc=at,actual_pid=os.getpid(),head=m['head'],github_base=m['github_base'],merge_base=m['merge_base'],original_manifest_sha256=sha((A/'snapshot_manifest.json').read_bytes()),files_count=len(rows),files=rows,owned_directories=[r['path'] for r in directory_rows],owned_directory_bindings=directory_rows,authorship_root_files=ROOT_FILES,authorship_directory_roots=OWN_DIRS,authorship_root_full_mode=stat.S_IMODE(A.stat().st_mode),self_excluded=['ORIGINAL_PREPARATION_MANIFEST.json'],outer_capture_outside_authorship_scope=OUTER,outer_capture_status_at_child_closure='PENDING_CHILD_EXIT',outer_capture_completion_rule='Actual ROOT operator writes CAPTURE/full streams and freezes its separate capture only after child exit; child manifest does not certify future completion.',outer_capture_expected_files_if_supplied_original_operator=['prelaunch_operator.py','prelaunch_target.py','PRELAUNCH.json','stdout.bin','stderr.bin','CAPTURE.json'],independent_reviewer_siblings_excluded_from_preparer_authorship=True,complete_prior_actual_captures=caps,complete_prior_actual_captures_count=len(caps),all_owned_files_full_mode=0o444,all4096_permission_bits_individually_recorded=True,original_foreign_pdf_ocr_pixel_bodies_in_authorship=False,foreign_cached_raw_bodies_copied=False,foreign_source_bodies_freshly_read=False,mathematical_reproduction_performed=False,helper_replays=0,acceptance_verdict=None,ROOT_acceptance='PENDING',independent_review='PENDING',native_transition='PENDING',merge='PENDING',original_ledger_kind='JSONL turns.jsonl',original_substantive_turns=2,turn_limit=5,new_substantive_turns=0,prior_report_source_presence='BOTH_UPSTREAM_KEYS_ABSENT_SQLITE_EMPTY_OBJECT_NO_PRIOR_FILE_PROSE_NULL',original_preparation_completion_estimate_percent=100,independent_claim_validation_completion_estimate_percent=0)
    target=A/'ORIGINAL_PREPARATION_MANIFEST.json';write(target,(json.dumps(record,indent=2,sort_keys=True)+'\n').encode());os.chmod(target,0o444);assert stat.S_IMODE(target.stat().st_mode)==0o444 and Path(__file__).read_bytes()==source
    for row in rows:
        p=A/row['path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==row['full_mode']
    for row in directory_rows:assert stat.S_IMODE((A/row['path']).stat().st_mode)==row['full_mode']
    print(json.dumps(dict(status='ORIGINAL_PREPARATION_CLOSED_ONLY',created_utc=at,actual_pid=os.getpid(),manifest_bytes=target.stat().st_size,manifest_sha256=sha(target.read_bytes()),owned_files=len(rows),owned_directories=len(dirs),prior_actual_captures=len(caps),scientific_originals=17,substantive_turns=2,helper_replays=0,acceptance_verdict=None,source_preparation_percent=100,claim_validation_percent=0),sort_keys=True))
if __name__=='__main__':main()
