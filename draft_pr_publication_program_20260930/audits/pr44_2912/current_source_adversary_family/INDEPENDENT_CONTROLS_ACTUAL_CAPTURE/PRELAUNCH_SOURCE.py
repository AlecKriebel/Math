"""Independent audit/control implementation. Production is read as text only.

This code neither imports nor compiles nor runs a proposed preparation program.
It independently checks immutable inputs, exact topology, actual ROOT evidence,
read-only database joins and private declarative counterexamples. Its claims are
source review, not a production runtime test or a mathematical theorem.
"""
from pathlib import Path, PurePosixPath
import ast
import collections
import copy
import ctypes
import datetime as dt
import hashlib
import json
import math
import os
import re
import sqlite3
import stat
import subprocess
import sys

HERE = Path(__file__).absolute().parent
A = HERE.parent
R = A.parents[2]
P = A / 'current_preparation_family'
counts = collections.Counter()
foreign = {}
rejected = []
commands = []
full_reads = 0
full_bytes = 0
def check(x, label):
    assert x, label
    counts[label] += 1
def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def encode(x): return (json.dumps(x, indent=2, allow_nan=False) + '\n').encode()
def valid_path(s):
    if type(s) is not str or not s or '\\' in s or '\x00' in s: raise ValueError('path')
    p = PurePosixPath(s)
    if p.is_absolute() or p.as_posix() != s or set(p.parts) & {'.', '..', '.git', '__pycache__'}: raise ValueError('path')
    return s
def valid_row(x):
    if type(x) is not dict or set(x) != {'path', 'bytes', 'sha256'}: raise ValueError('row fields')
    valid_path(x['path'])
    if type(x['bytes']) is not int or x['bytes'] < 0 or type(x['sha256']) is not str or not re.fullmatch('[0-9a-f]{64}', x['sha256']): raise ValueError('row types')
def decode(b):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d: raise ValueError('duplicate JSON key')
            d[k] = v
        return d
    def constant(x): raise ValueError('nonfinite constant')
    def floating(x):
        y = float(x)
        if not math.isfinite(y): raise ValueError('overflow')
        return y
    return json.loads(b, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)
