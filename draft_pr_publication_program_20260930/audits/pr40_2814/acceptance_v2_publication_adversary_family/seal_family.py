#!/usr/bin/env python3
"""Seal exactly this authored review; includes the intentionally empty fixture dir."""
import datetime as dt
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
NAME='FIRST_PARTY_MANIFEST.json'
assert not (HERE/NAME).exists()
def sha(raw): return hashlib.sha256(raw).hexdigest()
coverage=json.loads((HERE/'READ_COVERAGE.json').read_bytes())
for row in coverage['complete_combined_bound_input_inventory']:
    path=ROOT/row['path']
    assert path.is_file() and not path.is_symlink()
    raw=path.read_bytes()
    assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['path']
assessment=json.loads((HERE/'ASSESSMENT.json').read_bytes())
assert assessment['status']=='PASS_QUALIFIED_SOURCE_ONLY' and assessment['mandatory_candidate_defects']==[]
for name in ['report','full_read_coverage','foreign_inventories_separately_bound','v2_manifest','wrapper_manifest','wrapper_source']:
    row=assessment[name]; raw=(ROOT/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
for directory in [p for p in HERE.iterdir() if p.name.endswith('_actual_capture')]:
    assert directory.is_dir() and not directory.is_symlink()
    assert {p.name for p in directory.iterdir()}=={'CAPTURE.json','prelaunch_source.py','stdout.bin','stderr.bin'}
    receipt=json.loads((directory/'CAPTURE.json').read_bytes())
    assert receipt['actual_execution'] is True and receipt['completed'] is True and type(receipt['pid']) is int and receipt['pid']>0
    assert type(receipt['exit_code']) is int and receipt['exit_code']==(1 if directory.name=='inspect_wrapper_actual_capture' else 0)
    assert dt.datetime.fromisoformat(receipt['started_utc'])<=dt.datetime.fromisoformat(receipt['finished_utc'])
    assert sha((directory/'prelaunch_source.py').read_bytes())==receipt['source_sha256']
    for key in ['stdout','stderr']:
        row=receipt[key]; raw=(directory/row['path']).read_bytes()
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
files=[]; directories=[]
for path in sorted(HERE.rglob('*')):
    assert not path.is_symlink()
    if path.is_dir(): directories.append(path.relative_to(HERE).as_posix())
    else:
        assert path.is_file()
        raw=path.read_bytes()
        path.chmod(0o444)
        files.append({'path':path.relative_to(HERE).as_posix(),'bytes':len(raw),'sha256':sha(raw),'mode':292})
assert 'directory_publication_fixtures/empty_intervening/capture' in directories
manifest={
    'schema':'pr40-v2-wrapper-independent-publication-adversary-exact-closure/v1',
    'status':'CLOSED_PASS_QUALIFIED_SOURCE_ONLY','closed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'self_excluded_paths':[NAME],'foreign_excluded_prefixes':[],'scratch_exclusions':[],
    'files_count':len(files),'files':files,'directories':directories,
    'empty_directories_intentionally_retained':['directory_publication_fixtures/empty_intervening/capture'],
    'directory_membership_rule':'Exact explicit directory inventory including the retained empty intervening-destination control; no exclusions.',
    'foreign_input_inventory':{'path':'FOREIGN_INPUT_INVENTORIES.json','sha256':sha((HERE/'FOREIGN_INPUT_INVENTORIES.json').read_bytes()),'foreign_file_counts':[20,17,21]},
    'v2_preparation_manifest_sha256':'e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba',
    'wrapper_preparation_manifest_sha256':'aa58d2e3a9f470c6ce8d2781e47c72605de8338ee6766bb390a7f57ab7f42d50',
    'wrapper_source_sha256':'f00d8be3926b02d10f46a351802688a87f107d406c842317f51a5674248d4215',
    'reviewed_helper_wrapper_native_driver_import_compile_execution':False,
    'actual_future_PR40_gate_merge_mirror_post_claimed':False,
    'own_initial_wrapper_inspector_failure_retained':True,'mandatory_candidate_defects':[],
    'source_review_completion_estimate_percent':100,'scientific_discovery_completion_estimate_percent':0,
    'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,
}
raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
with (HERE/NAME).open('xb') as f: f.write(raw)
(HERE/NAME).chmod(0o444)
assert {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}=={r['path'] for r in files}|{NAME}
assert {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_dir()}==set(directories)
assert all((p.stat().st_mode & 0o777)==0o444 for p in HERE.rglob('*') if p.is_file())
print(json.dumps({'status':'CLOSED_PASS_QUALIFIED_SOURCE_ONLY','manifest_path':str(HERE/NAME),'manifest_sha256':sha(raw),'authored_members_excluding_self':len(files),'directories_count':len(directories),'retained_empty_directory':manifest['empty_directories_intentionally_retained'],'candidate_execution':False,'actual_future_gate_claimed':False}))
