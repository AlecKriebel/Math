"""Close only completed first-party ROOT reproduction evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import sys
A = Path(__file__).resolve().parent
R = A.parents[2]
D = A / 'root_original_actual_reproduction_v2'
def sha(b): return hashlib.sha256(b).hexdigest()
def parse(b): return json.loads(b)
def read(p):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    return p.read_bytes()
def ref(p):
    b = read(p); return {'path': p.relative_to(R).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
def dump(o): return (json.dumps(o, indent=2, allow_nan=False) + '\n').encode()
if not __debug__ or sys.flags.optimize: raise RuntimeError('Unoptimized runtime required')
source = read(Path(__file__))
(A / 'ROOT_REPRODUCTION_CLOSURE_PRELAUNCH_SOURCE.py').write_bytes(source)
outer = []
for n, expected_pid, code in [('root_original_reproduction_actual_capture', 62101, 1), ('root_original_reproduction_v2_actual_capture', 62514, 0), ('root_full_raw_SQL_actual_capture', 65174, 0)]:
    origin = A / n; cap = parse(read(origin / 'CAPTURE.json'))
    assert cap['pid'] == expected_pid and cap['exit_code'] == code and cap['actual_execution'] is cap['completed'] is cap['operator_unchanged'] is True
    start = dt.datetime.fromisoformat(cap['started_utc']); end = dt.datetime.fromisoformat(cap['finished_utc'])
    assert start.utcoffset() == end.utcoffset() == dt.timedelta(0) and start <= end <= dt.datetime.now(dt.timezone.utc)
    assert sha(read(origin / 'prelaunch_operator.py')) == cap['operator_sha256']
    for channel in ['stdout', 'stderr']:
        z = cap[channel]; b = read(origin / z['path'])
        assert len(b) == z['bytes'] and sha(b) == z['sha256']
    dest = D / 'completed_outer_captures' / n; dest.mkdir(parents=True, exist_ok=False)
    for p in origin.iterdir(): (dest / p.name).write_bytes(read(p))
    outer.append({'source_capture': ref(origin / 'CAPTURE.json'), 'entire_capture': cap})
for n in ['ROOT_MATHEMATICAL_REVIEW.md', 'ROOT_COMPLETE_RAW_SQL_AUDIT.json', 'ROOT_REPRODUCTION_PRELAUNCH_SOURCE.py', 'ROOT_REPRODUCTION_PRELAUNCH_SOURCE_V2.py', 'ROOT_RAW_AUDIT_PRELAUNCH_SOURCE.py', 'ROOT_REPRODUCTION_CLOSURE_PRELAUNCH_SOURCE.py']:
    (D / n).write_bytes(read(A / n))
original = parse(read(D / 'ROOT_REPRODUCTION_RESULT.json'))
raw = parse(read(D / 'ROOT_COMPLETE_RAW_SQL_AUDIT.json'))
assert original['actual_operator_pid'] == 62514 and raw['actual_pid'] == 65174
summary = {'schema': 'pr46-root-current-complete-reproduction-summary/v1', 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_closure_pid': os.getpid(), 'status': 'PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION', 'entire_author_result': original['author_result'], 'entire_historical_independent_result': original['historical_independent_result'], 'complete_helper_captures': original['complete_actual_captures'], 'complete_outer_captures': outer, 'raw_audit': ref(A / 'ROOT_COMPLETE_RAW_SQL_AUDIT.json'), 'full_raw_and_prior_bytes': raw['full_raw_and_prior_bytes'], 'all_SQL_rows': raw['all_SQL_rows'], 'source_record_schema': raw['source_record_schema'], 'selected_prior_key_present': raw['selected_prior_key_present'], 'selected_prior_fallback': raw['selected_prior_fallback'], 'source_record_wrapper_claimed': False, 'closed_original_and_two_family_bindings': original['closures'], 'complete_original_turns': original['original_turns'], 'original_substantive_attempts': 0, 'source_verification_responses': 1, 'new_substantive_attempts': 0, 'audit_turns': 0, 'status_recommendation': 'already_solved', 'known_result_credit': ['Khazhgali Kozhasov', 'Mario Kummer'], 'no_mandatory_mathematical_correction_identified': True, 'future_acceptance_approved': False, 'foreign_primary_SQL_raw_cache_body_copy': False, 'historical_failure_preserved': True, 'failure_qualification': 'Initial62101 wrapper tried to parse empty failed-run stdout as JSON; distinct62514 succeeds without altering helper bytes. Empty saved output is evidence of a failed computation, not a JSON result.'}
(D / 'ROOT_CURRENT_REPRODUCTION_SUMMARY.json').write_bytes(dump(summary))
rows = []
for p in sorted(D.rglob('*')):
    assert not p.is_symlink()
    if p.is_file():
        p.chmod(0o444); b = read(p)
        assert stat.S_IMODE(p.stat().st_mode) == 0o444
        rows.append({'path': p.relative_to(D).as_posix(), 'bytes': len(b), 'sha256': sha(b), 'full_mode': '0444'})
mf = {'schema': 'pr46-root-complete-reproduction-self-only-closure/v1', 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_closure_pid': os.getpid(), 'files_count': len(rows), 'files': rows, 'directories': sorted(p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_dir()), 'self_excluded': ['MANIFEST.json'], 'foreign_primary_raw_SQL_cache_bodies_copied': False, 'future_acceptance_approved': False}
(D / 'MANIFEST.json').write_bytes(dump(mf)); (D / 'MANIFEST.json').chmod(0o444)
assert read(Path(__file__)) == source
print(json.dumps({'status': summary['status'], 'actual_pid': os.getpid(), 'members': len(rows), 'manifest': ref(D / 'MANIFEST.json'), 'summary': ref(D / 'ROOT_CURRENT_REPRODUCTION_SUMMARY.json')}))