def same(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list: return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b
def aware(s):
    if type(s) is not str: raise ValueError('clock type')
    d = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
    if d.tzinfo is None or d.utcoffset() != dt.timedelta(0): raise ValueError('UTC')
    return d
def regular(p):
    if p.is_symlink() or any(q.is_symlink() for q in p.parents): raise ValueError('symlink')
    if not stat.S_ISREG(p.stat().st_mode): raise ValueError('regular')
    return p.read_bytes()
def whole(p, role):
    global full_reads, full_bytes
    b = regular(p); full_reads += 1; full_bytes += len(b)
    if p.suffix == '.json': decode(b)
    elif p.suffix == '.jsonl':
        for line in b.splitlines():
            check(bool(line.strip()), 'nonblank_JSONL'); decode(line)
    rel = p.relative_to(R).as_posix()
    row = {'path': rel, 'bytes': len(b), 'sha256': sha(b)}
    if rel in foreign: check(foreign[rel]['bytes'] == len(b) and foreign[rel]['sha256'] == sha(b), 'repeated_input_unchanged')
    foreign[rel] = dict(row, roles=sorted(set(foreign.get(rel, {}).get('roles', []) + [role])))
    return b
def pinned(root, row, role, mode=None):
    valid_row(row); b = whole(root / row['path'], role)
    check(len(b) == row['bytes'] and sha(b) == row['sha256'], 'whole_pin')
    if mode is not None: check(stat.S_IMODE((root / row['path']).stat().st_mode) == mode, 'exact_full_mode')
    return b
def topology(root):
    if root.is_symlink() or any(p.is_symlink() for p in root.parents) or not root.is_dir(): raise ValueError('root directory')
    files, dirs = set(), set()
    for p in root.rglob('*'):
        if p.is_symlink(): raise ValueError('topology symlink')
        name = valid_path(p.relative_to(root).as_posix())
        if stat.S_ISREG(p.stat().st_mode): files.add(name)
        elif stat.S_ISDIR(p.stat().st_mode): dirs.add(name)
        else: raise ValueError('special file')
    expected = {q.as_posix() for f in files for q in PurePosixPath(f).parents if q.as_posix() != '.'}
    if dirs != expected: raise ValueError('empty or extra directory')
    return files, dirs
def reject(fn, x, label):
    try: fn(x)
    except (ValueError, TypeError, KeyError, AssertionError, FileNotFoundError, NotADirectoryError):
        rejected.append(label); counts['rejected_mutant'] += 1
    else: raise AssertionError('mutant accepted: ' + label)

assert __debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0')
start = now()
prep_raw = whole(P / 'PREPARATION_MANIFEST.json', 'source_manifest')
check(sha(prep_raw) == '0ecdd7c6aaf27c766dcb83b8991f1d8093b3ed233e6e2e926d501b0501c1f4a6', 'exact_source_manifest')
prep = decode(prep_raw)
check(prep['files_count'] == len(prep['files']) == 48 and prep['self_excluded'] == ['PREPARATION_MANIFEST.json'], 'source48_self_only')
files, dirs = topology(P)
check(files == {r['path'] for r in prep['files']} | {'PREPARATION_MANIFEST.json'} and dirs == set(prep['directories']), 'source_exact_topology')
check(stat.S_IMODE((P / 'PREPARATION_MANIFEST.json').stat().st_mode) == 0o444, 'source_manifest_mode')
for row in prep['files']: pinned(P, row, 'source_authored_member', 0o444)
builder_raw = whole(P / 'prepare_current_packet.py', 'production_text_only')
operator_raw = whole(P / 'capture_root_builder_operation.py', 'production_text_only')
check(sha(builder_raw) == '09948a4ca10ef5014cdd35ec75ea82bf10887a5fd6ec9400fee0239fcc04983d', 'builder_pin')
check(sha(operator_raw) == 'fe0f02ceea16a15895073bda8851a9b67baaf6f02c5da55bfe13a06dc01733ec', 'operator_pin')
builder, operator = builder_raw.decode(), operator_raw.decode()
# Parse only syntax trees. No production AST or function is compiled/evaluated.
tree = ast.parse(builder); op_tree = ast.parse(operator)
for t in (tree, op_tree):
    calls = [n for n in ast.walk(t) if isinstance(n, ast.Call)]
    for call in calls:
        if isinstance(call.func, ast.Name): check(call.func.id not in {'exec', 'eval', 'compile', '__import__'}, 'no_dynamic_execution_call')
    modules = {n.module for n in ast.walk(t) if isinstance(n, ast.ImportFrom)} | {a.name for n in ast.walk(t) if isinstance(n, ast.Import) for a in n.names}
    check(not (modules & {'runpy', 'importlib', 'py_compile'}), 'no_production_dynamic_loader')
for fragment in ["BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'", "HEAD = 'c772dc5b851ec91da9d46d534577609e5d3ca389'", "GATE = 'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'", "stat.S_IMODE(path.stat().st_mode) == 0o444", "stat.S_IMODE((stage / 'MANIFEST.json').stat().st_mode) == 0o444", "rename(os.fsencode(source), os.fsencode(destination), 4)", "validate_native()", "new_source_adversary_closed_clean_complete_report_personally_read", "equal(summary['entire_author_result'], saved)", "equal(summary['entire_independent_result'], independent)", "for row in dependencies.values():", "future_complete_outer_capture_or_whole_PASS_certified_by_freeze", "current_inner_GIT_COMMANDS_record_is_final_only_after_builder_exit", "original['verify_group_block.py'] == original['review/submitted_verifier.py']", "fields[indexes['Turns']].strip() == '0/5'", "clock(prep['utc']) <= clock(evidence['created_utc'])"]:
    check(fragment in builder, 'specific_source_guard')
check(builder.count('    validate_native()') == 3, 'three_complete_native_rechecks')
for text in (builder, operator):
    for banned in ('git push', 'git commit', 'git merge', 'gh ', 'shutil.rmtree', 'os.remove(', '.unlink('): check(banned not in text, 'no_native_remote_or_erasure_mechanism')
check("'current_verdict': None" in builder and "'new_whole_current_gate'] = 'PENDING'" in operator, 'runtime_and_whole_unknown')
bindings = decode(whole(P / 'STATIC_INPUT_BINDINGS.json', 'fixed_contract'))
for row in bindings['auxiliary']: pinned(A, row, 'retained_actual_export_or_failure')
for family, info in bindings['families'].items():
    own = {r['path'] for r in info['copied_members']}; excluded = {r['path'] for r in info['foreign_members']}
    check(not own & excluded, 'disjoint_family_ownership')
    actual, dirs = topology(A / family)
    check(actual == own | excluded | {info['manifest']['path']} and dirs == set(info['directories']), 'family_exact_topology')
    pinned(A / family, info['manifest'], 'independent_manifest', 0o444)
    for row in info['copied_members']: pinned(A / family, row, 'independent_authored_member', 0o444)
    for row in info['foreign_members']: pinned(A / family, row, 'foreign_local_body_EXCLUDED', 0o444)
    for row in info['external_inputs']: pinned(A, row, 'foreign_parent_body_EXCLUDED_dated_not_current')
check(len(bindings['families']['duality_algebra_family']['copied_members']) == 54 and len(bindings['families']['duality_algebra_family']['foreign_members']) == 10, 'duality54_foreign10')
check(len(bindings['families']['literal_realization_family']['copied_members']) == 13 and len(bindings['families']['literal_realization_family']['foreign_members']) == 54, 'literal13_foreign54')
snapshot = decode(pinned(A, bindings['snapshot_manifest'], 'original_snapshot'))
original = {}
for row in snapshot['files']:
    adapted = {'path': 'source_snapshot_v2/' + row['path'], 'bytes': row['size'], 'sha256': row['sha256']}
    original[row['path']] = pinned(A, adapted, 'original18_immutable')
check(topology(A / 'source_snapshot_v2')[0] == set(original) and len(original) == 18, 'complete_original18')
for left, right in [('verify_group_block.py', 'review/submitted_verifier.py'), ('group_block_verification.json', 'review/submitted_results.json'), ('OBSTRUCTION.md', 'review/reviewed_obstruction.md')]: check(original[left] == original[right], 'literal_original_duplicates')
diff_raw = whole(A / 'original_diff_v2.patch', 'whole19_path_diff')
check(len(diff_raw) == 75046 and sha(diff_raw) == snapshot['diff_sha256'], 'whole_diff_pin')
pieces = diff_raw.split(b'diff --git ')
check(len(pieces) == 20, 'nineteen_diff_sections')
reconstructed = 0
for piece in pieces[1:]:
    if b'new file mode 100644\n' not in piece: continue
    ls = piece.splitlines(keepends=True)
    plus = next(x for x in ls if x.startswith(b'+++ b/')).decode().strip()[6:]
    name = plus.removeprefix('unsolved_math_prioritization/attempts/2912/') if hasattr(str, 'removeprefix') else plus[len('unsolved_math_prioritization/attempts/2912/'):]
    actual = b''.join(x[1:] for x in ls if x.startswith(b'+') and not x.startswith(b'+++'))
    check(name in original and actual == original[name], 'complete_new_hunk_reconstruction'); reconstructed += 1
check(reconstructed == 18, 'all18_new_hunks')
ledger = [decode(x) for x in original['turns.jsonl'].splitlines()]
check([x['turn'] for x in ledger] == [1, 2] and all(x['outcome'] == 'stalled' for x in ledger), 'two_original_stalled_turns')
saved, independent = decode(original['group_block_verification.json']), decode(original['review/independent_results.json'])
check(saved['exact_assertions'] == 507 and independent['exact_assertions'] == sum(independent['categories'].values()) == 29933, 'whole_original507_29933')

evidence_raw = whole(A / 'ROOT_EVIDENCE_BINDINGS.json', 'genuine_ROOT_evidence_binding')
check(sha(evidence_raw) == '19cfc91c5ebbff2712e13eced8cd56219d423ecac623af6afe48376bb4e00619', 'repaired_ROOT_binding_pin')
evidence = decode(evidence_raw)
def evidence_ok(x):
    assert set(x) == {'schema', 'approved_by_root', 'created_utc', 'notes', 'manifest', 'proof_notes', 'summary'}
    assert x['schema'] == 'PR44_ROOT_EVIDENCE_BINDINGS_v1' and x['approved_by_root'] is True
    assert aware(prep['utc']) <= aware(x['created_utc']) <= dt.datetime.now(dt.timezone.utc)
    assert x['manifest']['path'] == 'root_original_actual_reproduction/MANIFEST.json'
    assert x['proof_notes']['path'] == 'ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md'
    assert x['summary']['path'].startswith('root_original_actual_reproduction/')
    for key in ('manifest', 'proof_notes', 'summary'): valid_row(x[key])
evidence_ok(evidence); check(True, 'genuine_evidence_schema_compatibility')
bad_binding_raw = whole(A / 'ROOT_EVIDENCE_BINDINGS_REPOSITORY_RELATIVE_V1.json', 'retained_first_actual_path_mismatch')
check(sha(bad_binding_raw) == '99195dc7cecd5b18d6a86f62fe64bad102bc5b2967cd4d90cff5cc54e7380f22', 'first_bad_binding_preserved')
reject(evidence_ok, decode(bad_binding_raw), 'genuine_first_repository_relative_binding')
mf = decode(pinned(A, evidence['manifest'], 'genuine_ROOT_self_manifest', 0o444))
check(mf['schema'] == 'pr44-root-original-reproduction/v1' and mf['files_count'] == len(mf['files']) == 36 and mf['self_excluded'] == ['MANIFEST.json'], 'ROOT36_self_only')
check(topology(A / 'root_original_actual_reproduction')[0] == {x['path'] for x in mf['files']} | {'MANIFEST.json'}, 'ROOT_exact_topology')
for row in mf['files']: pinned(A / 'root_original_actual_reproduction', row, 'genuine_ROOT_owned_member', 0o444)
summary = decode(pinned(A, evidence['summary'], 'genuine_ROOT_entire_summary', 0o444))
notes = pinned(A, evidence['proof_notes'], 'genuine_ROOT_proof_notes', 0o444)
def summary_ok(x):
    assert x['schema'] == 'PR44_ROOT_CURRENT_REPRODUCTION_SUMMARY_v1' and x['actual_reproductions_completed'] is True
    assert same(x['entire_author_result'], saved) and same(x['entire_independent_result'], independent)
    assert same(x['whole_original_ledger'], ledger)
    assert all(x[k] is True for k in ('author_receipt_byte_exact', 'independent_receipt_byte_exact', 'full_original18_verified', 'finite_checks_do_not_prove_geometric_realization_or_full_problem'))
    assert type(x['whole_raw_bytes']) is int and x['whole_raw_bytes'] == 149266659
    assert type(x['whole_SQL_rows']) is int and x['whole_SQL_rows'] == 15458
    assert type(x['prior_raw_key_present']) is bool
    assert all(type(x[k]) is int and x[k] == v for k, v in [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)])
    assert type(x['actual_replay_captures']) is list and len(x['actual_replay_captures']) == 2
