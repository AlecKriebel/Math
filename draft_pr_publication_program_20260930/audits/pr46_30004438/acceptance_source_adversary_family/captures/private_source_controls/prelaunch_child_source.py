#!/usr/bin/env python3
"""Handwritten SOURCE controls; proposed production sources are only read as text."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone, timedelta
import copy
import hashlib
import io
import json
import math
import os
import stat
import sys
import tokenize
from capture_private import capture

assert __debug__ and sys.flags.optimize == 0
F = Path(__file__).resolve().parent
A = F.parent
R = A.parents[2]
P = A / 'acceptance_preparation_family'
C = A / 'reviewed_candidate'
W = A / 'current_whole_adversary_family'
EXPECTED_PREP = 'd97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab'
reads = []
assertions = 0
rejects = []


def require(ok, name):
    global assertions
    assertions += 1
    if not ok:
        raise AssertionError(name)


def equal(x, y):
    if type(x) is not type(y):
        return False
    if type(x) is dict:
        return x.keys() == y.keys() and all(equal(x[k], y[k]) for k in x)
    if type(x) is list:
        return len(x) == len(y) and all(equal(a, b) for a, b in zip(x, y))
    return x == y


def parse(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError('duplicate key')
            out[k] = v
        return out
    def floating(value):
        n = float(value)
        if not math.isfinite(n):
            raise ValueError('nonfinite decoded number')
        return n
    def constant(value):
        raise ValueError('nonfinite constant')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=floating, parse_constant=constant)


def canonical(name):
    if type(name) is not str or not name or name == '.' or '\\' in name or '\0' in name:
        raise ValueError('bad path')
    parts = name.split('/')
    if any(x in {'', '.', '..', '.git', '__pycache__'} for x in parts) or name.startswith('/'):
        raise ValueError('noncanonical path')
    return name


def body(path):
    path = Path(path)
    require(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'regular body')
    for q in path.parents:
        require(not q.is_symlink(), 'no symlink ancestor')
    raw = path.read_bytes()
    reads.append({'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                  'full_mode': stat.S_IMODE(path.lstat().st_mode)})
    return raw


def pinned(path, ref, mode=None):
    raw = body(path)
    require(type(ref['bytes']) is int and len(raw) == ref['bytes'], 'exact typed byte size')
    require(hashlib.sha256(raw).hexdigest() == ref['sha256'], 'exact full hash')
    if mode is not None:
        require(type(mode) is int and stat.S_IMODE(path.lstat().st_mode) == mode, 'exact full mode')
    return raw


def archive_syntax(base, name, raw):
    if name.endswith('.json'):
        if name == 'family_evidence/projective_algebra_family/failed01_run_stdout.json' and base == C:
            require(raw == b'', 'only literal failed empty JSON exception')
        else:
            parse(raw)
    if name.endswith('.jsonl'):
        special = {
            'original_preparation_archive/original_native_selected/assessment_history.jsonl': '0c7d72e9e188763a743e59ea13367ba23d66bf8dbaa5c67d7d0f325cee8ffeb5',
            'original_preparation_archive/original_native_selected/history.jsonl': 'cd650a0dec4b3ff77299d73300268e7bd465484f4b296636336f28ecdd79ae31',
        }
        if base == C and name in special:
            require(hashlib.sha256(raw).hexdigest() == special[name], 'literal selected-history body')
            obj = parse(raw)
            require(type(obj) is dict and obj['selection_only'] is True and obj['selected_problem_id'] == '30004438'
                    and obj['complete_selected_objects'] == [] and obj['priority_or_claim_verification'] is False,
                    'selected-only object is not event ledger')
        else:
            require(not raw or raw.endswith(b'\n'), 'complete actual JSONL')
            for line in raw.splitlines():
                parse(line)


def closed(base, manifest_name, digest=None, count=None):
    raw = body(base / manifest_name)
    if digest is not None:
        require(hashlib.sha256(raw).hexdigest() == digest, 'fixed manifest identity')
    mf = parse(raw)
    rr = mf['files']
    if type(rr) is dict:
        rr = [{'path': k, **v} for k, v in rr.items()]
    require(type(rr) is list and type(mf['files_count']) is int and len(rr) == mf['files_count'], 'typed count')
    if count is not None:
        require(len(rr) == count, 'fixed count')
    require(mf['self_excluded'] == [manifest_name], 'only root self excluded')
    names = []
    for z in rr:
        canonical(z['path'])
        names.append(z['path'])
        raw = pinned(base / z['path'], z, 0o444)
        archive_syntax(base, z['path'], raw)
    require(len(set(names)) == len(names) and manifest_name not in names, 'unique self-excluding rows')
    paths = list(base.rglob('*'))
    require(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths), 'regular recursive closure')
    require({p.relative_to(base).as_posix() for p in paths if p.is_file()} == set(names) | {manifest_name}, 'exact files')
    expected_dirs = {p.as_posix() for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    require({p.relative_to(base).as_posix() for p in paths if p.is_dir()} == expected_dirs, 'exact directory topology')
    require(stat.S_IMODE((base / manifest_name).stat().st_mode) == 0o444, 'manifest final mode')
    return mf, rr


def rejected(label, fn):
    try:
        fn()
    except (ValueError, TypeError, KeyError, AssertionError):
        rejects.append(label)
        require(True, 'real private rejection ' + label)
    else:
        raise AssertionError('accepted private mutant ' + label)


def readonly_git(label, argv):
    cap = capture(label, ['git'] + argv, R)
    return Path(cap['stdout']['path']).read_bytes()


started = datetime.now(timezone.utc).isoformat()
before_head = readonly_git('main_before', ['rev-parse', 'HEAD'])
branch = readonly_git('branch', ['branch', '--show-current'])
require(branch == b'main\n', 'stay main')
dirty = readonly_git('tracked_dirty_before', ['diff', '--name-only', '-z'])
prep, prep_rows = closed(P, 'PREPARATION_MANIFEST.json', EXPECTED_PREP, 166)
current, current_rows = closed(C, 'MANIFEST.json', '66239699390b279235c4064208e63134049a5804884818de9176d377476a189d', 946)
whole, whole_rows = closed(W, 'MANIFEST.json', 'be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2', 245)
inputs = parse(body(P / 'INPUT_BINDINGS.json'))
require(inputs['whole_binding_completed'] is True and len(inputs['external_input_rows']) == inputs['external_input_count'] == 1877, 'complete whole external bindings')
for ref in inputs['pins'].values():
    canonical(ref['path']); pinned(R / ref['path'], ref)
for ref in inputs['external_input_rows']:
    literal = Path(ref['path'])
    require(literal.is_absolute() and str(literal).startswith(str(R) + '/'), 'foreign inside repository')
    require(literal.resolve().is_relative_to(R) and not literal.is_symlink(), 'foreign canonical confinement')
    pinned(literal, ref, ref['full_mode'])

for name, key in [('EXPECTED_ROOT_WHOLE_REVIEW.json', 'closed_root_whole_inspection'),
                  ('EXPECTED_WHOLE_MANIFEST.json', 'closed_whole_manifest'),
                  ('EXPECTED_WHOLE_VERDICT.json', 'closed_whole_result'),
                  ('EXPECTED_EXTERNAL_INPUT_INVENTORY.json', 'closed_whole_external_inventory'),
                  ('EXPECTED_PREVIOUS_POST.json', 'previous_post'),
                  ('EXPECTED_PREVIOUS_ROOT_POST.json', 'previous_root_post')]:
    require(equal(parse(body(P / name)), parse(pinned(R / inputs[key]['path'], inputs[key]))), 'entire typed expected ' + name)

previous = parse(pinned(R / inputs['previous_mirror']['path'], inputs['previous_mirror']))
require(len(previous['entries']) == 35 and len(set(z['pr'] for z in previous['entries'])) == 35
        and 45 in previous['required_completed_prs'] and 46 not in previous['required_completed_prs'], 'all35 original primaries')
prior_optional_presence = [{'pr': e['pr'], 'keys': sorted(e), 'duplicate_key_present': 'duplicates' in e} for e in previous['entries']]
for e in previous['entries']:
    b = e['budget']; require(type(b['used']) is int and type(b['limit']) is int and 0 <= b['used'] <= b['limit'], 'typed prior budget')
    for key in ['acceptance', 'audit_acceptance', 'remote', 'accepted_source', 'canonical_acceptance_text', 'canonical_manifest', 'artifact']:
        if key in e:
            ref = e[key]; raw = body(R / canonical(ref['path'])); require(hashlib.sha256(raw).hexdigest() == ref['sha256'], 'entire old evidence body')
    ledger = body(R / canonical(b['ledger']['path'])); require(hashlib.sha256(ledger).hexdigest() == b['ledger']['sha256'], 'entire original prior ledger')

snapshot = parse(body(A / 'snapshot_manifest.json'))
require(len(snapshot['files']) == 13, 'all13 originals')
immutable = {'SOURCE_STATUS.md', 'independent_review/independent_checks.py', 'independent_review/independent_results.json',
             'provenance.json', 'source_record.json', 'turns.json', 'verification.json', 'verify.py'}
admin = {'status.json', 'readiness.json', 'independent_review/verdict.json', 'independent_review/review_summary.json'}
for row in snapshot['files']:
    n = row['relative_path']; original = pinned(A / 'source_snapshot' / n, row, 0o444)
    require(body(C / 'original_archive' / n) == original, 'literal original13 archive')
    if n in immutable:
        require(body(C / n) == original, 'literal operative8')
ledger = parse(body(C / 'turns.json'))
require(type(ledger) is dict and ledger['substantive_turns_used'] == 0 and type(ledger['substantive_turns_used']) is int
        and ledger['source_verification_responses'] == 1 and ledger['turn_limit'] == 5, 'object ledger original0/5 response1')
for changed in [{'substantive_turns_used': False}, {'substantive_turns_used': 1}, {'turn_limit': 4}, {'new_proof_turn': 0}]:
    mutant = copy.deepcopy(ledger); mutant.update(changed)
    require(not equal(mutant, ledger), 'whole zero-turn object mutant distinct')

frozen_names = {z['path'] for z in current_rows}
overlay = frozen_names | {'reviewed_pending_administration/' + n for n in admin} | {
    'reviewed_pending_administration/MANIFEST.json', 'ACCEPTED_QUEUE_PATCH.json', 'CURRENT_ACCEPTANCE_SCOPE.md',
    'CURRENT_CONTEXT_PRESENT.md', 'CURRENT_AUDIT_SCOPE_PRESENT.md'}
accepted = overlay | {'acceptance.json', 'ACCEPTANCE.md'}
require(len(overlay) == 955 and len(accepted) == 957 and 'MANIFEST.json' not in accepted, '955 overlay and957 payload self separate')

draft = parse(body(P / 'DRAFT_ROOT_IMMUTABLE_BINDINGS.json'))
plan = parse(body(P / 'DRAFT_FINAL_PLAN.json'))
require(draft['created_utc'] is None and draft['root_acceptance_source_review_completed'] is False
        and draft['acceptance_source_manifest'] is None and draft['acceptance_source_verdict'] is None, 'genuine pending bindings')
require(plan['partial_valid'] is None and plan['preparation_manifest_sha256'] is None and plan['root_bindings'] is None
        and plan['immutable_evidence_references'] == [] and plan['root_acceptance_source_review_completed'] is False, 'genuine pending reviewed final plan')
for obj in [draft, plan]:
    require(obj['original_substantive_attempts'] == 0 and obj['new_substantive_attempts'] == 0 and obj['audit_turns'] == 0, 'no false budget credit')
    if 'current_model' in obj:
        require(all(obj[k] is None for k in ['current_model', 'current_reasoning_effort', 'current_deadline_utc']), 'explicit current runtime null')

contract = parse(body(P / 'ROOT_POST_CONTRACT.json'))
keys = contract['required_ROOT_complete_keyset']
require(type(keys) is list and len(keys) == len(set(keys)) == 21, 'exact21-key whole post contract')
require(contract['future_ROOT_post_completed'] is False and contract['source_only'] is True, 'post contract is pending source')
post = parse(pinned(R / inputs['previous_post']['path'], inputs['previous_post']))
rootpost = parse(pinned(R / inputs['previous_root_post']['path'], inputs['previous_root_post']))
require(equal(rootpost['entire_post'], post) and rootpost['completed_primary_prs'] == 35, 'whole predecessor post not token')
for ref in rootpost['all_six_real_phase_captures'] + [rootpost['final_sealer_actual_capture']]:
    cap_path = R / ref['path']; cap = parse(pinned(cap_path, ref))
    require(cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code'] == 0
            and type(cap['pid']) is int and cap['pid'] > 0, 'genuine full predecessor actual capture')
    for channel in ['stdout', 'stderr']:
        pinned(cap_path.parent / cap[channel]['path'], cap[channel])
    for source_name in ['PRELAUNCH_SOURCE.py', 'PRELAUNCH_OPERATOR.py']:
        body(cap_path.parent / source_name)

source_reads = []
for name in ['pr46_guards.py', 'seal_final_evidence.py', 'capture_root_final_operation.py',
             'integrate_reviewed_partial.py', 'state_mirror_reconciliation.py', 'verify_post_acceptance.py']:
    raw = body(P / name); text = raw.decode(); stack = []
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type != tokenize.OP:
            continue
        if token.string in {'(', '[', '{'}:
            stack.append(token.string)
        elif token.string in {')', ']', '}'}:
            require(bool(stack) and stack.pop() == {')': '(', ']': '[', '}': '{'}[token.string], 'lexical delimiter')
    require(not stack, 'all lexical delimiters closed')
    source_reads.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                         'source_only_lexical_scan': True, 'imported_compiled_executed': False})

for label, raw in [('duplicate', b'{"a":1,"a":2}'), ('NaN', b'NaN'), ('infinite', b'Infinity'),
                   ('overflow', b'1e999'), ('trailing', b'{} {}'), ('blank', b'')]:
    rejected('json_' + label, lambda raw=raw: parse(raw))
require(not equal(None, {}) and not equal(False, 0) and not equal(0, 0.0), 'null and recursive scalar types exact')
for name in ['', '.', '..', '/a', 'a//b', 'a/./b', 'a/../b', 'a\\b', '.git/x', '__pycache__/x', 'x\0y']:
    rejected('path_' + repr(name), lambda name=name: canonical(name))

def clock(value):
    if type(value) is not str or value != value.strip():
        raise ValueError('clock type')
    d = datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    if d.tzinfo is None or d.utcoffset() != timedelta(0) or d > datetime.now(timezone.utc):
        raise ValueError('clock scope')
    return d

for value in [None, True, '2026-01-01T00:00:00', '2026-01-01T00:00:00+01:00',
              ' 2026-01-01T00:00:00Z', (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()]:
    rejected('clock_' + repr(value), lambda value=value: clock(value))
require(clock('2026-01-01T00:00:00Z').utcoffset() == timedelta(0), 'aware zero clock accepted privately')

probe = F / 'MODE_PROBE'
probe.write_bytes(b'own-mode-probe\n')
for mode in range(4096):
    probe.chmod(mode)
    require(stat.S_IMODE(probe.stat().st_mode) == mode, 'actual full12-bit chmod readback')
probe.chmod(0o644)
require(probe.read_bytes() == b'own-mode-probe\n', 'mode probe body preserved')
probe.unlink()

# Independent direct countermodel of the two literal operations. No production
# function is imported, extracted, compiled or run. Only own files are mutated.
model = F / 'PRIVATE_MODEL'
model.mkdir()
program_log = model / 'RESEARCH_LOG.md'
program_log.write_bytes(b'foreign prior work\n')
protected_before = body(program_log)
program_log.write_bytes(protected_before + b'authorized program checkpoint\n')
foreign_log_countermodel = {'production_foreign_scope_allows_program_log': True,
    'program_log_is_native13_or_selected_audit_or_canonical': False,
    'finalize_appends_program_log_after_last_foreign_check': True,
    'captured_before_sha256': hashlib.sha256(protected_before).hexdigest(),
    'after_sha256': hashlib.sha256(body(program_log)).hexdigest(),
    'full_preservation_after_append': program_log.read_bytes() == protected_before,
    'later_mirror_foreign_check_would_reject': program_log.read_bytes() != protected_before,
    'model_only_not_production_execution': True}
require(foreign_log_countermodel['full_preservation_after_append'] is False, 'protected-log countermodel genuinely changes bytes')
program_log.unlink(); model.rmdir()

native_refs = parse(body(P / 'EXPECTED_PREVIOUS_ROOT_POST.json'))['current13']
before_native = []
for ref in native_refs:
    raw = body(R / ref['path'])
    before_native.append({'path': ref['path'], 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                          'full_mode': stat.S_IMODE((R / ref['path']).stat().st_mode)})
state = parse(body(R / 'unsolved_math_prioritization/state.json'))
history = body(R / 'unsolved_math_prioritization/history.jsonl')
require(len(state) == 36 and '30004438' not in state and sum(v['turns_used'] for v in state.values()) == 44, 'live pre46 disposition only')
require(not history or history.endswith(b'\n'), 'whole native actual history complete')
for line in history.splitlines():
    parse(line)
after_head = readonly_git('main_after', ['rev-parse', 'HEAD'])
after_native = []
for ref in native_refs:
    raw = body(R / ref['path']); after_native.append({'path': ref['path'], 'bytes': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest(), 'full_mode': stat.S_IMODE((R / ref['path']).stat().st_mode)})
require(before_head == after_head and equal(before_native, after_native), 'private controls preserve main/native13')
result = {'schema': 'pr46-handwritten-independent-source-controls/v1', 'status': 'PASS_PRIVATE_SOURCE_CONTROLS_WITH_BOUNDARY_FINDING',
          'actual_pid': os.getpid(), 'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
          'assertions': assertions, 'preparation_manifest_sha256': EXPECTED_PREP,
          'production_imported_compiled_executed': False, 'all4096_actual_full_mode_probes': True,
          'full_input_reads': reads, 'unique_input_paths': len({z['path'] for z in reads}),
          'read_byte_sum': sum(z['bytes'] for z in reads), 'source_text_reads': source_reads,
          'private_mutant_rejections': rejects, 'prior_optional_presence': prior_optional_presence,
          'overlay_count': len(overlay), 'accepted_payload_count': len(accepted),
          'foreign_log_countermodel': foreign_log_countermodel,
          'main_before': before_head.decode().strip(), 'main_after': after_head.decode().strip(),
          'tracked_dirty_paths_before': dirty.decode().split('\0')[:-1], 'native13_before': before_native,
          'native13_after': after_native, 'future_acceptance_approved': False,
          'whole_current_mathematical_acceptance_supplied': False, 'new_substantive_turns': 0, 'audit_turns': 0,
          'foreign_raw_PDF_OCR_SQL_bodies_copied': False}
(F / 'PRIVATE_CONTROL_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'actual_pid', 'assertions', 'unique_input_paths', 'read_byte_sum',
    'production_imported_compiled_executed', 'overlay_count', 'accepted_payload_count', 'foreign_log_countermodel']}, indent=2))
