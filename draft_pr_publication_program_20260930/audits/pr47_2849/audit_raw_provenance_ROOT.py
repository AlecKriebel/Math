"""Full immutable importer reconstruction; save bindings, never raw cache bodies."""
from pathlib import Path
import collections
import datetime as dt
import hashlib
import json
import os
import sqlite3
import sys
A = Path(__file__).resolve().parent
R = A.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(items):
    o = {}
    for k, v in items:
        if k in o: raise ValueError('duplicate key')
        o[k] = v
    return o
def parse(b): return json.loads(b, object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def equal(x, y):
    if type(x) is not type(y): return False
    if type(x) is dict: return x.keys() == y.keys() and all(equal(x[k], y[k]) for k in x)
    if type(x) is list: return len(x) == len(y) and all(equal(a, b) for a, b in zip(x, y))
    return x == y
def read(p):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    return p.read_bytes()
def ref(p):
    b = read(p); return {'path': p.relative_to(R).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Unoptimized runtime required')
source = read(Path(__file__))
(A / 'ROOT_RAW_AUDIT_PRELAUNCH_SOURCE.py').write_bytes(source)
cache = R / 'unsolved_math_prioritization/cache'
rb = read(cache / 'problems.json'); pb = read(cache / 'research_results.json')
raw = parse(rb); prior = parse(pb)
assert len(rb) + len(pb) == 149266659 and len(raw) == 15458 and len(prior) == 6701
byid = {str(z['id']): z for z in raw}; assert len(byid) == len(raw)
codes = collections.Counter(z['problem_number'] for z in raw)
conn = sqlite3.connect('file:' + str(cache / 'catalog.sqlite') + '?mode=ro&immutable=1', uri=True)
conn.execute('PRAGMA query_only=ON'); assert conn.execute('PRAGMA query_only').fetchone() == (1,)
rows = []; seen = set()
for key, payload, report in conn.execute('SELECT key,payload,report FROM records ORDER BY key'):
    assert key not in seen; seen.add(key)
    expected = dict(byid[key]); code = expected['problem_number']
    ambiguous = codes[code] > 1 and code in prior
    if ambiguous: expected['_ambiguous_report'] = True
    expected_prior = {} if ambiguous else prior.get(code, {})
    assert equal(parse(payload), expected) and equal(parse(report), expected_prior), key
    rows.append({'key': key, 'payload_sha256': sha(payload.encode()), 'report_sha256': sha(report.encode()), 'complete_payload_recursive_type_equal': True, 'complete_report_recursive_type_equal': True, 'prior_key_present': code in prior, 'ambiguous_code': ambiguous})
conn.close(); assert seen == set(byid) and len(rows) == 15458
selected = byid['2849']; code = selected['problem_number']
assert code == 'KP-3.51' and code not in prior
saved = parse(read(A / 'source_snapshot/source_record.json'))
assert equal(saved, selected) and type(saved['id']) is int and saved['id'] == 2849
original_native = parse(read(A / 'ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json'))
assert read(A / 'source_snapshot/prior_report.json') == b'null\n'
assert original_native['upstream_report_key_presence'] == 'ABSENT' and equal(original_native['complete_selected_prior_report'], {}) and not original_native['original_vs_native_prior_JSON_equal']
result = {'schema': 'pr47-root-in-place-complete-raw-sql-audit/v1', 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid(), 'status': 'PASS_FULL_RAW_PRIOR_SQL_AND_ORIGINAL_PLAIN_SOURCE', 'inputs': [ref(cache / n) for n in ['problems.json', 'research_results.json', 'catalog.sqlite']], 'full_raw_and_prior_bytes': len(rb) + len(pb), 'all_SQL_rows': len(rows), 'complete_row_bindings': rows, 'source_record': ref(A / 'source_snapshot/source_record.json'), 'source_record_schema': 'plain_raw_problem_object', 'complete_saved_source_equals_raw_selected': True, 'selected_prior_key_present': False, 'selected_prior_fallback': {}, 'raw_null_present': False, 'literal_original_prior_file_value': None, 'literal_original_prior_differs_from_upstream_absent_fallback': True, 'original_native_selected_read': original_native, 'raw_or_SQL_or_foreign_source_bodies_copied': False, 'future_acceptance_approved': False}
with (A / 'ROOT_COMPLETE_RAW_SQL_AUDIT.json').open('x') as f:
    json.dump(result, f, indent=2, allow_nan=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
assert read(Path(__file__)) == source
print(json.dumps({'status': result['status'], 'actual_pid': os.getpid(), 'raw_bytes': len(rb) + len(pb), 'SQL_rows': len(rows), 'source_record_schema': result['source_record_schema'], 'prior_present': False}))