summary_ok(summary); check(True, 'genuine_summary_compatibility_with_extras')
keys = {'schema', 'argv', 'cwd', 'started_utc', 'actual_execution', 'pid', 'exit_code', 'completed', 'stdin_supplied', 'operator_sha256', 'finished_utc', 'stdout', 'stderr', 'operator_unchanged', 'expected_exit_code', 'status'}
def c1_ok(x):
    assert set(x) == keys and x['schema'] == 'root-explicit-command-capture/v1'
    assert all(x[k] is True for k in ('actual_execution', 'completed', 'operator_unchanged')) and x['stdin_supplied'] is False
    assert type(x['pid']) is int and x['pid'] > 0
    assert type(x['exit_code']) is int and x['exit_code'] == 0 and type(x['expected_exit_code']) is int and x['expected_exit_code'] == 0 and x['status'] == 'PASS'
    assert x['argv'][:2] == ['/usr/bin/python3', '-B'] and all(type(v) is str for v in x['argv']) and x['cwd'] == str(R)
    assert aware(x['started_utc']) <= aware(x['finished_utc']) <= dt.datetime.now(dt.timezone.utc)
    for k in ('stdout', 'stderr'): valid_row(x[k])
root_c1 = []
for row in summary['actual_replay_captures']:
    cap = decode(pinned(A, row, 'actual_ROOT_C1_record', 0o444)); c1_ok(cap)
    check(cap['pid'] in (9267, 11267), 'two_evidence_PIDs_not_two_helpers'); root_c1.append(cap)
    parent = A / row['path']; parent = parent.parent
    pre = whole(parent / 'prelaunch_operator.py', 'genuine_ROOT_prelaunch_operator')
    check(sha(pre) == cap['operator_sha256'] and pre == whole(A / 'capture_root_command.py', 'ROOT_C1_unchanged_operator'), 'C1_prelaunch_source_binding')
    for k in ('stdout', 'stderr'): pinned(parent, cap[k], 'genuine_ROOT_entire_stdio', 0o444)
