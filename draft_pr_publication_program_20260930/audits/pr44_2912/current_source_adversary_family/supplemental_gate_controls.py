"""Own independent gate schemas with private synthetic records, never ROOT approval."""
from pathlib import Path, PurePosixPath
import collections
import copy
import datetime as dt
import hashlib
import json
import os
import re

HERE = Path(__file__).absolute().parent
A = HERE.parent
P = A / 'current_preparation_family'
counts = collections.Counter()
rejected = []
def check(x, label): assert x, label; counts[label] += 1
def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def clock(s):
    assert type(s) is str
    d = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
    assert d.tzinfo is not None and d.utcoffset() == dt.timedelta(0)
    return d
def reject(fn, x, label):
    try: fn(x)
    except (AssertionError, ValueError, KeyError, TypeError): rejected.append(label); counts['rejected_gate_mutant'] += 1
    else: raise AssertionError('accepted ' + label)
def rows(xs):
    assert type(xs) is list
    names = set()
    for x in xs:
        assert type(x) is dict and set(x) == {'path', 'bytes', 'sha256'}
        s = x['path']; assert type(s) is str and s and '\\' not in s and '\x00' not in s
        p = PurePosixPath(s); assert not p.is_absolute() and p.as_posix() == s and not set(p.parts) & {'.', '..', '.git', '__pycache__'}
        assert s not in names; names.add(s)
        assert type(x['bytes']) is int and x['bytes'] >= 0 and type(x['sha256']) is str and re.fullmatch('[0-9a-f]{64}', x['sha256'])
    return names
prep_b = (P / 'PREPARATION_MANIFEST.json').read_bytes()
assert sha(prep_b) == '0ecdd7c6aaf27c766dcb83b8991f1d8093b3ed233e6e2e926d501b0501c1f4a6'
prep = json.loads(prep_b)
flags = list(json.loads((P / 'DRAFT_ROOT_READ_LEDGER.json').read_bytes())['root_flags'])
check(len(flags) == 9 and len(set(flags)) == 9, 'nine_unique_ROOT_flags')
native = {'unsolved_math_prioritization/' + n for n in ['QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json', 'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json', 'cache/research_results.json', 'cache/catalog.sqlite', 'review_v2/related_target_groups.json']}
native.add('draft_pr_publication_program_20260930/inventory.json')
check(len(native) == 13, 'exact_native13_set')
def fresh_ok(x):
    assert set(x) == {'schema', 'approved_by_root', 'created_utc', 'reason', 'current_head', 'files'}
    assert x['schema'] == 'PR44_ROOT_FRESH13_INPUT_PREIMAGES_v1' and x['approved_by_root'] is True
    assert clock(prep['utc']) <= clock(x['created_utc']) <= dt.datetime.now(dt.timezone.utc)
    assert type(x['reason']) is str and len(x['reason'].strip()) >= 40
    assert type(x['current_head']) is str and re.fullmatch('[0-9a-f]{40}', x['current_head'])
    assert len(x['files']) == 13 and rows(x['files']) == native
