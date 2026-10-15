"""ROOT-only actual self-excluded closure of this explicitly enumerated PR49 preparer corpus."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, stat

A = Path(__file__).resolve().parent
ROOT_FILES = ['EXPORT_PRELAUNCH_SOURCE.py', 'INSPECTION_PRELAUNCH_SOURCE.py', 'INSPECTION_V2_PRELAUNCH_SOURCE.py', 'INVENTORY_PRELAUNCH_SOURCE.py', 'ORIGINAL_CLAIM_INVENTORY.md', 'ORIGINAL_COMPLETE_RAW_SQL_READ.json', 'ORIGINAL_COMPLETE_READ_RECEIPT.json', 'ORIGINAL_COMPLETE_READ_RECEIPT_V2.json', 'ORIGINAL_NATIVE_SELECTED_READ.json', 'ORIGINAL_NATIVE_SELECTED_READ_V2.json', 'RESEARCH_LOG.md', 'capture_original_command.py', 'export_original.py', 'inspect_original.py', 'inspect_original_v2.py', 'original_diff.patch', 'original_full_tree.json', 'original_pr_metadata.json', 'original_queue_in_head.md', 'snapshot_manifest.json', 'write_original_inventory.py', 'close_original_preparation.py', 'verify_original_preparation.py', 'CLOSURE_PRELAUNCH_SOURCE.py']
CAP_DIRS = ['after_fetch_branch_actual_capture', 'after_fetch_head_actual_capture', 'after_fetch_index_actual_capture', 'before_fetch_branch_actual_capture', 'before_fetch_head_actual_capture', 'before_fetch_index_actual_capture', 'github_changed_files_actual_capture', 'github_metadata_actual_capture', 'original_export_actual_capture', 'original_fetch_actual_capture', 'original_head_object_actual_capture', 'original_inspection_actual_capture', 'original_inspection_v2_actual_capture', 'original_inventory_actual_capture']
OWN_DIRS = CAP_DIRS + ['original_git_commands', 'original_native_selected', 'original_native_selected_v2', 'source_snapshot']
MF = 'ORIGINAL_PREPARATION_MANIFEST.json'
def sha(body): return hashlib.sha256(body).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def write(path, body):
    with path.open('xb') as stream: stream.write(body); stream.flush(); os.fsync(stream.fileno())
def capture(directory, observed_exit):
    record = json.loads((directory/'CAPTURE.json').read_bytes()); pre = json.loads((directory/'PRELAUNCH.json').read_bytes())
    assert record['actual_execution'] is True and record['completed'] is True and type(record['pid']) is int and record['pid'] > 0
    assert type(record['exit_code']) is int and record['exit_code'] == observed_exit and record['operator_unchanged'] is True
    start = dt.datetime.fromisoformat(record['started_utc']); finish = dt.datetime.fromisoformat(record['finished_utc'])
    assert start.utcoffset() == finish.utcoffset() == dt.timedelta(0) and start < finish
    assert pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['exit_code'] is None
    for key in ['argv','cwd','operator_pid','operator_sha256','started_utc']:
        assert pre[key] == record[key]
    source = (directory/'prelaunch_operator.py').read_bytes(); assert sha(source) == record['operator_sha256']
    expected_names = {'prelaunch_operator.py', 'PRELAUNCH.json', 'stdout.bin', 'stderr.bin', 'CAPTURE.json'}
    target = record.get('target_source')
    if target is not None:
        assert isinstance(target, dict) and record['target_unchanged'] is True and pre['target_source'] == target
        body=(directory/'prelaunch_target.py').read_bytes(); assert len(body)==target['bytes'] and sha(body)==target['sha256']
        expected_names.add('prelaunch_target.py')
    elif 'target_source' in record:
        assert record['target_source'] is None and record['target_unchanged'] is None and pre['target_source'] is None
    assert {path.name for path in directory.iterdir()} == expected_names
    for name in ['stdout','stderr']:
        body=(directory/record[name]['path']).read_bytes();assert len(body)==record[name]['bytes'] and sha(body)==record[name]['sha256']
    if record['schema']=='pr49-original-actual-command/v1':
        assert record['expected_exit']==0
        assert record['capture_status']==('EXPECTED_ACTUAL_EXIT_COMPLETE' if observed_exit==0 else 'UNEXPECTED_OR_INCOMPLETE_ACTUAL_EXIT')
    else: assert record['schema']=='pr49-original-readonly-git-command/v1' and observed_exit==0
    return dict(path=(directory/'CAPTURE.json').relative_to(A).as_posix(), schema=record['schema'], argv=record['argv'], pid=record['pid'], operator_pid=record['operator_pid'], started_utc=record['started_utc'], finished_utc=record['finished_utc'], exit_code=record['exit_code'], capture_sha256=sha((directory/'CAPTURE.json').read_bytes()), full_streams_verified=True, actual_operation_complete=True, retained_failed_operation=observed_exit!=0, expected_success_not_fabricated=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected-inventory-sha256',required=True);args=parser.parse_args()
    source=Path(__file__).read_bytes()
    assert not (A/MF).exists() and sha((A/'ORIGINAL_CLAIM_INVENTORY.md').read_bytes())==args.expected_inventory_sha256
    write(A/'CLOSURE_PRELAUNCH_SOURCE.py',source)
    captures=[]
    for name in CAP_DIRS:
        observed=128 if name=='original_head_object_actual_capture' else 1 if name=='original_inspection_actual_capture' else 0
        captures.append(capture(A/name,observed))
    git_dirs=sorted((A/'original_git_commands').iterdir());assert len(git_dirs)==44 and all(path.is_dir() and not path.is_symlink() for path in git_dirs)
    for directory in git_dirs:captures.append(capture(directory,0))
    assert len(captures)==58 and sum(row['retained_failed_operation'] for row in captures)==2
    manifest=json.loads((A/'snapshot_manifest.json').read_bytes());read=json.loads((A/'ORIGINAL_COMPLETE_READ_RECEIPT_V2.json').read_bytes());raw=json.loads((A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json').read_bytes());native=json.loads((A/'ORIGINAL_NATIVE_SELECTED_READ_V2.json').read_bytes())
    assert manifest['original_files']==len(manifest['files'])==16 and manifest['whole_repository_diff_files']==17 and len(manifest['scientific_tree_entries'])==20
    assert manifest['head']=='036a5ed59bee5ed79f08349290481584610f1456' and manifest['merge_base']==manifest['github_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
    assert read['original_files_read_in_full']==16 and len(read['complete_original_JSON_values'])==9 and read['all_16_added_scientific_hunks_reconstructed_byte_exact'] is True
    assert read['original_substantive_turns']==0 and read['turn_limit']==5 and read['new_substantive_turns']==0
    assert read['helper_execution_performed'] is False and read['mathematical_predicates_reproduced'] is False and read['acceptance_verdict'] is None
    assert raw['literal_importer_verified_rows']==len(raw['rows'])==raw['raw_problem_count']==raw['all_SQL_rows_read']==15458 and raw['all_recursive_scalar_types_verified'] is True
    selected=raw['selected'];assert selected['upstream_report_key_present'] is False and selected['upstream_report_presence']=='ABSENT' and selected['sqlite_report_literal']=='{}' and selected['original_prior_report_equals_SQLite_importer_report'] is False
    assert raw['raw_foreign_bodies_copied'] is False and raw['SQLite_writes'] is False and raw['native_writes'] is False and raw['future_acceptance_authority'] is False
    assert native['canonical_count']==len(native['current_canonical13_bindings'])==13 and native['native_writes'] is False and native['transition_performed'] is False and native['authority_for_future_main'] is False
    for row in manifest['files']:
        path=A/'source_snapshot'/row['relative_path'];body=path.read_bytes();assert len(body)==row['bytes'] and sha(body)==row['sha256'] and row['git_mode']=='100644'
    at=now()
    with (A/'RESEARCH_LOG.md').open('a') as stream:
        stream.write('\n'+at+' — Actual ROOT closure child PID'+str(os.getpid())+' verified58 completed earlier capture records, including genuine missing-head exit128 and first-inspection exit1. Read all16 originals/9JSON values, complete17pathdiff, source plain/null/ABSENT/SQL{} distinction and15458literal importer checks. Explicit original-preparer corpus frozen at mode0444; only this closing manifest is self-excluded. Independent reviewer/ROOT sibling folders and future external closure capture are outside preparer authorship. Outer completion remains PENDING_CHILD_EXIT; this child does not certify its future external capture or future acceptance. Original preservation100%; mathematical/source-claim validation0%; original turns0/5; new substantive turns0; original status attributed already_solved; ROOT acceptance/native transition/merge remain pending.\n')
        stream.flush();os.fsync(stream.fileno())
    paths=[A/name for name in ROOT_FILES]
    for name in OWN_DIRS:
        directory=A/name;assert directory.is_dir() and not directory.is_symlink()
        for path in directory.rglob('*'):
            assert not path.is_symlink() and (path.is_file() or path.is_dir())
            if path.is_file():paths.append(path)
    assert len(paths)==len(set(paths))==350
    rows=[]
    for path in sorted(paths):
        assert path.is_file() and not path.is_symlink()
        body=path.read_bytes();os.chmod(path,0o444)
        rows.append(dict(path=path.relative_to(A).as_posix(),bytes=len(body),sha256=sha(body),full_mode=stat.S_IMODE(path.stat().st_mode)))
    directories=sorted({parent for path in paths for parent in path.parents if parent!=A and A in parent.parents})
    directory_rows=[dict(path=path.relative_to(A).as_posix(),full_mode=stat.S_IMODE(path.stat().st_mode)) for path in directories]
    actual_dirs={path.relative_to(A).as_posix() for name in OWN_DIRS for path in [A/name]+list((A/name).rglob('*')) if path.is_dir()};assert actual_dirs=={row['path'] for row in directory_rows}
    record=dict(schema='pr49-original-preparation-self-only-manifest/v1',created_utc=at,actual_pid=os.getpid(),head=manifest['head'],github_base=manifest['github_base'],merge_base=manifest['merge_base'],files_count=len(rows),files=rows,owned_directories=[row['path'] for row in directory_rows],owned_directory_bindings=directory_rows,authorship_root_files=ROOT_FILES,authorship_directory_roots=OWN_DIRS,authorship_root_full_mode=stat.S_IMODE(A.stat().st_mode),self_excluded=[MF],complete_prior_actual_captures=captures,complete_prior_actual_captures_count=len(captures),retained_failed_actual_operations=2,in_place_foreign_native_read_operations_count=32,in_place_foreign_native_read_operations_retained_as_typed_bindings=True,foreign_native_raw_bodies_not_copied=True,foreign_cached_raw_bodies_not_copied=True,foreign_primary_pdf_OCR_pixel_bodies_in_authorship=False,independent_review_and_ROOT_siblings_outside_preparer_authorship=True,outer_capture_status_at_child_closure='PENDING_CHILD_EXIT',outer_capture_outside_authorship_scope=True,outer_post_child_completion_and_ROOT_readback_required=True,all_owned_files_full_mode=0o444,all4096_permission_bits_individually_recorded=True,original_scientific_files=16,original_JSON_values=9,full_diff_paths=17,original_ledger_kind='JSON turns.json',original_substantive_turns=0,turn_limit=5,new_substantive_turns=0,original_proposed_status_attributed='already_solved',current_mathematical_verdict=None,source_claim_validation_verdict=None,helper_execution_performed=False,primary_source_bodies_freshly_read=False,primary_pdf_hashes_freshly_authenticated=False,ROOT_acceptance='PENDING',independent_review='PENDING',native_transition='PENDING',merge='PENDING',future_acceptance_authority=False,prior_report_source_presence='UPSTREAM_ABSENT_SQLITE_EMPTY_OBJECT_ORIGINAL_NULL_ADMINISTRATIVE_MARKER',original_preparation_completion_estimate_percent=100,mathematical_and_source_claim_validation_completion_estimate_percent=0)
    write(A/MF,(json.dumps(record,indent=2,sort_keys=True)+'\n').encode());os.chmod(A/MF,0o444)
    for row in rows:
        path=A/row['path'];body=path.read_bytes();assert len(body)==row['bytes'] and sha(body)==row['sha256'] and stat.S_IMODE(path.stat().st_mode)==row['full_mode']==0o444
    assert Path(__file__).read_bytes()==source
    print(json.dumps(dict(status='ORIGINAL_PREPARATION_CLOSED_ONLY',actual_pid=os.getpid(),created_utc=at,manifest_bytes=(A/MF).stat().st_size,manifest_sha256=sha((A/MF).read_bytes()),owned_files=len(rows),owned_directories=len(directory_rows),prior_actual_captures=len(captures),retained_failed_operations=2,original_files=16,original_JSON_values=9,helper_execution_performed=False,acceptance_verdict=None),sort_keys=True))
if __name__=='__main__':main()