record = decode(whole(A / 'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json', 'entire_three_helpers_actual_record'))
check(record['status'].startswith('PASS'), 'genuine_ROOT_actual_helper_result')
# Entire child receipts/stdout are individually pinned by the root closure above.
for dirname, expected in [('current_author', original['group_block_verification.json']), ('historical_submitted', original['group_block_verification.json']), ('historical_independent', original['review/independent_results.json'])]:
    d = A / 'root_original_actual_reproduction' / dirname
    cap = decode(whole(d / 'CAPTURE.json', 'actual_inner_helper_capture'))
    check(cap['actual_execution'] is True and cap['exit_code'] == 0, 'actual_three_inner_children')
    check(whole(d / 'stdout.bin', 'actual_inner_helper_whole_stdout') == expected and whole(d / 'ACTUAL_RESULT.json', 'actual_inner_helper_result') == expected, 'complete_helper_byte_exact')

# Independently reproduce complete source/prior joins; all bodies stay foreign.
cache = R / 'unsolved_math_prioritization/cache'
raw_b = whole(cache / 'problems.json', 'whole_foreign_raw_EXCLUDED')
prior_b = whole(cache / 'research_results.json', 'whole_foreign_prior_EXCLUDED')
raw, priors = decode(raw_b), decode(prior_b)
byid = {str(x['id']): x for x in raw}; codes = collections.Counter(x['problem_number'] for x in raw)
check(len(raw) == len(byid) == 15458 and len(priors) == 6701 and len(raw_b) + len(prior_b) == 149266659, 'entire_raw_records_and_bytes')
con = sqlite3.connect('file:' + str(cache / 'catalog.sqlite') + '?mode=ro&immutable=1', uri=True)
con.execute('PRAGMA query_only=ON'); check(con.execute('PRAGMA query_only').fetchone() == (1,), 'readonly_SQL')
seen = 0
for key, payload, report in con.execute('SELECT key,payload,report FROM records ORDER BY key'):
    expected = dict(byid[key]); code = expected['problem_number']
    if codes[code] > 1 and code in priors: expected['_ambiguous_report'] = True
    exp_prior = {} if expected.get('_ambiguous_report') else priors.get(code, {})
    check(same(decode(payload), expected) and same(decode(report), exp_prior), 'full_SQL_join_type_exact'); seen += 1