# These records are private syntactic controls, not observed current native bytes.
fresh = {'schema': 'PR44_ROOT_FRESH13_INPUT_PREIMAGES_v1', 'approved_by_root': True, 'created_utc': now(), 'reason': 'PRIVATE SYNTHETIC CONTROL ONLY: no ROOT approval or native authority.', 'current_head': '0' * 40, 'files': [{'path': p, 'bytes': 0, 'sha256': sha(b'')} for p in sorted(native)]}
fresh_ok(fresh); check(True, 'synthetic_fresh_schema_positive_only')
reject(fresh_ok, json.loads((P / 'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes()), 'actual_false_null_fresh_DRAFT')
for key, value in [('approved_by_root', False), ('created_utc', None), ('created_utc', '2026-10-03T00:00:00Z'), ('created_utc', '2100-01-01T00:00:00Z'), ('created_utc', '2026-10-03T00:00:00-07:00'), ('reason', ''), ('current_head', 'a' * 39), ('current_head', 'A' * 40), ('files', []), ('schema', 'PR43_ROOT_FRESH13_INPUT_PREIMAGES_v1')]:
    m = copy.deepcopy(fresh); m[key] = value; reject(fresh_ok, m, 'fresh_' + key + '_' + repr(value))
m = copy.deepcopy(fresh); m['files'][1] = m['files'][0]; reject(fresh_ok, m, 'fresh_duplicate13')
m = copy.deepcopy(fresh); m['files'][-1]['path'] = 'unsolved_math_prioritization/wrong'; reject(fresh_ok, m, 'fresh_missing_native_member')
m = copy.deepcopy(fresh); m['files'][0]['bytes'] = False; reject(fresh_ok, m, 'fresh_bool_byte_count')
m = copy.deepcopy(fresh); m['foreign_historical_head'] = '0' * 40; reject(fresh_ok, m, 'fresh_extra_historical_authority_key')

def reading_ok(x, science=False):
    assert x['schema'] == ('PR44_ROOT_SCIENCE_CARD_v1' if science else 'PR44_ROOT_PRIMARY_READ_LEDGER_v1')
    assert x['reading_completed'] is True and x['root_flags'] == dict.fromkeys(flags, True)
    assert all(type(x['root_flags'][f]) is bool for f in flags)
    assert type(x['reading_notes']) is str and len(x['reading_notes'].strip()) >= 40
    assert clock(prep['utc']) <= clock(x['created_utc']) <= dt.datetime.now(dt.timezone.utc)
    assert all(type(x[k]) is int and x[k] == v for k, v in [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)])
    if science:
        assert x['status'] == 'unsolved' and x['partial_valid'] is True and x['full_problem_solved'] is False and x['novelty_claimed'] is False
        assert type(x['turn_limit']) is int and x['turn_limit'] == 5
        assert all(x[k] is False for k in ['paper_created', 'new_DOI_created', 'tracker_row_created'])
        assert x['new_whole_current_gate'] == 'PENDING'
        assert all(x[k] is None for k in ['current_model', 'current_reasoning_effort', 'current_deadline_utc', 'current_verdict'])
for filename, science in [('DRAFT_ROOT_READ_LEDGER.json', False), ('DRAFT_ROOT_SCIENCE_CARD.json', True)]:
    draft = json.loads((P / filename).read_bytes())
    reject(lambda x: reading_ok(x, science), draft, 'actual_false_null_' + filename)
    control = copy.deepcopy(draft); control.update(reading_completed=True, root_flags=dict.fromkeys(flags, True), reading_notes='PRIVATE SYNTHETIC CONTROL ONLY: does not attest actual completed ROOT reading.', created_utc=now())
    if science: control['partial_valid'] = True
    reading_ok(control, science); check(True, 'synthetic_reading_schema_positive_only')
    for flag in flags:
        m = copy.deepcopy(control); m['root_flags'][flag] = False
        reject(lambda x: reading_ok(x, science), m, filename + '_false_' + flag)
    m = copy.deepcopy(control); m['root_flags'][flags[0]] = 1
    reject(lambda x: reading_ok(x, science), m, filename + '_integer_true_flag')
    m = copy.deepcopy(control); m['audit_turns'] = True
    reject(lambda x: reading_ok(x, science), m, filename + '_bool_audit_count')
    if science:
        for key, value in [('status', 'claimed_solved'), ('full_problem_solved', True), ('novelty_claimed', True), ('turn_limit', True), ('paper_created', True), ('new_DOI_created', True), ('tracker_row_created', True), ('new_whole_current_gate', 'PASS'), ('current_verdict', 'PASS'), ('current_model', 'historical-model'), ('current_reasoning_effort', 'historical-effort'), ('current_deadline_utc', '2026-09-30T07:27:00Z')]:
            m = copy.deepcopy(control); m[key] = value
            reject(lambda x: reading_ok(x, science), m, 'science_' + key)
builder = (P / 'prepare_current_packet.py').read_text()
check("equal(obj['root_flags'], {flag: True for flag in FLAGS})" in builder, 'production_type_distinct_root_flags')
check("fields[indexes['Status']].strip() == 'queued'" in builder and "fields[indexes['Turns']].strip() == '0/5'" in builder, 'production_exact_prequeue_gate')
check("for name, value in [('Status', 'unsolved'), ('Turns', '2/5'), ('Findings', finding)]" in builder, 'production_exact_three_queue_changes')
check("if index not in allowed" in builder and "Chat/DOI" in builder, 'production_all_other_queue_fields_preserved')
check('genuine_separate_ROOT_prerequisite' in builder and "args.execute" in builder, 'production_real_separate_prerequisites')
check(sha((P / 'PREPARATION_MANIFEST.json').read_bytes()) == sha(prep_b), 'source_manifest_unchanged_after_gate_controls')
result = {'schema': 'pr44-source-adversary-supplemental-gate-controls/v1', 'status': 'PASS', 'actual_pid': os.getpid(), 'utc': now(), 'assertions': sum(counts.values()), 'categories': dict(counts), 'rejected_mutants': rejected, 'synthetic_positive_records_are_not_ROOT_approvals': True, 'production_import_compile_or_execution': False, 'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0, 'whole_current_gate_still_PENDING': True, 'native_or_remote_mutation': False}
(HERE / 'SUPPLEMENTAL_GATE_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'actual_pid': os.getpid(), 'assertions': result['assertions'], 'rejected_mutants': len(rejected), 'production_execution': False}))