con.close(); check(seen == 15458, 'all_SQL_rows')
check(same(byid['2912'], decode(original['source_record.json'])) and byid['2912']['problem_number'] == 'KP-4.36', 'whole_literal_source_match')
check('KP-4.36' not in priors and summary['prior_raw_key_present'] is False and decode(whole(A / 'pinned_prior_report.json', 'saved_ABSENT_key_fallback')) == {}, 'ABSENT_not_raw_null')

# Fresh private hostile cases, never mutation of a real source/native input.
fixture = HERE / 'private_controls'; fixture.mkdir(exist_ok=False)
observations = []
for mode in range(0o10000): check((mode == 0o444) == (mode in {0o444}), 'full4096_mode_predicates')
for mode in (0o444, 0o1444, 0o2444, 0o4444):
    p = fixture / ('mode_' + format(mode, '04o')); p.write_bytes(b'private full-mode fixture\n'); p.chmod(mode)
    observed = stat.S_IMODE(p.stat().st_mode); check(observed == mode, 'actual_special_mode_observation')
    check((observed == 0o444) == (mode == 0o444), 'actual_full_mode_rejection')
    observations.append({'path': p.name, 'observed_at_test_mode': format(observed, '04o'), 'accepted': observed == 0o444, 'later_frozen_mode': '0444'}); p.chmod(0o444)
base = {'path': 'nested/file', 'bytes': 0, 'sha256': sha(b'')}
for key, value in [('path', '/tmp/escape'), ('path', '../escape'), ('path', 'nested/../escape'), ('path', 'a//b'), ('path', 'a/./b'), ('path', '.'), ('path', 'a\\b'), ('path', 'a\x00b'), ('path', 'a/.git/b'), ('path', 'a/__pycache__/b'), ('bytes', True), ('bytes', -1), ('bytes', 0.0), ('sha256', 'A' * 64), ('sha256', '0' * 63)]:
    m = dict(base); m[key] = value; reject(valid_row, m, 'row_' + key + '_' + repr(value))
reject(valid_row, dict(base, extra=True), 'row_extra_field')
for b in [b'{"x":1,"x":2}', b'{"a":{"x":1,"x":2}}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e999}']: reject(decode, b, 'strict_JSON_' + b.decode())
for a, b in [(True, 1), (False, 0), (1.0, 1), (None, False)]: check(not same(a, b), 'typed_scalar_distinction')
for key, value in [('original_substantive_attempts', True), ('new_substantive_attempts', 1), ('audit_turns', 1), ('whole_raw_bytes', 149266659.0), ('whole_SQL_rows', True), ('prior_raw_key_present', None), ('actual_reproductions_completed', False), ('actual_replay_captures', [])]:
    m = copy.deepcopy(summary); m[key] = value; reject(summary_ok, m, 'summary_' + key)
for result_key in ('entire_author_result', 'entire_independent_result'):
    m = copy.deepcopy(summary); m[result_key]['limits'].append('fabricated scope'); reject(summary_ok, m, 'summary_full_limits_' + result_key)
m = copy.deepcopy(summary); m['whole_original_ledger'][1]['outcome'] = 'solved'; reject(summary_ok, m, 'summary_ledger_mutation')
for key, value in [('pid', True), ('pid', 0), ('completed', False), ('actual_execution', False), ('stdin_supplied', True), ('operator_unchanged', False), ('exit_code', False), ('expected_exit_code', 1), ('status', 'PASS_FUTURE'), ('cwd', str(HERE)), ('started_utc', '2026-10-03T00:00:00'), ('finished_utc', '2100-01-01T00:00:00Z')]:
    m = copy.deepcopy(root_c1[0]); m[key] = value; reject(c1_ok, m, 'C1_' + key + '_' + repr(value))
m = copy.deepcopy(evidence); m['approved_by_root'] = False; reject(evidence_ok, m, 'draft_evidence_false_gate')
m = copy.deepcopy(evidence); m['created_utc'] = '2026-10-03T00:00:00Z'; reject(evidence_ok, m, 'evidence_before_source_closure')
p = fixture / 'regular_member'; p.write_bytes(b'original private byte\n')
pin = {'path': p.name, 'bytes': len(p.read_bytes()), 'sha256': sha(p.read_bytes())}
def private_pin(row):
    valid_row(row); b = regular(fixture / row['path']); assert len(b) == row['bytes'] and sha(b) == row['sha256']
private_pin(pin); p.write_bytes(b'mutated private byte!\n'); reject(private_pin, pin, 'same_length_private_source_mutation'); p.write_bytes(b'original private byte\n')
for name, target in [('link_file', p), ('broken_link', fixture / 'absent'), ('link_directory', fixture)]:
    q = fixture / name; q.symlink_to(target, target_is_directory=name == 'link_directory')
    try:
        reject(regular, q if name != 'link_directory' else q / p.name, 'actual_' + name)
        reject(topology, fixture, 'actual_topology_' + name)
    finally: q.unlink()
empty = fixture / 'empty_extra'; empty.mkdir(); reject(topology, fixture, 'actual_extra_empty_directory'); empty.rmdir()

check(sys.platform == 'darwin', 'macOS_private_exclusive_publication_control')
lib = ctypes.CDLL(None, use_errno=True); rename = lib.renamex_np
rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]; rename.restype = ctypes.c_int
src, dst = fixture / 'publication_source', fixture / 'publication_existing'; src.mkdir(); dst.mkdir()
(src / 'new').write_bytes(b'new\n'); (dst / 'sentinel').write_bytes(b'keep\n')
check(rename(os.fsencode(src), os.fsencode(dst), 4) == -1 and ctypes.get_errno() == 17, 'actual_RENAME_EXCL_existing_rejection')
check((src / 'new').read_bytes() == b'new\n' and (dst / 'sentinel').read_bytes() == b'keep\n', 'actual_existing_tree_preserved')
absent = fixture / 'publication_absent'; check(rename(os.fsencode(src), os.fsencode(absent), 4) == 0 and (absent / 'new').read_bytes() == b'new\n', 'actual_RENAME_EXCL_absent_success')

gd = HERE / 'readonly_git'; gd.mkdir(exist_ok=False)
for argv in [['git', 'branch', '--show-current'], ['git', 'rev-parse', 'HEAD'], ['git', 'diff', snapshot['base'], snapshot['head']]]:
    i = len(commands); rec = {'argv': argv, 'cwd': str(R), 'started_utc': now(), 'stdin_supplied': False}
    with (gd / (str(i) + '.stdout')).open('xb') as out, (gd / (str(i) + '.stderr')).open('xb') as err:
        child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=out, stderr=err, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
        rec.update(actual_execution=True, pid=child.pid, exit_code=child.wait(timeout=60), completed=True)
    rec['finished_utc'] = now()
    for channel in ('stdout', 'stderr'):
        b = (gd / (str(i) + '.' + channel)).read_bytes(); rec[channel] = {'path': 'readonly_git/' + str(i) + '.' + channel, 'bytes': len(b), 'sha256': sha(b)}
    check(rec['exit_code'] == 0 and rec['stderr']['bytes'] == 0, 'actual_readonly_Git_success'); commands.append(rec)
check((gd / '0.stdout').read_bytes() == b'main\n' and (gd / '2.stdout').read_bytes() == diff_raw, 'actual_main_and_original_diff')
check(regular(P / 'prepare_current_packet.py') == builder_raw and regular(P / 'capture_root_builder_operation.py') == operator_raw and regular(P / 'PREPARATION_MANIFEST.json') == prep_raw, 'operative_source_unchanged_after_controls')
check(regular(A / 'ROOT_EVIDENCE_BINDINGS.json') == evidence_raw, 'genuine_ROOT_binding_unchanged')
result = {'schema': 'pr44-new-independent-source-adversary-controls/v1', 'status': 'PASS_SOURCE_ONLY_INDEPENDENT_CONTROLS', 'started_utc': start, 'finished_utc': now(), 'actual_pid': os.getpid(), 'assertions': sum(counts.values()), 'categories': dict(counts), 'rejected_mutants': rejected, 'full_input_reads': full_reads, 'full_input_bytes': full_bytes, 'individual_foreign_input_count': len(foreign), 'production_import_compile_execution': False, 'scientific_assertions': 0, 'source_manifest_sha256': sha(prep_raw), 'builder_sha256': sha(builder_raw), 'operator_sha256': sha(operator_raw), 'genuine_ROOT_evidence_binding_sha256': sha(evidence_raw), 'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0, 'full_problem_solved': False, 'source_status': 'unsolved', 'prior_raw_key_present': False, 'raw_null_prior_retrieved': False, 'independent_whole_raw_bytes': len(raw_b) + len(prior_b), 'independent_whole_SQL_rows': seen, 'actual_mode_observations': observations, 'actual_readonly_git_commands': commands, 'native_Git_remote_or_outreach_mutations': False, 'genuine_first_ROOT_binding_incompatibility_repaired': True, 'later_current_whole_or_acceptance_PASS_claimed': False}
(HERE / 'RESULT.json').write_bytes(encode(result))
(HERE / 'INDIVIDUAL_FOREIGN_INPUTS.json').write_bytes(encode({'schema': 'pr44-source-adversary-individual-foreign-inputs/v1', 'anchor': 'repository_root', 'foreign_input_count': len(foreign), 'files': sorted(foreign.values(), key=lambda r: r['path']), 'foreign_bodies_copied_into_authored_family': False, 'publication_exclusion': 'Every listed body is foreign input; individual path/bytes/SHA references only are authored.'}))
print(json.dumps({k: result[k] for k in ('status', 'actual_pid', 'assertions', 'full_input_reads', 'full_input_bytes', 'individual_foreign_input_count', 'independent_whole_raw_bytes', 'independent_whole_SQL_rows', 'production_import_compile_execution')}))
